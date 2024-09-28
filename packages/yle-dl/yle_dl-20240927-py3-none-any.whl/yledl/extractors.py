# This file is part of yle-dl.
#
# Copyright 2010-2024 Antti Ajanki and others
#
# Yle-dl is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yle-dl is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with yle-dl. If not, see <https://www.gnu.org/licenses/>.

import itertools
import json
import logging
import os.path
import re
from dataclasses import dataclass, field
from datetime import datetime
from requests import HTTPError
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs
from .backends import HLSAudioBackend, DASHHLSBackend, WgetBackend
from .http import update_url_query
from .io import OutputFileNameGenerator
from .kaltura import YleKalturaApiClient
from .localization import TranslationChooser
from .streamflavor import StreamFlavor, failed_flavor
from .streamprobe import FullHDFlavorProber
from .subtitles import Subtitle
from .timestamp import parse_areena_timestamp, format_finnish_short_weekday_and_date
from .titleformatter import TitleFormatter


logger = logging.getLogger('yledl')


def extractor_factory(url, language_chooser, httpclient, title_formatter, ffprobe):
    if (
        re.match(r'^https?://yle\.fi/aihe/', url)
        or re.match(r'^https?://svenska\.yle\.fi/artikel/', url)
        or re.match(r'^https?://svenska\.yle\.fi/a/', url)
    ):
        logger.debug(f'{url} is an Elävä Arkisto URL')
        return ElavaArkistoExtractor(
            language_chooser, httpclient, title_formatter, ffprobe
        )
    elif (
        re.match(r'^https?://areena\.yle\.fi/audio/ohjelmat/[-a-zA-Z0-9]+', url)
        or re.match(r'^https?://areena\.yle\.fi/podcastit/ohjelmat/[-a-zA-Z0-9]+', url)
        or re.match(r'^https?://areena\.yle\.fi/radio/suorat/[-a-zA-Z0-9]+', url)
    ):
        logger.debug(f'{url} is a live radio URL')
        return AreenaLiveRadioExtractor(
            language_chooser, httpclient, title_formatter, ffprobe
        )
    elif re.match(r'^https?://yle\.fi/(a|uutiset|urheilu|saa)/', url):
        logger.debug(f'{url} is a news URL')
        return YleUutisetExtractor(
            language_chooser, httpclient, title_formatter, ffprobe
        )
    elif re.match(r'^https?://(areena|arenan)\.yle\.fi/', url) or re.match(
        r'^https?://yle\.fi/', url
    ):
        logger.debug(f'{url} is an Areena URL')
        return AreenaExtractor(language_chooser, httpclient, title_formatter, ffprobe)
    elif url.lower() in ['tv1', 'tv2', 'teema']:
        logger.debug(f'{url} is a live TV channel')
        return AreenaLiveTVExtractor(
            language_chooser, httpclient, title_formatter, ffprobe
        )
    else:
        logger.debug(f'{url} is an unrecognized URL')
        return None


## Flavors


class Flavors:
    @staticmethod
    def media_type(media):
        mtype = media.get('type')
        if mtype == 'AudioObject' or (
            mtype is None and media.get('containerFormat') == 'mpeg audio'
        ):
            return 'audio'
        else:
            return 'video'


## Clip


@dataclass
class Clip:
    webpage: str
    flavors: list = field(default_factory=list)
    title: str = ''
    episode_title: str = ''
    description: Optional[str] = None
    duration_seconds: Optional[int] = None
    region: str = 'Finland'
    publish_timestamp: Optional[datetime] = None
    expiration_timestamp: Optional[datetime] = None
    subtitles: List = field(default_factory=list)
    program_id: Optional[str] = None
    origin_url: Optional[str] = None

    def metadata(self, io):
        flavors_meta = sorted(
            (self.flavor_meta(f) for f in self.flavors),
            key=lambda x: x.get('bitrate', 0),
        )
        meta = [
            ('program_id', self.program_id),
            ('webpage', self.webpage),
            ('title', self.title),
            ('episode_title', self.episode_title),
            ('description', self.description),
            ('filename', self.meta_file_name(self.flavors, io)),
            ('flavors', flavors_meta),
            ('duration_seconds', self.duration_seconds),
            (
                'subtitles',
                [
                    {'language': x.lang, 'url': x.url, 'category': x.category}
                    for x in self.subtitles
                ],
            ),
            ('region', self.region),
            ('publish_timestamp', self.format_timestamp(self.publish_timestamp)),
            ('expiration_timestamp', self.format_timestamp(self.expiration_timestamp)),
        ]
        return self.ignore_none_values(meta)

    def meta_file_name(self, flavors, io):
        flavors = sorted(flavors, key=lambda x: x.bitrate or 0)
        flavors = [fl for fl in flavors if any(s.is_valid() for s in fl.streams)]
        if flavors:
            extensions = [
                s.file_extension('mkv') for s in flavors[-1].streams if s.is_valid()
            ]
            if extensions:
                return OutputFileNameGenerator().filename(self.title, extensions[0], io)

        return None

    def format_timestamp(self, ts):
        return ts.isoformat() if ts else None

    def flavor_meta(self, flavor):
        if all(not s.is_valid() for s in flavor.streams):
            return self.error_flavor_meta(flavor)
        else:
            return self.valid_flavor_meta(flavor)

    def valid_flavor_meta(self, flavor):
        backends = [s.name for s in flavor.streams if s.is_valid()]

        streams = flavor.streams
        if streams and any(s.is_valid() for s in streams):
            valid_stream = next(s for s in streams if s.is_valid())
            url = valid_stream.stream_url()
        else:
            url = None

        meta = [
            ('media_type', flavor.media_type),
            ('height', flavor.height),
            ('width', flavor.width),
            ('bitrate', flavor.bitrate),
            ('backends', backends),
            ('url', url),
        ]
        return self.ignore_none_values(meta)

    def error_flavor_meta(self, flavor):
        error_messages = [
            s.error_message
            for s in flavor.streams
            if not s.is_valid() and s.error_message
        ]
        if error_messages:
            msg = error_messages[0]
        else:
            msg = 'Unknown error'

        return {'error': msg}

    def ignore_none_values(self, li):
        return {key: value for (key, value) in li if value is not None}


