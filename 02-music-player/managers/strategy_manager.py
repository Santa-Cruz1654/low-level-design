from common.singleton import SingletonMeta
from strategies.play_strategy import PlayStrategy
from strategies.sequential_play_strategy import SequentialPlayStrategy
from strategies.random_play_strategy import RandomPlayStrategy
from strategies.custom_queue_strategy import CustomQueueStrategy
from enums.play_strategy_type import PlayStrategyType


class StrategyManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._strategies: dict[PlayStrategyType, PlayStrategy] = {
            PlayStrategyType.SEQUENTIAL: SequentialPlayStrategy(),
            PlayStrategyType.RANDOM: RandomPlayStrategy(),
            PlayStrategyType.CUSTOM_QUEUE: CustomQueueStrategy(),
        }

    @classmethod
    def get_instance(cls) -> "StrategyManager":
        return cls()

    def get_strategy(self, strategy_type: PlayStrategyType) -> PlayStrategy:
        return self._strategies[strategy_type]
