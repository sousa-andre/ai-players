import copy
from pprint import pprint
from typing import Optional, Tuple

from games.connect4.action import Connect4Action
from games.connect4.player import Connect4Player
from games.connect4.state import Connect4State
from games.state import State


class CustomConnect4Player(Connect4Player):
    def __init__(self, name: str):
        super().__init__(name)

    def _get_other_player_single_move(self, fake_state: Connect4State, row: int, col: int):
        return CustomConnect4Player._get_num_blocks(fake_state, row, col, 0 if self.get_current_pos() == 1 else 1,
                                                    (5, 2, 1,))

    def _get_other_player_score(self, state: Connect4State, my_play: Tuple[int, int]) -> float:
        fake_state = copy.deepcopy(state)
        fake_state.update(Connect4Action(my_play[1]))

        points_to_check = self.get_pos_list(fake_state)
        tmp = []

        biggest = 0
        for point in points_to_check:
            s = self._get_other_player_single_move(fake_state, point[0], point[1])
            tmp.append(s)
            if s > biggest:
                biggest = s

        return biggest

    @staticmethod
    def _get_num_blocks(state: Connect4State, row: int, col: int, choice: int, weights: Tuple[float, float, float]) \
            -> int:
        grid = state.get_grid()
        w = [0, 0, 0, 0]

        # down
        for row_idx in range(row + 1, state.get_num_rows()):
            if grid[row_idx][col] != choice:
                break
            w[0] += 1

        # left
        for col_idx in range(col - 1, -1, -1):
            if grid[row][col_idx] != choice:
                break
            w[1] += 1

        # right
        for col_idx in range(col + 1, state.get_num_cols()):
            if grid[row][col_idx] != choice:
                break
            w[1] += 1

        # top right diag
        for row_idx, col_idx in zip(range(row - 1, -1, -1), range(col + 1, state.get_num_cols())):
            if grid[row_idx][col_idx] != choice:
                break
            w[2] += 1

        # bot left diag
        for row_idx, col_idx in zip(range(row + 1, state.get_num_rows()), range(col - 1, -1, -1)):
            if grid[row_idx][col_idx] != choice:
                break
            w[2] += 1

        # top left diag
        for row_idx, col_idx in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if grid[row_idx][col_idx] != choice:
                break
            w[3] += 1

        # bot right diag
        for row_idx, col_idx in zip(range(row + 1, state.get_num_rows()), range(col + 1, state.get_num_cols())):
            if grid[row_idx][col_idx] != choice:
                break
            w[3] += 1
        s = 0
        for v, in zip(w):
            if v == 3:
                s += v * weights[0]
            elif v == 2:
                s += v * weights[1]
            elif v == 1:
                s += v * weights[2]
        return s

    def _get_num_blocks_defense(self, state: Connect4State, row: int, col: int):
        return CustomConnect4Player._get_num_blocks(state, row, col, self.get_current_pos(), (2, 0.5, 0.01,))

    def _get_num_blocks_attack(self, state: Connect4State, row: int, col: int):
        return CustomConnect4Player._get_num_blocks(state, row, col, 0 if self.get_current_pos() == 1 else 0,
                                                    (float('inf'), 0.5, 0.01,))

    @staticmethod
    def _get_last_for_column(state, col: int) -> Optional[int]:
        grid = state.get_grid()
        num_rows = state.get_num_rows()

        if grid[0][col] != -1:
            return None

        for row_idx in range(num_rows - 1, -1, -1):
            if grid[row_idx][col] == -1:
                return row_idx

    def get_pos_list(self, state: Connect4State):
        d = []
        for col_idx in range(state.get_num_cols()):
            tmp = self._get_last_for_column(state, col_idx)
            if tmp is not None:
                d.append((tmp, col_idx))
        return d

    def get_action(self, state: Connect4State):
        points_to_check = self.get_pos_list(state)

        if (state.get_num_rows()-1, state.get_num_cols()//2) in points_to_check:
            return Connect4Action(state.get_num_cols()//2)

        tmp_point = points_to_check[0]
        tmp_biggest = float('-inf')
        for point in points_to_check:
            a = self._get_num_blocks_defense(state, point[0], point[1]) * 0.7 + \
                self._get_num_blocks_attack(state, point[0], point[1]) * 0.3 \
                - self._get_other_player_score(state, point) * 0.1

            if tmp_biggest < a:
                tmp_biggest = a
                tmp_point = point
        return Connect4Action(tmp_point[1])

    def event_action(self, pos: int, action, new_state: Connect4State):
        pass

    def event_end_game(self, final_state: State):
        pass