class FailedClip(Clip):
    def __init__(self, webpage, error_message, **kwargs):
        super().__init__(
            webpage=webpage, flavors=[failed_flavor(error_message)], **kwargs
        )


@dataclass(frozen=True)
class AreenaApiProgramInfo:
    media_id: str
    title: str
    episode_title: str
    description: Optional[str]
    flavors: List[StreamFlavor]
    subtitles: List[Subtitle]
    duration_seconds: Optional[int]
    available_at_region: str
    publish_timestamp: Optional[datetime]
    expiration_timestamp: Optional[datetime]
    pending: bool
    expired: bool


@dataclass(frozen=True)
class PlaylistData:
    # The base URL from which to download a playlist
    base_url: str
    # List of query parameters. Each item is a dictionary of query
    # parameters for one season. If empty, a playlist is downloaded
    # from the plain base_url.
    season_parameters: List[Dict]

    def season_playlist_urls(self):
        if self.season_parameters:
            for season_query in self.season_parameters:
                yield update_url_query(self.base_url, season_query)
        else:
            yield self.base_url


@dataclass(frozen=True)
class EpisodeMetadata:
    uri: str
    season_number: Optional[int]
    episode_number: Optional[int]
    release_date: Optional[datetime]

    def sort_key(self):
        return (
            self.season_number or 99999,
            self.episode_number or 99999,
            self.release_date or datetime(1970, 1, 1, 0, 0, 0),
        )

    def with_episode_number(self, ep):
        return EpisodeMetadata(self.uri, self.season_number, ep, self.release_date)


class ClipExtractor:
    def __init__(self, httpclient):
        self.httpclient = httpclient

    def extract(self, url, latest_only):
        playlist = self.get_playlist(url, latest_only)
        return (self.extract_clip(clipurl, url) for clipurl in playlist)

    def get_playlist(self, url, latest_only=False):
        return AreenaPlaylistParser(self.httpclient).get(url, latest_only)

    def extract_clip(self, url, origin_url):
        raise NotImplementedError('extract_clip must be overridden')


