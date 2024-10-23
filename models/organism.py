class Organism:
    def __init__(self, genome, row: int, col: int, world):
        self._genome = genome
        self._energy: int = self._genome.get_max_energy()
        self._row: int = row
        self._col: int = col
        self._world = world
        # Custom / Organism-Specific Properties
        self._move_energy_expenditure = 1   # Energy spend moving
        self._food_energy = 1               # Energy given when eaten
        self._base_energy_expenditure = 1   # Baseline energy expended per turn
        self._food_type = None              # Food class if a consumer   

    def move(self, row: int, col: int) -> None:
        """Updates the Organisms row and col"""
        if row == self._row and col == self._col:
            return
        self._world.move(self._row, self._col, row, col)
        self._energy -= self._move_energy_expenditure
        self._row = row
        self._col = col

    def get_genome(self):
        return self._genome

    def get_color(self):
        return self._genome.get_color()

    def get_energy(self) -> int:
        return self._energy

    def get_location(self) -> (int, int):
        """Returns a tuple with the location (row, col)"""
        return self._row, self._col
    
    def get_food_energy(self) -> int:
        return self._food_energy

    def eat(self, food: 'Organism') -> None:
        """Consumes the food"""
        # This might work for herbivore/carnivore but not passive
        row, col = food.get_location()
        self._energy += food.get_energy()
        self._world.kill_organism(row, col)

    def reproduce(self, row: int, col: int) -> 'Organism':
        """Reproduces and returns the offspring"""
        return self.__class__(self._genome.reproduce(), row, col, self._world)

    def choose_action(self):
        """Depends on type of Organism"""
        pass