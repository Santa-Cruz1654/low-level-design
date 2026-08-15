from device.i_audio_output_device import IAudioOutputDevice
from external.wired_speaker_api import WiredSpeakerAPI
from models.song import Song


class WiredSpeakerAdapter(IAudioOutputDevice):
    def __init__(self, api: WiredSpeakerAPI) -> None:
        self._api = api

    def play_audio(self, song: Song) -> None:
        payload = f"{song.title} by {song.artist}"
        self._api.play_sound_via_cable(payload)