class AreenaPlaylistParser:
    """Get a list of episodes in a series from Areena API

    Reference: https://docs.api.yle.fi/api/programs-api-v3
    """

    def __init__(self, httpclient):
        self.httpclient = httpclient

    def get(self, url, latest_only=False):
        """If url is a series page, return a list of included episode pages."""
        tree = self.httpclient.download_html_tree(url)
        if tree is None:
            logger.warning(f'Failed to download {url} while looking for a playlist')
            return [url]

        playlist = []
        playlist_data = None
        if self._is_tv_series_page(tree):
            logger.debug('TV playlist')
            playlist_data = self._parse_series_playlist(tree)
        elif self._is_radio_series_page(tree):
            logger.debug('Radio playlist')
            playlist_data = self._parse_radio_playlist(tree)
        elif self._extract_package_id(tree) is not None:
            logger.debug('Package playlist')
            playlist_data = self._parse_package_playlist(tree)
        else:
            logger.debug('Not a playlist')
            playlist = [url]

        if playlist_data is not None:
            playlist = self._download_playlist_or_latest(playlist_data, latest_only)
            logger.debug(f'playlist page with {len(playlist)} episodes')

        return playlist

    def _is_tv_series_page(self, tree):
        next_data_tag = tree.xpath('//script[@id="__NEXT_DATA__"]')
        if len(next_data_tag) == 0:
            return False

        next_data = json.loads(next_data_tag[0].text)
        ptype = (
            next_data.get('props', {})
            .get('pageProps', {})
            .get('meta', {})
            .get('item', {})
            .get('type')
        )

        return ptype in ['TVSeries', 'TVSeason', 'TVView', 'RadioSeries', 'Package']

    def _is_radio_series_page(self, tree):
        is_radio_page = len(tree.xpath('//div[contains(@class, "RadioPlayer")]')) > 0
        if is_radio_page:
            episode_modal = tree.xpath('//div[starts-with(@class, "EpisodeModal")]')
            play_button = tree.xpath(
                '//main//button[starts-with(@class, "PlayButton")]'
            )
            return not episode_modal and not play_button
        else:
            return False

    def _parse_series_playlist(self, html_tree):
        next_data_tag = html_tree.xpath('//script[@id="__NEXT_DATA__"]')
        if next_data_tag:
            next_data = json.loads(next_data_tag[0].text)
            page_props = next_data.get('props', {}).get('pageProps', {})
            tabs = page_props.get('view', {}).get('tabs', [])
            first_tab_slug = tabs[0].get('slug') if tabs else None
            selected_tab = page_props.get('selectedTab') or first_tab_slug or 'jaksot'
            return self._parse_episodes_tab(
                tabs, selected_tab
            ) or self._parse_episodes_tab(tabs, None)

        return None

    def _parse_episodes_tab(self, next_data_tabs, tab_slug):
        if tab_slug:
            episodes_tab = [
                tab for tab in next_data_tabs if tab.get('slug') == tab_slug
            ]
        else:
            episodes_tab = [
                tab
                for tab in next_data_tabs
                if tab.get('type') == 'tab' and 'title' not in tab
            ]

        if episodes_tab:
            episodes_content = episodes_tab[0].get('content', [])
            if episodes_content:
                playlist_data = episodes_content[0]
                if playlist_data.get('title') not in ['Katso myös', 'Kuuntele myös']:
                    uri = playlist_data.get('source', {}).get('uri')

                    series_parameters = {}
                    filters = playlist_data.get('filters', [])
                    if filters:
                        options = filters[0].get('options', [])
                        series_parameters = [x['parameters'] for x in options]

                    return PlaylistData(uri, series_parameters)

        return None

    def _parse_package_playlist(self, html_tree):
        package_tag = html_tree.xpath('//div[@class="package-view"]/@data-view')
        if package_tag:
            package_data = json.loads(package_tag[0])
            tabs = package_data.get('tabs', [])
            if tabs:
                content = tabs[0].get('content', [])
                if content:
                    uri = content[0].get('source', {}).get('uri')
                    return PlaylistData(uri, [])

        return None

    def _parse_radio_playlist(self, html_tree):
        state_tag = html_tree.xpath(
            '//script[contains(., "window.STORE_STATE_FROM_SERVER")]'
        )
        if state_tag:
            state_str = state_tag[0].text
            data = json.loads(state_str.split('=', 1)[-1].strip())
            tabs = data.get('viewStore', {}).get('viewPageView', {}).get('tabs', [])
            tabs = [t for t in tabs if t.get('title') in ['Jaksot', 'Avsnitt']]
            if tabs:
                all_content = tabs[0].get('allContent')
                if all_content:
                    uri = all_content[0].get('source', {}).get('uri')
                    return PlaylistData(uri, [])

        return None

    def _download_playlist_or_latest(self, playlist_data, latest_only):
        season_urls = list(enumerate(playlist_data.season_playlist_urls(), start=1))
        if latest_only:
            # Optimization: The latest episode belongs to the latest season
            season_urls = season_urls[-1:]

        playlist = self._download_playlist(season_urls)

        # Heuristics: If most episodes do not have an episode number,
        # use time-based sorting.
        if self._episode_numbers_are_rare(playlist) and self._timestamps_are_common(
            playlist
        ):
            playlist = [x.with_episode_number(None) for x in playlist]

        # We can't control whether Areena API returns episodes in
        # ascending or descending order. Additionally, metadata
        # contains only the date (not hours or minutes) so it's not
        # possible to sort intra-day episodes properly. This is a hack
        # that tries to sort intra-day episodes in ascending order.
        # For example: https://areena.yle.fi/1-3863205
        if self._is_descending_date_based_playlist(playlist):
            playlist = reversed(playlist)

        # Sort in ascending order: first by episode number, then by date
        playlist = sorted(playlist, key=lambda x: x.sort_key())

        # The episode API doesn't seem to have any way to download only the
        # latest episode or start from the latest. We need to download all and
        # pick the latest.
        if latest_only:
            playlist = playlist[-1:]

        return [x.uri for x in playlist]

    def _episode_numbers_are_rare(self, playlist):
        num_has_episode = sum(p.episode_number is not None for p in playlist)
        return num_has_episode < 0.5 * len(playlist)

    def _timestamps_are_common(self, playlist):
        num_has_timestamp = sum(p.release_date is not None for p in playlist)
        return num_has_timestamp > 0.8 * len(playlist)

    def _is_descending_date_based_playlist(self, playlist):
        if not all(p.episode_number is None for p in playlist):
            return False

        prev_ts = None
        for p in playlist:
            if (
                prev_ts is not None
                and p.release_date is not None
                and p.release_date < prev_ts
            ):
                return True

            prev_ts = p.release_date

        return False

    def _download_playlist(self, season_urls):
        playlist = []
        for season_num, season_url in season_urls:
            # Areena server fails (502 Bad gateway) if page_size is larger
            # than 100.
            page_size = 100
            offset = 0
            has_next_page = True
            while has_next_page:
                logger.debug(
                    f'Getting a playlist page, season = {season_num}, '
                    f'size = {page_size}, offset = {offset}'
                )

                params = {
                    'offset': str(offset),
                    'limit': str(page_size),
                    'app_id': 'areena-web-items',
                    'app_key': 'wlTs5D9OjIdeS9krPzRQR4I1PYVzoazN',
                }
                playlist_page_url = update_url_query(season_url, params)
                page = self._parse_series_episode_data(playlist_page_url, season_num)

                if page is None:
                    logger.warning(
                        f'Playlist failed at offset {offset}. Some episodes may be missing!'
                    )
                    break

                playlist.extend(page)
                offset += len(page)
                has_next_page = len(page) == page_size

        return playlist

    def _parse_series_episode_data(self, playlist_page_url, season_number):
        playlist = self.httpclient.download_json(playlist_page_url)
        if playlist is None:
            return None

        episodes = []
        for data in playlist.get('data', []):
            uri = self._episode_uri(data)
            episode_number = self._episode_number(data)
            release_date = self._tv_release_date(data) or self._radio_release_date(data)

            if uri:
                episodes.append(
                    EpisodeMetadata(uri, season_number, episode_number, release_date)
                )

        return episodes

    @staticmethod
    def _extract_package_id(tree):
        package_id = tree.xpath('/html/body/@data-package-id')
        if package_id:
            return package_id[0]
        else:
            return None

    @staticmethod
    def _episode_uri(data):
        program_uri = data.get('pointer', {}).get('uri')
        if program_uri:
            media_id = program_uri.rsplit('/')[-1]
            return f'https://areena.yle.fi/{media_id}'
        else:
            return None

    @staticmethod
    def _episode_number(data):
        title = data.get('title')
        if title:
            # Try to parse the episode number from the title. That's the
            # only location where the episode number is available in the
            # API response.
            m = re.match(r'Jakso (\d+)', title, flags=re.IGNORECASE)
            if m:
                return int(m.group(1))

        return None

    def _tv_release_date(self, data):
        labels = data.get('labels')
        generics = self._label_by_type(labels, 'generic', 'formatted')
        for val in generics:
            # Look for a label that matches the format "pe 15.3.2019"
            m = re.match(
                r'[a-z]{2} (?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})', val
            )
            if m:
                return datetime(
                    int(m.group('year')), int(m.group('month')), int(m.group('day'))
                )

        return None

    def _radio_release_date(self, data):
        labels = data.get('labels')
        date_str = self._label_by_type(labels, 'releaseDate', 'raw')
        if date_str:
            try:
                return parse_areena_timestamp(date_str[0])
            except ValueError:
                pass

        return None

    def _label_by_type(self, labels: dict, type_name: str, key_name: str) -> List[str]:
        """Return a key value of an Areena API label object which as the given type."""
        matches = [x for x in labels if x.get('type') == type_name]
        return [x[key_name] for x in matches if key_name in x]


