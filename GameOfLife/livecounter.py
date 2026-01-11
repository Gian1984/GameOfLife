"""
Game of Life - Counter/Statistics Module
Tracks game statistics (optional but useful)

Following OOP principles:
- Encapsulation of statistics
- Can be integrated with Model or Controller
"""


class LiveCounter:
    """
    Tracks statistics for the Game of Life.

    Responsibilities:
    - Count generations
    - Count alive cells
    - Track population history
    - Calculate statistics

    Optional feature but demonstrates good separation of concerns.
    """

    def __init__(self):
        """
        Initialize the counter.
        """
        self.__generation_count = 0
        self.__alive_cells_count = 0
        self.__population_history = []
        self.__max_population = 0
        self.__min_population = 0

    @property
    def generation_count(self):
        """Get the current generation count"""
        return self.__generation_count

    @property
    def alive_cells_count(self):
        """Get the current number of alive cells"""
        return self.__alive_cells_count

    @property
    def max_population(self):
        """Get the maximum population reached"""
        return self.__max_population

    @property
    def min_population(self):
        """Get the minimum population (after first generation)"""
        return self.__min_population

    @property
    def population_history(self):
        """Get the population history (read-only)"""
        return self.__population_history.copy()

    def __str__(self):
        """
        String representation of current statistics.
        """
        stats = self.get_statistics()
        return (
            f"Generation: {stats['generation']}\n"
            f"Alive Cells: {stats['alive_cells']}\n"
            f"Max Population: {stats['max_population']}\n"
            f"Min Population: {stats['min_population']}\n"
            f"Avg Population: {stats['average_population']:.2f}"
        )

    def reset(self):
        """
        Reset all counters.
        """
        self.__generation_count = 0
        self.__alive_cells_count = 0
        self.__population_history = []
        self.__max_population = 0
        self.__min_population = 0

    def increment_generation(self):
        """
        Increment the generation counter.
        """
        self.__generation_count += 1

    def update_alive_count(self, count):
        """
        Update the alive cells count.

        Args:
            count (int): Number of alive cells
        """
        self.__alive_cells_count = count

        # Update history
        self.__population_history.append(count)

        # Update max/min
        if count > self.__max_population:
            self.__max_population = count

        if self.__min_population == 0 or count < self.__min_population:
            self.__min_population = count

    def count_alive_cells(self, grid):
        """
        Count alive cells in a grid and update statistics.

        Args:
            grid: 2D list of LiveCell objects

        Returns:
            int: Number of alive cells
        """
        count = 0
        for row in grid:
            for cell in row:
                if cell.state:
                    count += 1

        self.update_alive_count(count)
        return count

    def get_average_population(self):
        """
        Calculate average population over all generations.

        Returns:
            float: Average population or 0 if no history
        """
        if not self.__population_history:
            return 0.0

        return sum(self.__population_history) / len(self.__population_history)

    def get_statistics(self):
        """
        Get all statistics as a dictionary.

        Returns:
            dict: Statistics dictionary
        """
        return {
            'generation': self.__generation_count,
            'alive_cells': self.__alive_cells_count,
            'max_population': self.__max_population,
            'min_population': self.__min_population,
            'average_population': self.get_average_population(),
            'history_length': len(self.__population_history)
        }


# Simple test
if __name__ == "__main__":
    print("Testing LiveCounter...")

    counter = LiveCounter()

    # Simulate some generations
    counter.increment_generation()
    counter.update_alive_count(50)

    counter.increment_generation()
    counter.update_alive_count(75)

    counter.increment_generation()
    counter.update_alive_count(60)

    print(counter)
    print("\nStatistics:", counter.get_statistics())

    print("\nLiveCounter tests completed!")
