from typing import Generic, Protocol
from ...traits.with_parts.with_parts import WithParts
from .types import TBuilderOutput, TBuilderPart


class Builderable(
    WithParts[TBuilderOutput, TBuilderPart],
    Generic[TBuilderOutput, TBuilderPart],
    Protocol,
):
    def __init__(self) -> None:
        self.set_parts([])
