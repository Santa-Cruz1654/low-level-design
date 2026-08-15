from device.i_audio_output_device import IAudioOutputDevice
from external.headphones_api import HeadphonesAPI
from models.song import Song


class HeadphonesAdapter(IAudioOutputDevice):
    def __init__(self, api: HeadphonesAPI) -> None:
        self._api = api

    def play_audio(self, song: Song) -> None:
        payload = f"{song.title} by {song.artist}"
        self._api.play_sound_via_jack(payload)
