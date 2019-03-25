from src.battle.battle_manager import BattleManager


class BattleManagerMock(BattleManager):

    def __init__(self):
        super().__init__(None)