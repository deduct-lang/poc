from __future__ import annotations

__all__ = (
    "DeductError",
    "NoPremiseBoundingError",
    "ValidationError",
)

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from deduct_poc.effect import Effect


class DeductError(Exception):
    """このライブラリで起きたエラー全般を示す。"""


class NoPremiseBoundingError(DeductError):
    """演繹進行中、ステートマシンが前提を満たさないエフェクトに遭遇した際のエラー。"""

    def __init__(self, effect: Effect, premise: Effect) -> None:
        super().__init__(
            "エフェクトの前提をステートマシンは満たしていません。\n\n"
            f"エフェクト: {effect}\n前提: {premise}"
        )

        self.effect = effect
        self.premise = premise


class ValidationError(DeductError):
    """演繹進行中、ステートマシンが前提または結論の検証に失敗した際のエラー。"""

    def __init__(
        self,
        mode: Literal["前提", "結論"],
        effect: Effect,
        incoming: Effect,
    ) -> None:
        super().__init__(
            f"エフェクトの{mode}の検証中にエラーが発生しました。\n\n"
            f"エフェクト: {effect}\n{mode}: {incoming}"
        )

        self.effect = effect
        self.incoming = incoming
