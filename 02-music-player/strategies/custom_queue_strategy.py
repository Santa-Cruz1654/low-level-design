from collections import deque

from strategies.play_strategy import PlayStrategy
from strategies.playback_history import PlaybackHistory
from models.song import Song
from models.playlist import Playlist


class CustomQueueStrategy(PlayStrategy):
    def __init__(self) -> None:
        self._current_playlist: Playlist | None = None
        self._current_index: int = -1
        self._next_queue: deque[Song] = deque()
        self._history = PlaybackHistory()
        self._position_by_song_id: dict[int, int] = {}

    def set_playlist(self, playlist: Playlist) -> None:
        self._current_playlist = playlist
        self._current_index = -1
        self._next_queue.clear()
        self._history.clear()
        self._position_by_song_id = (
            {id(song): idx for idx, song in enumerate(playlist.songs)}
            if playlist else {}
        )

    def has_next(self) -> bool:
        if self._current_playlist is None:
            return False
        sequential_has_next = (self._current_index + 1) < self._current_playlist.size
        return len(self._next_queue) > 0 or sequential_has_next

    def next(self) -> Song:
        if not self.has_next():
            raise RuntimeError("No next song available.")

        if self._next_queue:
            song = self._next_queue.popleft()
            self._current_index = self._position_by_song_id[id(song)]
        else:
            song = self._next_sequential()

        self._history.record(song)
        return song

    def has_previous(self) -> bool:
        return self._history.has_previous()

    def previous(self) -> Song:
        song = self._history.pop_previous()
        self._current_index = self._position_by_song_id[id(song)]
        return song

    def add_to_next(self, song: Song) -> None:
        if song is None:
            raise ValueError("Cannot enqueue None as a song.")
        self._next_queue.append(song)

    def _next_sequential(self) -> Song:
        self._current_index += 1
        return self._current_playlist.songs[self._current_index]
