"""
Game of Life - Model Layer
Contains all game logic and data structures

Following OOP principles:
- Private attributes with property decorators
- Composition: Grid composed of Cell objects
- No global variables
- Standard indices (0, 1, 2, 3...) NOT pixel coordinates
- OBSERVER PATTERN: Model notifies observers of state changes
"""

from abc import ABC, abstractmethod
import random


# ============================================================================
# OBSERVER PATTERN - Abstract Classes
# ============================================================================

class Observer(ABC):
    """
    OBSERVER PATTERN: Abstract Observer interface.

    Any class that wants to be notified of Model changes must implement this.
    """

    @abstractmethod
    def update(self, subject):
        """
        Called when the observed subject changes state.

        Args:
            subject: The object that changed (usually LiveModel)
        """
        pass


class Observable(ABC):
    """
    OBSERVER PATTERN: Abstract Observable (Subject) interface.

    Objects that can be observed must implement these methods.
    """

    @abstractmethod
    def attach(self, observer):
        """
        Attach an observer to be notified of changes.

        Args:
            observer (Observer): The observer to attach
        """
        pass

    @abstractmethod
    def detach(self, observer):
        """
        Detach an observer.

        Args:
            observer (Observer): The observer to detach
        """
        pass

    @abstractmethod
    def notify_observers(self):
        """
        Notify all attached observers of a state change.
        """
        pass


# ============================================================================
# End of Observer Pattern Classes
# ============================================================================


# ============================================================================
# STRATEGY PATTERN - Configuration Strategies
# ============================================================================

class ConfigurationStrategy(ABC):
    """
    STRATEGY PATTERN: Abstract strategy for grid configuration.

    Different configuration strategies can be implemented and swapped at runtime.
    """

    @abstractmethod
    def apply(self, model):
        """
        Apply this configuration strategy to the model grid.

        Args:
            model (LiveModel): The model to configure
        """
        pass


class EmptyStrategy(ConfigurationStrategy):
    """
    STRATEGY PATTERN: Clear all cells (empty grid).
    """

    def apply(self, model):
        """Clear the entire grid."""
        for row in range(model.height):
            for col in range(model.width):
                cell = model.grid[row][col]
                cell.state = False
                cell.age = 0


class RandomStrategy(ConfigurationStrategy):
    """
    STRATEGY PATTERN: Random configuration with specified percentage of alive cells.
    """

    def __init__(self, alive_percentage=0.25):
        """
        Initialize the random strategy.

        Args:
            alive_percentage (float): Percentage of cells to set alive (0.0 to 1.0)
        """
        self.__alive_percentage = alive_percentage

    def apply(self, model):
        """Set random cells alive based on percentage."""
        EmptyStrategy().apply(model)  # Start with empty grid
        for row in range(model.height):
            for col in range(model.width):
                if random.random() < self.__alive_percentage:
                    cell = model.grid[row][col]
                    cell.state = True
                    cell.age = 1  # Newborn cells


class CannonStrategy(ConfigurationStrategy):
    """
    STRATEGY PATTERN: Gosper Glider Gun configuration.
    """

    def apply(self, model):
        """Set up the Gosper Glider Gun pattern."""
        EmptyStrategy().apply(model)  # Start with empty grid

        # Gosper Glider Gun pattern coordinates
        pattern = [
            # Left square
            (5, 1), (5, 2), (6, 1), (6, 2),
            # Left part
            (5, 11), (6, 11), (7, 11),
            (4, 12), (8, 12),
            (3, 13), (9, 13), (3, 14), (9, 14),
            (6, 15),
            (4, 16), (8, 16),
            (5, 17), (6, 17), (7, 17),
            (6, 18),
            # Right part
            (3, 21), (4, 21), (5, 21),
            (3, 22), (4, 22), (5, 22),
            (2, 23), (6, 23),
            (1, 25), (2, 25), (6, 25), (7, 25),
            # Right square
            (3, 35), (4, 35), (3, 36), (4, 36)
        ]

        for row, col in pattern:
            if 0 <= row < model.height and 0 <= col < model.width:
                cell = model.grid[row][col]
                cell.state = True
                cell.age = 1  # Newborn cells


# ============================================================================
# End of Strategy Pattern Classes
# ============================================================================