class AreenaPreviewApiParser:
    def __init__(self, data):
        self.preview = data or {}

    def media_id(self):
        ongoing = self.ongoing()
        mid1 = ongoing.get('media_id')
        mid2 = ongoing.get('adobe', {}).get('yle_media_id')
        return mid1 or mid2

    def duration_seconds(self):
        return self.ongoing().get('duration', {}).get('duration_in_seconds')

    def title(self, language_chooser):
        title = {}
        ongoing = self.ongoing()
        title_object = ongoing.get('title', {})
        if title_object:
            title['title'] = language_chooser.choose_long_form(title_object).strip()

        series_title_object = ongoing.get('series', {}).get('title', {})
        if series_title_object:
            title['series_title'] = language_chooser.choose_long_form(
                series_title_object
            ).strip()

        # If title['title'] does not equal title['episode_title'], then
        # the episode title is title['title'].
        #
        # If title['title'] equals title['episode_title'], then either
        # 1. the episode title is the publication date ("pe 16.9.2022"), or
        # 2. the episode title is title['title']
        #
        # It seem impossible to decide which of the cases 1. or 2. should apply
        # based on the preview API response only. We will always use the date
        # (case 1.) because that is the more common case.
        if title.get('title') is not None and title.get('title') == title.get(
            'series_title'
        ):
            title_timestamp = parse_areena_timestamp(ongoing.get('start_time'))
            if title_timestamp:
                # Should be localized (Finnish or Swedish) based on language_chooser
                title['title'] = format_finnish_short_weekday_and_date(title_timestamp)

        return title

    def description(self, language_chooser):
        description_object = self.ongoing().get('description', {})
        if not description_object:
            return None

        description_text = language_chooser.choose_long_form(description_object) or ''
        return description_text.strip()

    def season_and_episode(self):
        res = {}
        episode = self.ongoing().get('episode_number')
        if episode is not None:
            res = {'episode': episode}

            desc = self.description(TranslationChooser(['fin'])) or ''
            m = re.match(r'Kausi (\d+)\b', desc)
            if m:
                res.update({'season': int(m.group(1))})

        return res

    def available_at_region(self):
        return self.ongoing().get('region')

    def timestamp(self):
        if self.is_live():
            return datetime.now().replace(microsecond=0)
        else:
            dt = self.ongoing().get('start_time')
            return parse_areena_timestamp(dt)

    def manifest_url(self):
        return self.ongoing().get('manifest_url')

    def media_url(self):
        return self.ongoing().get('media_url')

    def media_type(self):
        if not self.preview:
            return None
        elif self.ongoing().get('content_type') == 'AudioObject':
            return 'audio'
        else:
            return 'video'

    def is_live(self):
        data = self.preview.get('data', {})
        return 'ongoing_channel' in data or 'ongoing_event' in data

    def is_pending(self):
        data = self.preview.get('data', {})
        pending = data.get('pending_event') or data.get('pending_ondemand')
        return pending is not None

    def is_expired(self):
        data = self.preview.get('data', {})
        return data.get('gone') is not None

    def ongoing(self):
        data = self.preview.get('data', {})
        return (
            data.get('ongoing_ondemand')
            or data.get('ongoing_event', {})
            or data.get('ongoing_channel', {})
            or data.get('pending_event')
            or {}
        )

    def subtitles(self):
        langname2to3 = {
            'fi': 'fin',
            'fih': 'fin',
            'sv': 'swe',
            'svh': 'swe',
            'se': 'smi',
            'en': 'eng',
        }
        hearing_impaired_langs = ['fih', 'svh']

        sobj = self.ongoing().get('subtitles', [])
        subtitles = []
        for s in sobj:
            # Areena has two subtitle objects. The newer object has "language"
            # and "kind" properties. "language" is a three-letter language code.
            lcode_longform = s.get('language', None)
            # The older (not used anymore as of Nov 2023?) format has "lang",
            # which is a two-letter language code with a possible third letter
            # "h" indicating hard-of-hearing subtitles.
            lcode = s.get('lang', None)

            if lcode_longform:
                lang = lcode_longform
                if s.get('kind', None) == 'hardOfHearing':
                    category = 'ohjelmatekstitys'
                else:
                    category = 'käännöstekstitys'
            elif lcode:
                lang = langname2to3.get(lcode, lcode)
                if lcode in hearing_impaired_langs:
                    category = 'ohjelmatekstitys'
                else:
                    category = 'käännöstekstitys'
            else:
                lang = 'unk'
                category = 'käännöstekstitys'
            url = s.get('uri', None)
            if lang and url:
                subtitles.append(Subtitle(url, lang, category))
        return subtitles


