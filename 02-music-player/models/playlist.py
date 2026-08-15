from dataclasses import dataclass, field

from models.song import Song


@dataclass
class Playlist:
    name: str
    _songs: list[Song] = field(default_factory=list)

    def add_song(self, song: Song) -> None:
        if song is None:
            raise ValueError("Cannot add None to playlist.")
        self._songs.append(song)

    @property
    def songs(self) -> list[Song]:
        return self._songs.copy()

    @property
    def size(self) -> int:
        return len(self._songs)
