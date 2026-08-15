from common.singleton import SingletonMeta
from models.playlist import Playlist
from models.song import Song


class PlaylistLibrary(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._playlists: dict[str, Playlist] = {}

    @classmethod
    def get_instance(cls) -> "PlaylistLibrary":
        return cls()

    def create_playlist(self, name: str) -> None:
        if name in self._playlists:
            raise ValueError(f'Playlist "{name}" already exists.')
        self._playlists[name] = Playlist(name)

    def get_playlist(self, name: str) -> Playlist:
        if name not in self._playlists:
            raise ValueError(f'Playlist "{name}" not found.')
        return self._playlists[name]

    def add_song_to_playlist(self, playlist_name: str, song: Song) -> None:
        playlist = self.get_playlist(playlist_name)
        playlist.add_song(song)