### Extract streams from an Areena webpage ###


class AreenaExtractor(ClipExtractor):
    def __init__(self, language_chooser, httpclient, title_formatter, ffprobe):
        super().__init__(httpclient)
        self.language_chooser = language_chooser
        self.title_formatter = title_formatter
        self.ffprobe = ffprobe

    def extract_clip(self, clip_url, origin_url):
        pid = self.program_id_from_url(clip_url)
        program_info = self.program_info_for_pid(
            pid, clip_url, self.title_formatter, self.ffprobe
        )
        return self.create_clip_or_failure(pid, program_info, clip_url, origin_url)

    def program_id_from_url(self, url):
        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query)
        play = query_dict.get('play')
        if parsed.path.startswith('/tv/ohjelmat/') and play:
            return play[0]
        else:
            return parsed.path.split('/')[-1]

    def create_clip_or_failure(self, pid, program_info, url, origin_url):
        if not pid:
            return FailedClip(url, 'Failed to parse a program ID')

        if not program_info:
            return FailedClip(url, 'Failed to download program data', program_id=pid)

        return self.create_clip(pid, program_info, url, origin_url)

    def create_clip(self, program_id, program_info, pageurl, origin_url):
        if program_info.flavors:
            all_streams = list(
                itertools.chain.from_iterable(fl.streams for fl in program_info.flavors)
            )
        else:
            all_streams = []

        if program_info.pending:
            error_message = 'Stream not yet available.'
            if program_info.publish_timestamp:
                error_message = (
                    f'{error_message} Becomes available on '
                    f'{program_info.publish_timestamp.isoformat()}'
                )
        elif program_info.expired:
            error_message = 'This stream has expired'
        elif all_streams and all(not s.is_valid() for s in all_streams):
            error_message = all_streams[0].error_message
        elif not program_info.flavors:
            error_message = 'Media not found'
        else:
            error_message = None

        if error_message:
            return FailedClip(
                webpage=pageurl,
                error_message=error_message,
                title=program_info.title,
                description=program_info.description,
                duration_seconds=program_info.duration_seconds,
                region=program_info.available_at_region,
                publish_timestamp=program_info.publish_timestamp,
                expiration_timestamp=program_info.expiration_timestamp,
                program_id=program_id,
            )
        else:
            return Clip(
                webpage=pageurl,
                flavors=program_info.flavors,
                title=program_info.title,
                episode_title=program_info.episode_title,
                description=program_info.description,
                duration_seconds=program_info.duration_seconds,
                region=program_info.available_at_region,
                publish_timestamp=program_info.publish_timestamp,
                expiration_timestamp=program_info.expiration_timestamp,
                subtitles=program_info.subtitles,
                program_id=program_id,
                origin_url=origin_url,
            )

    def media_flavors(
        self,
        media_id,
        hls_manifest_url,
        download_url,
        media_type,
        is_live,
        pageurl,
        ffprobe,
    ):
        flavors = []

        if download_url:
            flavors.extend(self.download_flavors(download_url, media_type))

        flavors2 = []
        if media_id:
            flavors2.extend(
                self.flavors_by_media_id(media_id, hls_manifest_url, is_live, ffprobe)
            )

        if not flavors2 and hls_manifest_url:
            flavors2.extend(self.hls_flavors(hls_manifest_url, media_type))

        flavors.extend(flavors2)

        if self.is_kaltura_media(media_id):
            # Get mp4 streams (for wget support) from Kaltura if available.
            # Web Areena no longer uses Kaltura, so this may break (Dec 2023).
            flavors.extend(self.kaltura_mp4_flavors(media_id, pageurl))

        return flavors or None

    def flavors_by_media_id(self, media_id, hls_manifest_url, is_live, ffprobe):
        if self.is_full_hd_media(media_id) or is_live:
            logger.debug('Detected a full-HD media')
            flavors = self.hls_probe_flavors(hls_manifest_url, is_live, ffprobe)
            error = [failed_flavor('Manifest URL is missing')]
            return flavors or error
        elif self.is_html5_media(media_id):
            logger.debug('Detected an HTML5 media')
            return self.hls_probe_flavors(hls_manifest_url, False, ffprobe)
        elif self.is_media_67(media_id) or self.is_mp3_podcast(media_id):
            return []
        elif hls_manifest_url:
            # Fall-back options for new media_id types
            logger.debug('Detected a possible HLS media')
            return self.hls_probe_flavors(hls_manifest_url, False, ffprobe)
        else:
            return [failed_flavor('Unknown stream flavor')]

    def kaltura_mp4_flavors(self, media_id, pageurl):
        entry_id = self.kaltura_entry_id(media_id)
        kapi_client = YleKalturaApiClient(self.httpclient)
        playback_context = kapi_client.playback_context(entry_id, pageurl)
        if playback_context:
            return kapi_client.parse_stream_flavors(playback_context, pageurl)
        else:
            return []

    def is_html5_media(self, media_id):
        # 29- is the most common media ID
        # 84-, hosted on yleawsmpondemand-04.akamaized.net, April 2024
        # 85-, ylekvodmod01.akamaized.net, also seen on podcasts, Summer 2024
        return media_id and (
            media_id.startswith('29-')
            or media_id.startswith('84-')
            or media_id.startswith('85-')
        )

    def is_kaltura_media(self, media_id):
        return media_id and media_id.startswith('29-')

    def is_full_hd_media(self, media_id):
        return media_id and media_id.startswith('55-')

    def is_media_67(self, media_id):
        # A new hosting alternative (June 2021)? Hosted on yleawsmpodamdipv4.akamaized.net
        return media_id and media_id.startswith('67-')

    def is_mp3_podcast(self, media_id):
        # Podcast streams, "78-" seen on Spring 2023
        # Prefer download_url, no extra flavors here.
        return media_id and media_id.startswith('78-')

    def is_live_media(self, media_id):
        return media_id and media_id.startswith('10-')

    def kaltura_entry_id(self, mediaid):
        return mediaid.split('-', 1)[-1]

    def hls_flavors(self, hls_manifest_url, media_type):
        if not hls_manifest_url:
            return []

        if media_type == 'video':
            backend = DASHHLSBackend(hls_manifest_url, experimental_subtitles=True)
        else:
            backend = HLSAudioBackend(hls_manifest_url)

        return [StreamFlavor(media_type=media_type, streams=[backend])]

    def hls_probe_flavors(self, hls_manifest_url, is_live, ffprobe):
        if not hls_manifest_url:
            return []

        logger.debug('Probing for stream flavors')
        return FullHDFlavorProber().probe_flavors(hls_manifest_url, is_live, ffprobe)

    def download_flavors(self, download_url, media_type):
        path = urlparse(download_url)[2]
        ext = os.path.splitext(path)[1] or None
        backend = WgetBackend(download_url, ext)
        return [StreamFlavor(media_type=media_type, streams=[backend])]

    def publish_event(self, program_info):
        events = (program_info or {}).get('data', {}).get('publicationEvent', [])
        areena_events = [
            e for e in events if e.get('service', {}).get('id') == 'yle-areena'
        ]
        has_current = any(self.publish_event_is_current(e) for e in areena_events)
        if has_current:
            areena_events = [
                e for e in areena_events if self.publish_event_is_current(e)
            ]

        with_media = [e for e in areena_events if e.get('media')]
        if with_media:
            sorted_events = sorted(
                with_media, key=lambda e: e.get('startTime'), reverse=True
            )
            return sorted_events[0]
        else:
            return {}

    def publish_timestamp(self, program_info):
        ts = self.publish_event(program_info).get('startTime')
        return parse_areena_timestamp(ts)

    def program_info_for_pid(self, pid, pageurl, title_formatter, ffprobe):
        if not pid:
            return None

        preview = self.preview_parser(pid, pageurl)
        publish_timestamp = preview.timestamp()
        titles = preview.title(self.language_chooser)
        title_params = {
            'title': '',
            'program_id': pid,
            'publish_timestamp': publish_timestamp,
        }
        title_params.update(titles)
        season_and_episode = preview.season_and_episode()
        if season_and_episode and 'season' not in season_and_episode:
            logger.debug('Checking the webpage for a season number')
            season_and_episode.update(self.extract_season_number(pageurl))
        title_params.update(season_and_episode)
        title = title_formatter.format(**title_params) or 'areena'
        simple_formatter = TitleFormatter('${series_separator}${title}')
        episode_title = simple_formatter.format(**title_params)
        media_id = preview.media_id()
        is_live = self.is_live_media(media_id) or preview.is_live()
        download_url = self.ignore_invalid_download_url(preview.media_url())
        if self.is_html5_media(media_id):
            preview_subtitles = preview.subtitles()
        else:
            preview_subtitles = []

        return AreenaApiProgramInfo(
            media_id=media_id,
            title=title,
            episode_title=episode_title,
            description=preview.description(self.language_chooser),
            flavors=self.media_flavors(
                media_id,
                preview.manifest_url(),
                download_url,
                preview.media_type(),
                is_live,
                pageurl,
                ffprobe,
            ),
            subtitles=preview_subtitles,
            duration_seconds=preview.duration_seconds(),
            available_at_region=preview.available_at_region() or 'Finland',
            publish_timestamp=publish_timestamp,
            expiration_timestamp=None,
            pending=preview.is_pending(),
            expired=preview.is_expired(),
        )

    def preview_parser(self, pid, pageurl):
        preview_headers = {'Referer': pageurl, 'Origin': 'https://areena.yle.fi'}
        url = self.preview_url(pid)
        try:
            preview_json = self.httpclient.download_json(url, preview_headers)
        except HTTPError as ex:
            if ex.response.status_code == 404:
                logger.warning(f'Preview API result not found: {url}')
                preview_json = []
            else:
                raise
        logger.debug(f'preview data:\n{json.dumps(preview_json, indent=2)}')

        return AreenaPreviewApiParser(preview_json)

    def preview_url(self, program_id):
        return (
            f'https://player.api.yle.fi/v1/preview/{program_id}.json?'
            'language=fin'
            '&ssl=true'
            '&countryCode=FI'
            '&host=areenaylefi'
            '&app_id=player_static_prod'
            '&app_key=8930d72170e48303cf5f3867780d549b'
            '&isPortabilityRegion=true'
        )

    def publish_event_is_current(self, event):
        return event.get('temporalStatus') == 'currently'

    def ignore_invalid_download_url(self, url):
        # Sometimes download url is missing the file name
        return None if (url and url.endswith('/')) else url

    def extract_season_number(self, pageurl):
        # TODO: how to get the season number without downloading the HTML page?
        tree = self.httpclient.download_html_tree(pageurl)
        title_tag = tree.xpath('/html/head/title/text()')
        if len(title_tag) > 0:
            title = title_tag[0]
            m = re.match(r'K(\d+), J\d+', title)
            if m:
                return {'season': int(m.group(1))}

        return {}


