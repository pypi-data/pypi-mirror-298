from abc import ABC
from typing import Generic
from ...traits.with_parts_builder.with_parts_builder import WithPartsBuilder
from ...traits.with_parts.with_parts import WithParts
from .types import TBuilderOutput, TBuilderPart


class Builderable(
    WithPartsBuilder[TBuilderOutput, TBuilderPart],
    WithParts[TBuilderOutput, TBuilderPart],
    Generic[TBuilderOutput, TBuilderPart],
    ABC,
):
    def __init__(self) -> None:
        self.set_parts([])
