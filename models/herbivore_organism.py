from models import Organism, PassiveOrganism

class HerbivoreOrganism(Organism):
    def __init__(self, genome, row, col, world, generation, species):
        super().__init__(genome, row, col, world, generation, species)        

    def choose_action(self):
        """Herbivore checks adjacent cells for passive organisms, eats if found, 
        moves if no food, and dies if out of energy."""

        # Step 1: Invoke checks / handlers for low energy states.
        if self.hibernate_helper():
            return
        self.panic_mode_helper()
        
        # Step 2: Check adjacent cells for food
        food_found, food_row, food_col = self._world.get_adjacent_food(self._row, self._col, self._food_type)

        # Step 3: Eat the food if found. If no food found, Move. Either seek food or move randomly. Do this however many times genome instructs.
        for num in range(self._genome.get_movement_iterations()):    
            if food_found:                        
                self.eat(self._world.get_cell(food_row, food_col))   
                break        
                        
            elif self._genome.get_can_seek_food():
                if not self.seek_food():  # Try to move strategically toward food
                    if self._genome.get_can_move():
                        self.random_move()  # Fallback to random movement if no food found
            else:
                if self._genome.get_can_move():
                    self.random_move()  # Move randomly if food-seeking is disabled        
        
        # Step 5: Calculate baseline energy loss. Die if out of energy.
        self._energy -= self._base_energy_expenditure
        if self._energy <= 0:
            self._world.kill_organism(self._row, self._col)

        # Step 6: Check if sufficient energy and space to reproduce
        self.check_if_can_reproduce()


