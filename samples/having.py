from deduct_poc import Effect, Entity, Generic, Rule, StateMachine

# エンティティの定義
takagi = Entity("髙木")
cat = Entity("猫")
marisa = Entity("魔理沙")

# ルールの定義
having_s = Generic("Having S")
having_o = Generic("Having O")
having = Rule("持つ", (having_s, having_o), (), ())

give_x = Generic("Give X")
give_y = Generic("Give Y")
give_o = Generic("Give O")
give = Rule(
    "渡す",
    (give_x, give_y, give_o),
    (Effect(having, {having_s: give_x, having_o: give_o}),),
    (Effect(having, {having_s: give_y, having_o: give_o}),),
)

# 理論の記述
theory = (
    Effect(having, {having_s: takagi, having_o: cat}),
    Effect(give, {give_x: takagi, give_y: marisa, give_o: cat}),
)

# 理論の進行
state_machine = StateMachine(theory)
for effect in state_machine.proceed():
    print(effect)
