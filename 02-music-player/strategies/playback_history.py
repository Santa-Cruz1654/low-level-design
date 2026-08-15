from models.song import Song


class PlaybackHistory:
    def __init__(self) -> None:
        self._stack: list[Song] = []

    def record(self, song: Song) -> None:
        self._stack.append(song)

    def has_previous(self) -> bool:
        return len(self._stack) > 0

    def pop_previous(self) -> Song:
        if not self.has_previous():
            raise RuntimeError("No previous song available.")
        return self._stack.pop()

    def clear(self) -> None:
        self._stack.clear()
