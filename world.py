class World:
    def __init__(self, rows: int, cols: int):
        self._energy_rate: int = 10  # how much can be absorbed per cycle
        self._world: list[list[object]] = \
            [[None for _ in range(cols)] for _ in range(rows)]

    def kill_organism(self, row: int, col: int) -> None:
        """Sets the row col to None"""
        self._world[row][col] = None

    def move(self, rowA: int, colA: int, rowB: int, colB: int) -> None:
        """Moves the organism from a to b"""
        if rowA == rowB and colA == colB:
            return
        self._world[rowB][colB] = self._world[rowA][colA]
        self._world[rowA][colA] = None

    def add_organism(self, organism, row: int, col :int) -> None:
        """Adds the organism to self._world"""
        self._world[row][col] = organism

    def is_cell_empty(self, row: int, col: int) -> bool:
        """Returns if the world contains an object at row, col"""
        return self._world[row][col] is None

    def get_cell(self, row: int, col: int):
        """Returns the object in the world at row, col"""
        return self._world[row][col]

    def get_world(self) -> list[list[object]]:
        """Returns the 2d world array"""
        return self._world

    def get_empty_neighbor(self, row: int, col: int) -> (bool, int, int):
        """
        Returns the first empty neighbor cell if there is one
        bool- for if there is an empty neighbor, int for row, int for col
        """
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, -1), (1, 0), (1, 1)]

        for r, c in neighbors:
            check_row, check_col = r + row, c + col
            if (check_row < 0 or check_row >= len(self._world) or
                    check_col < 0 or check_col >= len(self._world[0])):
                continue

            if not self._world[check_row][check_col]:
                return True, check_row, check_col
        return False, 0, 0