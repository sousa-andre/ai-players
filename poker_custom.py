from typing import Tuple

import random

from games.poker.action import KuhnPokerAction
from games.poker.card import KuhnPokerCard
from games.poker.player import KuhnPokerPlayer
from games.poker.state import KuhnPokerState
from games.state import State

choices = {
    None: {
        KuhnPokerCard.King: (
            (KuhnPokerAction.BET, 0.8),
            (KuhnPokerAction.PASS, 0.2)
        ),
        KuhnPokerCard.Queen: (
            (KuhnPokerAction.BET, 0.5),
            (KuhnPokerAction.PASS, 0.5)
        ),
        KuhnPokerCard.Jack: (
            (KuhnPokerAction.BET, 0.05),
            (KuhnPokerAction.PASS, 0.95)
        )
    },
    KuhnPokerAction.BET: {
        KuhnPokerCard.King: (
            (KuhnPokerAction.BET, 0.99),
            (KuhnPokerAction.PASS, 0.01)
        ),
        KuhnPokerCard.Queen: (
            (KuhnPokerAction.BET, 0.2),
            (KuhnPokerAction.PASS, 0.8)
        ),
        KuhnPokerCard.Jack: (
            (KuhnPokerAction.BET, 0.01),
            (KuhnPokerAction.PASS, 0.99),
        )
    },
    KuhnPokerAction.PASS: {
        KuhnPokerCard.King: (
            (KuhnPokerAction.BET, 0.99),
            (KuhnPokerAction.PASS, 0.01)
        ),
        KuhnPokerCard.Queen: (
            (KuhnPokerAction.BET, 0.7),
            (KuhnPokerAction.PASS, 0.3)
        ),
        KuhnPokerCard.Jack: (
            (KuhnPokerAction.BET, 0.2),
            (KuhnPokerAction.PASS, 0.8)
        )
    }
}


class CustomKuhnPokerPlayer(KuhnPokerPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.__enemy_action = None

    @staticmethod
    def __randomize_action(options: Tuple[Tuple[KuhnPokerAction, float], Tuple[KuhnPokerAction, float]]):
        return random.choices([options[0][0], options[1][0]], weights=[options[0][1], options[1][1]], k=1)[0]

    def get_action(self, state: KuhnPokerState):
        if self.get_current_pos() == 0:
            return self.__randomize_action(choices[None][self.get_current_card()])
        else:
            return self.__randomize_action(choices[self.__enemy_action][self.get_current_card()])

    def event_action(self, pos: int, action: KuhnPokerAction, new_state: KuhnPokerState):
        if self.get_current_pos() != pos:
            self.__enemy_action = action

    def event_end_game(self, final_state: State):
        pass

