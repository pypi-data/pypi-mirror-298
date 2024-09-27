import copy
from typing import Generic, Protocol, Self
from ...traits.with_parts.with_parts import WithParts
from ...core.builderable.types import TBuilderPart, TBuilderOutput


class WithImmutability(
    WithParts[TBuilderOutput, TBuilderPart],
    Generic[TBuilderOutput, TBuilderPart],
    Protocol,
):
    def add_part(self, part: TBuilderPart) -> Self:
        cloned = copy.deepcopy(self)

        cloned.get_parts().append(part)

        return cloned
