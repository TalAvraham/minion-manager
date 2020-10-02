"""
    Author  : Tal Avraham
    Created : 7/11/2020
    Purpose : Minecraft chest handler.
"""

import config
from typing import Tuple


class Chest:
    SLOTS_DISTANCE = 38

    def __init__(self,
                 top_left_slot: Tuple[int, int],
                 rows: int,
                 slots_per_row: int):
        self._rows = rows
        self._slots_per_row = slots_per_row
        self._total_number_of_slots = self._rows * self._slots_per_row
        self._top_left_slot = top_left_slot

    def get_slot_coordinates(self, chest_slot: int):
        self._validate_chest_slot(chest_slot)
        return self._calc_chest_slot_coordinates(chest_slot)

    def _validate_chest_slot(self, chest_slot: int):
        if not str(chest_slot).isnumeric():
            raise ValueError("Given chest slot string is not numeric.")
        if not (0 <= chest_slot <= (self._total_number_of_slots - 1)):
            raise ValueError("Chest slot number out of range.")

    def _calc_chest_slot_coordinates(self, chest_slot: int):
        row = int(chest_slot / self._slots_per_row)
        column = chest_slot % self._slots_per_row
        x = self._top_left_slot[0] + (column * self.SLOTS_DISTANCE)
        y = self._top_left_slot[1] + (row * self.SLOTS_DISTANCE)
        return x, y


class SmallChest(Chest):
    ROWS = 3
    SLOT_PER_ROW = 9

    def __init__(self):
        super().__init__(config.SMALL_CHEST_TOP_LEFT_SLOT,
                         self.ROWS,
                         self.SLOT_PER_ROW)
