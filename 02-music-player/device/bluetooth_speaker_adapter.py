from device.i_audio_output_device import IAudioOutputDevice
from external.bluetooth_speaker_api import BluetoothSpeakerAPI
from models.song import Song


class BluetoothSpeakerAdapter(IAudioOutputDevice):
    def __init__(self, api: BluetoothSpeakerAPI) -> None:
        self._api = api

    def play_audio(self, song: Song) -> None:
        payload = f"{song.title} by {song.artist}"
        self._api.play_sound_via_bluetooth(payload)
