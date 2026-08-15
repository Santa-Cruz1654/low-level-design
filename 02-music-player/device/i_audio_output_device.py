from abc import ABC, abstractmethod

from models.song import Song


class IAudioOutputDevice(ABC):
    @abstractmethod
    def play_audio(self, song: Song) -> None: ...
