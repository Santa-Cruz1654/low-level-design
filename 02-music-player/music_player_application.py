from common.singleton import SingletonMeta
from library.song_library import SongLibrary
from library.playlist_library import PlaylistLibrary
from music_player_facade import MusicPlayerFacade
from models.song import Song
from enums.device_type import DeviceType
from enums.play_strategy_type import PlayStrategyType


class MusicPlayerApplication(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._song_library = SongLibrary.get_instance()
        self._playlist_library = PlaylistLibrary.get_instance()
        self._facade = MusicPlayerFacade.get_instance()

    @classmethod
    def get_instance(cls) -> "MusicPlayerApplication":
        return cls()

    def create_song_in_library(self, title: str, artist: str, path: str) -> None:
        self._song_library.add_song(Song(title, artist, path))

    def create_playlist(self, playlist_name: str) -> None:
        self._playlist_library.create_playlist(playlist_name)

    def add_song_to_playlist(self, playlist_name: str, song_title: str) -> None:
        song = self._song_library.find_by_title(song_title)
        if song is None:
            raise RuntimeError(f'Song "{song_title}" not found in library.')
        self._playlist_library.add_song_to_playlist(playlist_name, song)

    def connect_audio_device(self, device_type: DeviceType) -> None:
        self._facade.connect_device(device_type)

    def select_play_strategy(self, strategy_type: PlayStrategyType) -> None:
        self._facade.set_play_strategy(strategy_type)

    def load_playlist(self, playlist_name: str) -> None:
        self._facade.load_playlist(playlist_name)

    def play_single_song(self, song_title: str) -> None:
        song = self._find_song_or_raise(song_title)
        self._facade.play_song(song)

    def pause_current_song(self, song_title: str) -> None:
        song = self._find_song_or_raise(song_title)
        self._facade.pause_song(song)

    def play_all_tracks_in_playlist(self) -> None:
        self._facade.play_all_tracks()

    def play_next_track_in_playlist(self) -> None:
        self._facade.play_next_track()

    def play_previous_track_in_playlist(self) -> None:
        self._facade.play_previous_track()

    def queue_song_next(self, song_title: str) -> None:
        song = self._find_song_or_raise(song_title)
        self._facade.enqueue_next(song)

    def _find_song_or_raise(self, song_title: str) -> Song:
        song = self._song_library.find_by_title(song_title)
        if song is None:
            raise RuntimeError(f'Song "{song_title}" not found.')
        return song
