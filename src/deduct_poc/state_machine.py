__all__ = ("StateMachine",)

from collections import deque
from collections.abc import Iterable

from deduct_poc.effect import Effect
from deduct_poc.error import NoPremiseBoundingError, ValidationError


class StateMachine:
    """理論を検証および進行し結論を出すステートマシン"""

    def __init__(
        self, theory: Iterable[Effect], *, initial_state: list[Effect] | None = None
    ) -> None:
        self.theory = deque(theory)

        self.state = [] if initial_state is None else initial_state

    def proceed_once(self) -> None:
        head = self.theory.popleft()

        # 前提の検証と削除
        for premise in head.rule.premise:
            try:
                premise = premise.copy().hydrate(head.associated)
            except ValueError as e:
                raise ValidationError("前提", head, premise) from e

            for i, effect in enumerate(self.state):
                if premise.is_bounded(effect):
                    del self.state[i]
                    break
            else:
                raise NoPremiseBoundingError(head, premise)

        # 結論への状態遷移
        if not head.rule.conclusion:
            # もし結論が空なら、自分を結論とする。
            self.state.append(head)

        for conclusion in head.rule.conclusion:
            try:
                conclusion = conclusion.copy().hydrate(head.associated)
            except ValueError as e:
                raise ValidationError("結論", head, conclusion) from e

            self.state.append(conclusion)

    def proceed(self) -> list[Effect]:
        while self.theory:
            self.proceed_once()

        return self.state
