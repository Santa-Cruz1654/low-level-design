from device.i_audio_output_device import IAudioOutputDevice
from device.bluetooth_speaker_adapter import BluetoothSpeakerAdapter
from device.headphones_adapter import HeadphonesAdapter
from device.wired_speaker_adapter import WiredSpeakerAdapter
from external.bluetooth_speaker_api import BluetoothSpeakerAPI
from external.headphones_api import HeadphonesAPI
from external.wired_speaker_api import WiredSpeakerAPI
from enums.device_type import DeviceType


class DeviceFactory:
    _creators = {
        DeviceType.BLUETOOTH: lambda: BluetoothSpeakerAdapter(BluetoothSpeakerAPI()),
        DeviceType.WIRED: lambda: WiredSpeakerAdapter(WiredSpeakerAPI()),
        DeviceType.HEADPHONES: lambda: HeadphonesAdapter(HeadphonesAPI()),
    }

    @staticmethod
    def create_device(device_type: DeviceType) -> IAudioOutputDevice:
        creator = DeviceFactory._creators.get(device_type)
        if creator is None:
            raise ValueError(f"Unsupported device type: {device_type}")
        return creator()