### Areena live TV ###


class AreenaLiveTVExtractor(AreenaExtractor):
    def get_playlist(self, url, latest_only=False):
        return [url]

    def program_id_from_url(self, url):
        known_channels = {
            'tv1': 'yle-tv1',
            'tv2': 'yle-tv2',
            'teema': 'yle-teema-fem',
        }

        return known_channels.get(url.lower())


### Areena live radio ###


class AreenaLiveRadioExtractor(AreenaExtractor):
    def get_playlist(self, url, latest_only=False):
        return [url]

    def program_id_from_url(self, url):
        known_channels = {
            '57-p89RepWE0': 'yle-radio-1',
            '57-JAprnp7W2': 'ylex',
            '57-kpDBBz8Pz': 'yle-puhe',
            '57-md5vJP6a2': 'yle-x3m',
            '57-llL6Y4blL': 'yle-klassinen',
            '57-bN8gjw7AY': 'yle-sami-radio',
            # Radio Suomi and Vega have regional channels selected by the query
            # parameter _c. If _c is missing, use these hard coded values.
            '57-3gO4bl7J6': 'yle-radio-suomi-helsinki',
            '57-P3mO0mdm6': 'radio-vega-huvudstadsregionen',
        }

        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query)
        if query_dict.get('_c'):
            return query_dict.get('_c')[0]
        else:
            key = parsed.path.split('/')[-1]
            return known_channels.get(key, key)