class LiveCell:
    """
    Represents a single cell in the Game of Life grid.

    Encapsulation: Private state with property accessor
    Tracks age: how many generations the cell has been alive
    """

    def __init__(self, state=False):
        """
        Initialize a cell.

        Args:
            state (bool): True if alive, False if dead
        """
        self.__state = state
        self.__previous_state = False  # État précédent pour calculer la transition
        self.__neighbors_count = 0
        self.__age = 0  # Age: how many generations the cell has been alive
        self.__transition = 'dead'  # Transition: 'surviving', 'dying', 'born', 'dead'

    def __str__(self):
        """String representation for debugging"""
        return "1" if self.__state else "0"

    @property
    def state(self):
        """Get the cell state (alive/dead)"""
        return self.__state

    @state.setter
    def state(self, value):
        """Set the cell state (alive/dead)"""
        self.__state = value

    @property
    def neighbors_count(self):
        """Get the number of alive neighbors"""
        return self.__neighbors_count

    @neighbors_count.setter
    def neighbors_count(self, value):
        """Set the number of alive neighbors"""
        self.__neighbors_count = value

    @property
    def age(self):
        """Get the cell age (generations alive)"""
        return self.__age

    @age.setter
    def age(self, value):
        """Set the cell age"""
        self.__age = value

    @property
    def previous_state(self):
        """Get the previous cell state"""
        return self.__previous_state

    @previous_state.setter
    def previous_state(self, value):
        """Set the previous cell state"""
        self.__previous_state = value

    @property
    def transition(self):
        """Get the cell transition ('surviving', 'dying', 'born', 'dead')"""
        return self.__transition

    @transition.setter
    def transition(self, value):
        """Set the cell transition"""
        self.__transition = value

    @property
    def fate(self):
        """Alias for transition (backwards compatibility)"""
        return self.__transition

    @fate.setter
    def fate(self, value):
        """Alias for transition (backwards compatibility)"""
        self.__transition = value


