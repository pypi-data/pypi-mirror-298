from typing import Generic, Protocol, Self
from ...core.builderable.types import TBuilderPart, TBuilderOutput


class WithParts(
    Generic[TBuilderOutput, TBuilderPart],
    Protocol,
):
    _parts: list[TBuilderPart] = []

    def get_parts(self) -> list[TBuilderPart]:
        return self._parts

    def set_parts(self, parts: list[TBuilderPart]) -> Self:
        self._parts = parts

        return self

    def add_part(self, part: TBuilderPart) -> Self:
        self.get_parts().append(part)

        return self
