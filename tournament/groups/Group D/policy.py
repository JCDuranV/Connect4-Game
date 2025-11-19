import numpy as np
from connect4.policy import Policy
from typing import override

ROWS = 6
COLS = 7


class GroupDPolicy(Policy):

    @override
    def mount(self) -> None:
        pass

    def can_play(self, s, col):
        return s[0, col] == 0

    def next_state(self, s, col, player):
        """Devuelve un nuevo tablero tras poner la ficha."""
        new_s = s.copy()
        for r in range(ROWS - 1, -1, -1):
            if new_s[r, col] == 0:
                new_s[r, col] = player
                break
        return new_s

    def check_win(self, s, player):
        """Detectar si player ya ganó."""
        # horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(s[r, c+i] == player for i in range(4)):
                    return True

        # vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(s[r+i, c] == player for i in range(4)):
                    return True

        # diag /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(s[r-i, c+i] == player for i in range(4)):
                    return True

        # diag \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(s[r+i, c+i] == player for i in range(4)):
                    return True

        return False

    @override
    def act(self, s: np.ndarray) -> int:
        player = 1
        opponent = -1

        legal = [c for c in range(COLS) if self.can_play(s, c)]

        # 1️⃣ Si podemos GANAR, ganemos
        for c in legal:
            new_s = self.next_state(s, c, player)
            if self.check_win(new_s, player):
                return c

        # 2️⃣ Si el rival puede ganar, BLOQUEARLO
        for c in legal:
            new_s = self.next_state(s, c, opponent)
            if self.check_win(new_s, opponent):
                return c

        # 3️⃣ Preferir el centro
        if 3 in legal:
            return 3

        # 4️⃣ Si no, una columna medianamente buena
        for c in [2, 4, 1, 5, 0, 6]:
            if c in legal:
                return c

        return legal[0]