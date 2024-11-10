from __future__ import annotations

__all__ = ("Effect",)

from copy import copy
from dataclasses import dataclass
from typing import Self

from deduct_poc.entity import Entity
from deduct_poc.rule import Arg, Generic, Rule


@dataclass
class Effect:
    """ルールの具体例

    Raises:
        ValueError:
            渡された値が間違っている場合に送出されます。
            例：使われていないジェネリックの関連付けを指定する。
    """

    rule: Rule
    "このエフェクトが具現化している対象のルール"
    associated: dict[Generic, Arg]
    "ジェネリックとの関連付け"

    def __post_init__(self) -> None:
        for generic in self.associated.keys():
            if generic not in self.rule.args:
                raise ValueError(
                    f"関連付けに使われたジェネリック「{generic}」はこのエフェクトに使われていません。"
                )

    def hydrate(self, associated: dict[Generic, Arg]) -> Self:
        """渡された関連付けをこのエフェクトに適用します。

        Raises:
            ValueError:
                このエフェクトに使われていないジェネリックを使うと発生します。
        """
        for incoming_generic, incoming_arg in associated.items():
            for own_generic, own_arg in self.associated.items():
                if incoming_generic == own_arg:
                    self.associated[own_generic] = incoming_arg
                    break

        return self

    def copy(self) -> Self:
        return copy(self)

    def is_bounded(self, effect: Effect) -> bool:
        """渡されたエフェクトが、自身の引数に束縛されているかを求めます。

        このメソッドは、渡されたエフェクトの前提と結論が自身と一緒か確認し、
        そして渡されたエフェクトの引数がジェネリック以外一致しているかを確認します。
        その状況はジェネリック以外が一致しているため、ジェネリック以外の部分で
        束縛されているといえるでしょう。
        """
        if effect.rule != self.rule:
            return False

        for key, value in effect.associated.items():
            current = self.associated[key]

            match current:
                case Entity() if current != value:
                    return False
                case Generic():
                    continue

        return True
