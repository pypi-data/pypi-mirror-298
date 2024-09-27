import pytest

from .stubs.custom_arg_builder import CustomArgBuilder
from .stubs.custom_list_builder import MyCustomListBuilder
from .stubs.stub_builder import StubBuilder
from .stubs.mutable_builder import MutableBuilder
from .stubs.immutable_builder import ImmutableBuilder


@pytest.mark.asyncio
async def test_builderable():
    builder = (StubBuilder()).add_part(1).add_part(2).add_part(3)

    assert builder.build_parts() == "StubBuilder built with parts: [1, 2, 3]"


@pytest.mark.asyncio
async def test_custom_list_builder():
    my_builder = (MyCustomListBuilder()).add(1).add(2).add(3)

    assert my_builder.custom_parts == [1, 2, 3]
    assert my_builder.build() == "Built with custom parts: [1, 2, 3]"


@pytest.mark.asyncio
async def test_custom_arguments():
    custom_arg_builder = (
        (CustomArgBuilder()).add_part(1).add_part(2).add_part(3)
    )

    assert custom_arg_builder.build_parts(5) == "Result is 11"


@pytest.mark.asyncio
async def test_add_after_build():
    builder = (MutableBuilder()).add(1).add(2).add(3)

    assert builder.custom_parts == [1, 2, 3]
    assert builder.build(0) == "result is 6"
    assert builder.add(4).custom_parts == [1, 2, 3, 4]
    assert builder.build(5) == "result is 15"


@pytest.mark.asyncio
async def test_new_instances_dont_share_parts():
    builder1 = (MutableBuilder()).add(1).add(2).add(3)
    assert builder1.custom_parts == [1, 2, 3]
    assert builder1.build(0) == "result is 6"

    builder2 = (MutableBuilder()).add(4).add(5).add(6)
    assert builder2.custom_parts == [4, 5, 6]
    assert builder2.build(0) == "result is 15"


@pytest.mark.asyncio
async def test_inheritance():
    class SubBuilder(MutableBuilder):
        def build(self, payload: int) -> str:
            result = payload + sum(self.custom_parts)

            return f"sub result is {result}"

    builder = (SubBuilder()).add(1).add(2).add(3)
    assert builder.custom_parts == [1, 2, 3]
    assert builder.build(0) == "sub result is 6"
    assert builder.add(4).custom_parts == [1, 2, 3, 4]
    assert builder.build(5) == "sub result is 15"


@pytest.mark.asyncio
async def test_immutability():
    builder = (ImmutableBuilder()).add(1).add(2).add(3)
    builder2 = builder.add(4)

    assert builder.custom_parts == [1, 2, 3]
    assert builder2.custom_parts == [1, 2, 3, 4]

    assert builder.build(5) == "result is 11"
    assert builder2.build(5) == "result is 15"


@pytest.mark.asyncio
async def test_mutability():
    builder = (MutableBuilder()).add(1).add(2).add(3)
    builder2 = builder.add(4)

    assert builder.custom_parts == [1, 2, 3, 4]
    assert builder2.custom_parts == [1, 2, 3, 4]