### Elava Arkisto ###


class ElavaArkistoExtractor(AreenaExtractor):
    def get_playlist(self, url, latest_only=False):
        ids = self.get_dataids(url)

        if latest_only:
            ids = ids[-1:]

        if ids:
            return [f'https://areena.yle.fi/{x}' for x in ids]
        else:
            # Fallback to Yle news parser because sometimes Elävä
            # arkisto pages are published using the same article type
            # as news articles.
            return parse_playlist_from_yle_article(url, self.httpclient, latest_only)

    def get_dataids(self, url):
        tree = self.httpclient.download_html_tree(url)
        if tree is None:
            return []

        return self.ordered_union(self._simple_dataids(tree), self._ydd_dataids(tree))

    def ordered_union(self, xs, ys):
        union = list(xs)  # copy
        for y in ys:
            if y not in union:
                union.append(y)
        return union

    def _simple_dataids(self, tree):
        dataids = tree.xpath("//article[@id='main-content']//div/@data-id")
        dataids = [str(d) for d in dataids]
        return [d if '-' in d else f'1-{d}' for d in dataids]

    def _ydd_dataids(self, tree):
        player_props = [
            json.loads(p)
            for p in tree.xpath("//main[@id='main-content']//div/@data-player-props")
        ]
        return [x['id'] for x in player_props if 'id' in x]


