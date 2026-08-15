import random

from strategies.play_strategy import PlayStrategy
from strategies.playback_history import PlaybackHistory
from models.song import Song
from models.playlist import Playlist


class RandomPlayStrategy(PlayStrategy):
    def __init__(self) -> None:
        self._current_playlist: Playlist | None = None
        self._remaining_songs: list[Song] = []
        self._history = PlaybackHistory()

    def set_playlist(self, playlist: Playlist) -> None:
        self._current_playlist = playlist
        self._remaining_songs = list(playlist.songs) if playlist else []
        self._history.clear()

    def has_next(self) -> bool:
        return self._current_playlist is not None and len(self._remaining_songs) > 0

    def next(self) -> Song:
        if not self.has_next():
            raise RuntimeError("No next song available.")

        idx = random.randrange(len(self._remaining_songs))
        selected_song = self._remaining_songs[idx]

        last_index = len(self._remaining_songs) - 1
        self._remaining_songs[idx] = self._remaining_songs[last_index]
        self._remaining_songs.pop()

        self._history.record(selected_song)
        return selected_song

    def has_previous(self) -> bool:
        return self._history.has_previous()

    def previous(self) -> Song:
        return self._history.pop_previous()
