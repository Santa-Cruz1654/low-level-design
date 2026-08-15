from abc import ABC, abstractmethod

from models.song import Song
from models.playlist import Playlist


class PlayStrategy(ABC):
    @abstractmethod
    def set_playlist(self, playlist: Playlist) -> None: ...

    @abstractmethod
    def has_next(self) -> bool: ...

    @abstractmethod
    def next(self) -> Song: ...

    @abstractmethod
    def has_previous(self) -> bool: ...

    @abstractmethod
    def previous(self) -> Song: ...

    def add_to_next(self, song: Song) -> None:
        pass
