import numpy as np
from connect4.policy import Policy
from typing import override


class GroupDPolicy(Policy):

    @override
    def mount(self) -> None:
        pass

    @override
    def act(self, s: np.ndarray) -> int:
        """
        `s` es un array numpy de shape (6, 7)
        s[fila, columna]
        Para saber si una columna está disponible:
        - Si s[0, c] == 0, la columna está libre.
        """
        available_cols = [c for c in range(7) if s[0, c] == 0]

        if not available_cols:
            return 0

        rng = np.random.default_rng()
        return int(rng.choice(available_cols))
