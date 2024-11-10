from __future__ import annotations

__all__ = ("Generic", "Rule")

from collections.abc import Hashable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deduct_poc.effect import Effect
    from deduct_poc.entity import Entity


@dataclass
class Generic(Hashable):
    """何らかのエンティティを表現するジェネリック"""

    name: str

    def __hash__(self) -> int:
        return id(self)


type Arg = Generic | Entity


@dataclass
class Rule:
    """状態遷移の方法を定義したルール"""

    name: str
    args: tuple[Arg, ...]
    premise: tuple[Effect, ...]
    conclusion: tuple[Effect, ...]
