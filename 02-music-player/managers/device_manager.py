from common.singleton import SingletonMeta
from device.i_audio_output_device import IAudioOutputDevice
from factories.device_factory import DeviceFactory
from enums.device_type import DeviceType


class DeviceManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._current_output_device: IAudioOutputDevice | None = None

    @classmethod
    def get_instance(cls) -> "DeviceManager":
        return cls()

    def connect(self, device_type: DeviceType) -> None:
        self._current_output_device = DeviceFactory.create_device(device_type)
        print(f"{device_type.name.title()} device connected")

    def get_output_device(self) -> IAudioOutputDevice:
        if self._current_output_device is None:
            raise RuntimeError("No output device is connected.")
        return self._current_output_device

    def has_output_device(self) -> bool:
        return self._current_output_device is not None