class LiveModel(Observable):
    """
    Main model for the Game of Life.

    Responsibilities:
    - Store grid of cells (COMPOSITION)
    - Calculate neighbor counts
    - Evolve generations based on rules
    - Provide public interface for controllers
    - OBSERVER PATTERN: Notify observers when state changes
    - SINGLETON PATTERN: Only one instance exists

    Important: Uses standard array indices (0, 1, 2...)
               NOT pixel coordinates (0, 10, 20...)
    """

    # SINGLETON PATTERN: Class attribute to store the single instance
    __instance = None

    @classmethod
    def singleton(cls, width=40, height=40):
        """
        SINGLETON PATTERN: Get the single instance of LiveModel.

        This method ensures only one instance of the model exists.
        Subsequent calls return the same instance.

        Args:
            width (int): Grid width (only used on first call)
            height (int): Grid height (only used on first call)

        Returns:
            LiveModel: The singleton instance
        """
        if cls.__instance is None:
            cls.__instance = cls(width, height)
        return cls.__instance

    def __init__(self, width=40, height=40):
        """
        Initialize the Game of Life model.

        Args:
            width (int): Number of cells horizontally (NOT pixels)
            height (int): Number of cells vertically (NOT pixels)
        """
        self.__width = width
        self.__height = height
        self.__generation = 0
        self.__grid = []  # 2D list of LiveCell objects
        self.__observers = []  # OBSERVER PATTERN: List of observers
        self.__create_grid()

    def __str__(self):
        """String representation for debugging"""
        result = f"Generation {self.__generation}\n"
        for row in range(self.__height):
            for col in range(self.__width):
                result += str(self.__grid[row][col])
            result += "\n"
        return result

    @property
    def width(self):
        """Get grid width (number of cells)"""
        return self.__width

    @property
    def height(self):
        """Get grid height (number of cells)"""
        return self.__height

    @property
    def generation(self):
        """Get current generation number"""
        return self.__generation

    @property
    def grid(self):
        """Get the cell grid (read-only access)"""
        return self.__grid

    # ========================================================================
    # OBSERVER PATTERN Implementation
    # ========================================================================

    def attach(self, observer):
        """
        OBSERVER PATTERN: Attach an observer to this model.

        Args:
            observer (Observer): Observer to be notified of changes
        """
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self, observer):
        """
        OBSERVER PATTERN: Detach an observer from this model.

        Args:
            observer (Observer): Observer to remove
        """
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self):
        """
        OBSERVER PATTERN: Notify all observers that the model has changed.

        This is called automatically after state-changing operations.
        """
        for observer in self.__observers:
            observer.update(self)

    # ========================================================================
    # End of Observer Pattern
    # ========================================================================

    def get_cell_state(self, row, col):
        """
        Get the state of a cell at given position.

        Args:
            row (int): Row index (0 to height-1)
            col (int): Column index (0 to width-1)

        Returns:
            bool: True if alive, False if dead
        """
        if 0 <= row < self.__height and 0 <= col < self.__width:
            return self.__grid[row][col].state
        return False

    def toggle_cell(self, row, col):
        """
        Toggle the state of a cell (alive <-> dead).
        Used for user interaction.

        Args:
            row (int): Row index (0 to height-1)
            col (int): Column index (0 to width-1)
        """
        if 0 <= row < self.__height and 0 <= col < self.__width:
            cell = self.__grid[row][col]
            current_state = cell.state
            cell.state = not current_state
            # Update age: if becoming alive, set age to 1; if dying, set to 0
            cell.age = 1 if cell.state else 0
            self.notify_observers()  # OBSERVER PATTERN: Notify change

    def set_cell_state(self, row, col, state):
        """
        Set the state of a specific cell.

        Args:
            row (int): Row index
            col (int): Column index
            state (bool): True for alive, False for dead
        """
        if 0 <= row < self.__height and 0 <= col < self.__width:
            self.__grid[row][col].state = state

    def clear_grid(self):
        """
        Reset all cells to dead state and reset generation counter.
        """
        for row in range(self.__height):
            for col in range(self.__width):
                cell = self.__grid[row][col]
                cell.state = False
                cell.age = 0  # Reset age
        self.__generation = 0
        self.notify_observers()  # OBSERVER PATTERN: Notify change

    def evolve(self):
        """
        Public method: Evolve to the next generation.

        Game of Life rules:
        - Any live cell with 2-3 neighbors survives
        - Any dead cell with exactly 3 neighbors becomes alive
        - All other cells die or stay dead

        Age tracking:
        - Cell born (dead -> alive): age = 1
        - Cell survives (alive -> alive): age += 1
        - Cell dies (alive -> dead): age = 0
        """
        # First, count neighbors for all cells
        self.__update_neighbors_count()

        # Create new states based on rules
        # Important: Store new states separately to avoid affecting counts
        new_states = []
        for row in range(self.__height):
            row_states = []
            for col in range(self.__width):
                cell = self.__grid[row][col]
                neighbors = cell.neighbors_count
                current_state = cell.state

                # Apply Game of Life rules
                if neighbors == 3:
                    # Birth: dead cell with 3 neighbors becomes alive
                    # Survival: alive cell with 3 neighbors stays alive
                    new_state = True
                elif neighbors == 2:
                    # Survival: alive cell with 2 neighbors stays alive
                    # Death: dead cell with 2 neighbors stays dead
                    new_state = current_state
                else:
                    # Death: any other case results in death
                    new_state = False

                row_states.append(new_state)
            new_states.append(row_states)

        # Apply new states to grid and update ages and transitions
        for row in range(self.__height):
            for col in range(self.__width):
                cell = self.__grid[row][col]
                old_state = cell.state
                new_state = new_states[row][col]

                # Save previous state for transition display
                cell.previous_state = old_state

                # Update state
                cell.state = new_state

                # Calculate transition (Wikipedia color conventions)
                # Based on what JUST HAPPENED, not predictions
                if old_state and new_state:
                    cell.transition = 'surviving'  # Bleu: était vivante, reste vivante
                elif not old_state and new_state:
                    cell.transition = 'born'       # Vert: était morte, devient vivante
                elif old_state and not new_state:
                    # Cellule qui meurt - vérifier si éphémère (n'a vécu qu'une génération)
                    if cell.age == 1:
                        cell.transition = 'ephemeral'  # Jaune: n'a vécu qu'une génération
                    else:
                        cell.transition = 'dying'      # Rouge: était vivante, devient morte
                else:
                    cell.transition = 'dead'       # Blanc: était morte, reste morte

                # Update age based on state transition
                if new_state:  # Cell is alive
                    if old_state:  # Was already alive -> survives
                        cell.age += 1  # Increment age
                    else:  # Was dead -> just born
                        cell.age = 1  # Newborn
                else:  # Cell is dead
                    cell.age = 0  # Reset age

        # Increment generation counter
        self.__generation += 1

        # OBSERVER PATTERN: Notify observers of state change
        self.notify_observers()

    def apply_configuration_strategy(self, strategy):
        """
        STRATEGY PATTERN: Apply a configuration strategy to the grid.

        This method uses the Strategy Pattern to allow different grid
        configurations to be applied dynamically.

        Args:
            strategy (ConfigurationStrategy): The strategy to apply

        Example:
            model.apply_configuration_strategy(RandomStrategy(0.25))
            model.apply_configuration_strategy(CannonStrategy())
            model.apply_configuration_strategy(EmptyStrategy())
        """
        strategy.apply(self)
        self.notify_observers()

    def update_cell_fates(self):
        """
        Update cell transitions for display (NO predictions).

        This is called for initial display before any evolution.
        Transitions are calculated in evolve() based on actual state changes.

        For initial display:
        - 'surviving': alive cell -> Blue
        - 'dead': dead cell -> White

        After evolve():
        - 'surviving': was alive, stays alive -> Blue
        - 'born': was dead, becomes alive -> Green
        - 'dying': was alive, becomes dead -> Red
        - 'dead': was dead, stays dead -> White
        """
        # For initial display, just show current state (no predictions)
        for row in range(self.__height):
            for col in range(self.__width):
                cell = self.__grid[row][col]
                if cell.state:
                    cell.transition = 'surviving'  # Vivante = Bleu
                else:
                    cell.transition = 'dead'       # Morte = Blanc

    def set_random_configuration(self, alive_percentage=0.25):
        """
        Set a random initial configuration.

        Args:
            alive_percentage (float): Percentage of cells to set alive (0.0 to 1.0)
        """
        self.clear_grid()
        for row in range(self.__height):
            for col in range(self.__width):
                if random.random() < alive_percentage:
                    cell = self.__grid[row][col]
                    cell.state = True
                    cell.age = 1  # Newborn cells
        # Note: clear_grid() already called notify_observers()
        # but we call again after adding alive cells
        self.notify_observers()

    def set_cannon_configuration(self):
        """
        Set the Gosper Glider Gun configuration.

        Note: Uses direct row/col indices (0, 1, 2...)
               NOT pixel multiplications (0*c, 1*c, 10*c...)
        """
        self.clear_grid()

        # Gosper Glider Gun pattern
        # Pattern coordinates (row, col) - using standard indices
        pattern = [
            # Left square
            (5, 1), (5, 2), (6, 1), (6, 2),
            # Left part
            (5, 11), (6, 11), (7, 11),
            (4, 12), (8, 12),
            (3, 13), (9, 13), (3, 14), (9, 14),
            (6, 15),
            (4, 16), (8, 16),
            (5, 17), (6, 17), (7, 17),
            (6, 18),
            # Right part
            (3, 21), (4, 21), (5, 21),
            (3, 22), (4, 22), (5, 22),
            (2, 23), (6, 23),
            (1, 25), (2, 25), (6, 25), (7, 25),
            # Right square
            (3, 35), (4, 35), (3, 36), (4, 36)
        ]

        for row, col in pattern:
            if 0 <= row < self.__height and 0 <= col < self.__width:
                cell = self.__grid[row][col]
                cell.state = True
                cell.age = 1  # Newborn cells

        # Note: clear_grid() already called notify_observers()
        # but we call again after setting the pattern
        self.notify_observers()

    # ========================================================================
    # Private Methods
    # ========================================================================

    def __create_grid(self):
        """
        Private method: Create the initial grid filled with dead cells.
        Uses standard indices (0, 1, 2...) NOT multiplications like 0*c, 1*c
        """
        self.__grid = []
        for row in range(self.__height):
            row_cells = []
            for col in range(self.__width):
                row_cells.append(LiveCell(state=False))
            self.__grid.append(row_cells)

    def __count_neighbors(self, row, col):
        """
        Private method: Count alive neighbors for a cell.

        Note: Uses direct arithmetic, NOT divisions or modulo operations.
        Handles edge cases properly.

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            int: Number of alive neighbors (0-8)
        """
        count = 0

        # Check all 8 neighboring positions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the cell itself
                if dr == 0 and dc == 0:
                    continue

                neighbor_row = row + dr
                neighbor_col = col + dc

                # Check boundaries
                if 0 <= neighbor_row < self.__height and 0 <= neighbor_col < self.__width:
                    if self.__grid[neighbor_row][neighbor_col].state:
                        count += 1

        return count

    def __update_neighbors_count(self):
        """
        Private method: Update neighbor count for all cells.
        """
        for row in range(self.__height):
            for col in range(self.__width):
                neighbors = self.__count_neighbors(row, col)
                self.__grid[row][col].neighbors_count = neighbors


# Unit test example
if __name__ == "__main__":
    print("Testing LiveModel...")

    # Test 1: Create small grid
    model = LiveModel(width=10, height=10)
    print(f"Grid created: {model.width}x{model.height}")

    # Test 2: Toggle cells
    model.toggle_cell(5, 5)
    model.toggle_cell(5, 6)
    model.toggle_cell(5, 7)
    print("Cells toggled (blinker pattern)")

    # Test 3: Evolve
    print(f"Generation: {model.generation}")
    model.evolve()
    print(f"After evolution: {model.generation}")

    # Test 4: Random configuration
    model.set_random_configuration(0.25)
    print("Random configuration set")

    # Test 5: Cannon
    model.set_cannon_configuration()
    print("Cannon configuration set")

    print("\nLiveModel tests completed!")