### News clips at the Yle news site ###


class YleUutisetExtractor(AreenaExtractor):
    def get_playlist(self, url, latest_only=False):
        return parse_playlist_from_yle_article(url, self.httpclient, latest_only)


def parse_playlist_from_yle_article(url, httpclient, latest_only):
    def id_to_areena_url(data_id):
        if '-' in data_id:
            areena_id = data_id
        else:
            areena_id = f'1-{data_id}'
        return f'https://areena.yle.fi/{areena_id}'

    tree = httpclient.download_html_tree(url)
    if tree is None:
        return []

    state = None
    state_script_nodes = tree.xpath(
        '//script[@type="text/javascript" and '
        '(contains(text(), "window.__INITIAL__STATE__") or '
        ' contains(text(), "window.__INITIAL_STATE__"))]/text()'
    )
    if len(state_script_nodes) > 0:
        state_json = re.sub(
            r'^window\.__INITIAL__?STATE__\s*=\s*', '', state_script_nodes[0]
        )
        state = json.loads(state_json)

    if state is None:
        state_div_nodes = tree.xpath('//div[@id="initialState"]')
        if len(state_div_nodes) > 0:
            state = json.loads(state_div_nodes[0].attrib.get('data-state'))

    if state is None:
        return []

    data_ids = []
    article = state.get('pageData', {}).get('article', {})
    if article.get('mainMedia') is not None:
        medias = article['mainMedia']
        data_ids = [
            media['id']
            for media in medias
            if media.get('type') in ['VideoBlock', 'video'] and 'id' in media
        ]
    else:
        headline_video_id = article.get('headline', {}).get('video', {}).get('id')
        if headline_video_id:
            data_ids = [headline_video_id]

    content = article.get('content', [])
    inline_media = [
        block['id']
        for block in content
        if block.get('type') in ['AudioBlock', 'audio', 'VideoBlock', 'video']
        and 'id' in block
    ]
    for id in inline_media:
        if id not in data_ids:
            data_ids.append(id)

    logger.debug(f"Found Areena data IDs: {','.join(data_ids)}")

    playlist = [id_to_areena_url(id) for id in data_ids]
    if latest_only:
        playlist = playlist[-1:]

    return playlist
