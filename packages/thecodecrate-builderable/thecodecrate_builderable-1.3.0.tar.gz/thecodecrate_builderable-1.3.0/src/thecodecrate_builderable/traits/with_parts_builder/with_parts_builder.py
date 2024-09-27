from abc import abstractmethod
from typing import Generic, Any, Protocol
from ..with_parts.with_parts import WithParts
from ...core.builderable.types import TBuilderPart, TBuilderOutput


class WithPartsBuilder(
    WithParts[TBuilderOutput, TBuilderPart],
    Generic[TBuilderOutput, TBuilderPart],
    Protocol,
):
    @abstractmethod
    def build_parts(
        self,
        *args: Any,
        **kwds: Any,
    ) -> TBuilderOutput:
        pass
