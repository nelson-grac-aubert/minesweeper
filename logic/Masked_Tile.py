from __future__ import annotations
from typing import TYPE_CHECKING

from logic.Tile import Tile

if TYPE_CHECKING:
    from logic.Board import Board


class Masked_Tile(Tile):
    """
    Case non révélée sans marquage.
    Un clic gauche déclenche la révélation récursive (ou la défaite si mine).
    Un clic droit pose un drapeau.
    """

    def __init__(self, row: int, col: int):
        super().__init__(row, col)

    #  actions

    def on_left_click(self, board: "Board") -> bool:
        """
        Si la case est une mine → défaite (True).
        Sinon lance la révélation récursive depuis cette case.
        """
        if board.is_mine(self._row, self._col):
            return True  # mine touchée

        self.reveal_recursive(board)
        return False

    def on_right_click(self, board: "Board") -> "Tile":
        """Pose un drapeau : Masked → Masked_Bomb_Tile."""
        from logic.Masked_Bomb_Tile import Masked_Bomb_Tile
        return Masked_Bomb_Tile(self._row, self._col)

    def __repr__(self):
        return f"Masked_Tile({self._row}, {self._col})"