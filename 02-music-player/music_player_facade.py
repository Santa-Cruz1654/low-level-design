from common.singleton import SingletonMeta
from core.audio_engine import AudioEngine
from managers.device_manager import DeviceManager
from managers.strategy_manager import StrategyManager
from library.playlist_library import PlaylistLibrary
from models.playlist import Playlist
from models.song import Song
from enums.device_type import DeviceType
from enums.play_strategy_type import PlayStrategyType
from strategies.play_strategy import PlayStrategy


class MusicPlayerFacade(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._audio_engine = AudioEngine()
        self._loaded_playlist: Playlist | None = None
        self._play_strategy: PlayStrategy | None = None

    @classmethod
    def get_instance(cls) -> "MusicPlayerFacade":
        return cls()

    def connect_device(self, device_type: DeviceType) -> None:
        DeviceManager.get_instance().connect(device_type)

    def set_play_strategy(self, strategy_type: PlayStrategyType) -> None:
        self._play_strategy = StrategyManager.get_instance().get_strategy(strategy_type)

    def load_playlist(self, name: str) -> None:
        if self._play_strategy is None:
            raise RuntimeError("Play strategy not set before loading.")

        self._loaded_playlist = PlaylistLibrary.get_instance().get_playlist(name)
        self._play_strategy.set_playlist(self._loaded_playlist)

    def play_song(self, song: Song) -> None:
        if not DeviceManager.get_instance().has_output_device():
            raise RuntimeError("No audio device connected.")

        device = DeviceManager.get_instance().get_output_device()
        self._audio_engine.play(device, song)

    def pause_song(self, song: Song) -> None:
        if not self._audio_engine.is_currently_playing(song):
            raise RuntimeError(f'Cannot pause "{song.title}"; not currently playing.')
        self._audio_engine.pause()

    def play_all_tracks(self) -> None:
        if self._loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        while self._play_strategy.has_next():
            next_song = self._play_strategy.next()
            device = DeviceManager.get_instance().get_output_device()
            self._audio_engine.play(device, next_song)

        print(f"Completed playlist: {self._loaded_playlist.name}")

    def play_next_track(self) -> None:
        if self._loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        if self._play_strategy.has_next():
            next_song = self._play_strategy.next()
            device = DeviceManager.get_instance().get_output_device()
            self._audio_engine.play(device, next_song)
        else:
            print(f"Completed playlist: {self._loaded_playlist.name}")

    def play_previous_track(self) -> None:
        if self._loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        if self._play_strategy.has_previous():
            prev_song = self._play_strategy.previous()
            device = DeviceManager.get_instance().get_output_device()
            self._audio_engine.play(device, prev_song)
        else:
            print(f"Completed playlist: {self._loaded_playlist.name}")

    def enqueue_next(self, song: Song) -> None:
        if self._play_strategy is None:
            raise RuntimeError("No play strategy set.")
        self._play_strategy.add_to_next(song)
