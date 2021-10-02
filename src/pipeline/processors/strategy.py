from typing import Optional, List

from entities.candle import Candle
from entities.strategy import Strategy
from entities.strategy_signal import StrategySignal
from pipeline.processor import Processor
from pipeline.shared_context import SharedContext
from trade.signals_executor import SignalsExecutor


class StrategyProcessor(Processor):
    def __init__(self, strategies: List[Strategy], signals_executor: SignalsExecutor,
                 next_processor: Optional[Processor]) -> None:
        super().__init__(next_processor)
        self.signals_executor = signals_executor
        self.strategies = strategies

    def process(self, context: SharedContext, candle: Candle):
        signals: List[StrategySignal] = []
        for strategy in self.strategies:
            signals += strategy.process(context, candle) or []

        if signals:
            self.signals_executor.execute(signals)

        if self.next_processor:
            self.next_processor.process(context, candle)