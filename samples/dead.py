from deduct_poc import Effect, Entity, Generic, Rule, StateMachine

# エンティティの定義
socrates = Entity("ソクラテス")
human = Entity("人間")

# ルールの定義
is_s = Generic("Is S")
s_is_human = Rule("人間である", (is_s, human), (), ())

die_s = Generic("Die S")
die = Rule(
    "死ぬ",
    (die_s,),
    (Effect(s_is_human, {is_s: die_s}),),
    (),
)

# 理論の記述
theory = (
    Effect(s_is_human, {is_s: socrates}),
    Effect(die, {die_s: socrates}),
)

# 理論の進行
state_machine = StateMachine(theory)
for effect in state_machine.proceed():
    print(effect)
