from strategies.play_strategy import PlayStrategy
from models.song import Song
from models.playlist import Playlist


class SequentialPlayStrategy(PlayStrategy):
    def __init__(self) -> None:
        self._current_playlist: Playlist | None = None
        self._current_index: int = -1

    def set_playlist(self, playlist: Playlist) -> None:
        self._current_playlist = playlist
        self._current_index = -1

    def has_next(self) -> bool:
        if self._current_playlist is None:
            return False
        return (self._current_index + 1) < self._current_playlist.size

    def next(self) -> Song:
        if not self.has_next():
            raise RuntimeError("No next song available.")
        self._current_index += 1
        return self._current_playlist.songs[self._current_index]

    def has_previous(self) -> bool:
        if self._current_playlist is None:
            return False
        return (self._current_index - 1) >= 0

    def previous(self) -> Song:
        if not self.has_previous():
            raise RuntimeError("No previous song available.")
        self._current_index -= 1
        return self._current_playlist.songs[self._current_index]
