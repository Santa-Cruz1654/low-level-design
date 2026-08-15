from common.singleton import SingletonMeta
from models.song import Song


class SongLibrary(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._songs: list[Song] = []

    @classmethod
    def get_instance(cls) -> "SongLibrary":
        return cls()

    def add_song(self, song: Song) -> None:
        if song is None:
            raise ValueError("Cannot add None to library.")
        self._songs.append(song)

    def find_by_title(self, title: str) -> Song | None:
        for song in self._songs:
            if song.title == title:
                return song
        return None
