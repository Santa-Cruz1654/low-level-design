from models.song import Song
from device.i_audio_output_device import IAudioOutputDevice


class AudioEngine:
    def __init__(self) -> None:
        self._current_song: Song | None = None
        self._is_paused: bool = False

    @property
    def current_song(self) -> Song | None:
        return self._current_song

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    def is_currently_playing(self, song: Song) -> bool:
        return self._current_song is song

    def play(self, device: IAudioOutputDevice, song: Song) -> None:
        if song is None:
            raise ValueError("Cannot play a null song.")

        if self._is_paused and song is self._current_song:
            self._is_paused = False
            print(f"Resuming song: {song.title}")
            device.play_audio(song)
            return

        self._current_song = song
        self._is_paused = False
        print(f"Playing song: {song.title}")
        device.play_audio(song)

    def pause(self) -> None:
        if self._current_song is None:
            raise RuntimeError("No song is currently playing to pause.")
        if self._is_paused:
            raise RuntimeError("Song is already paused.")

        self._is_paused = True
        print(f"Pausing song: {self._current_song.title}")
