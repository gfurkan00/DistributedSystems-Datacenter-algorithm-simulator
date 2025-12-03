from typing import Dict, Type

from .topology_strategy import TopologyStrategy


class TopologyBuilderFactory:
    _STRATEGIES: Dict[str, Type[TopologyStrategy]] = {}

    @classmethod
    def register(cls, name: str, strategy: Type[TopologyStrategy]):
        cls._STRATEGIES[name] = strategy

    @classmethod
    def get_strategy(cls, protocol_name: str) -> TopologyStrategy:
        strategy_class = cls._STRATEGIES.get(protocol_name)
        if not strategy_class:
            raise ValueError(f"No topology strategy found for protocol: {protocol_name}")
        return strategy_class()