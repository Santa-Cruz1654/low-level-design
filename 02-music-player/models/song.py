from dataclasses import dataclass


@dataclass(frozen=True)
class Song:
    title: str
    artist: str
    file_path: str
