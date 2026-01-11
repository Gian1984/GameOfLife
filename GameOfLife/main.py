"""
Game of Life - Main Entry Point

This is the application entry point.
It should contain minimal code - just instantiation and launch.

Following MVC principles:
- No global variables
- No business logic
- Just create Model, View, Controller and run
"""

from livemodel import LiveModel
from liveview import LiveView
from livecontroller import LiveController


def main():
    """
    Main function to start the Game of Life application.

    Creates Model, View, and Controller in proper order:
    1. Create Model (independent)
    2. Create View (independent)
    3. Create Controller (coordinates Model and View)
    4. Run the application
    """

    # Configuration
    GRID_WIDTH = 40  # Number of cells horizontally
    GRID_HEIGHT = 40  # Number of cells vertically
    WINDOW_TITLE = "Conway's Game of Life - Q54 Project"

    # Step 1: Create Model
    print("Creating Model...")
    model = LiveModel(width=GRID_WIDTH, height=GRID_HEIGHT)

    # Step 2: Create View
    print("Creating View...")
    view = LiveView(title=WINDOW_TITLE)

    # Step 3: Create Controller (connects Model and View)
    print("Creating Controller...")
    controller = LiveController(model, view)

    # Step 4: Run the application
    print("Starting Game of Life...")
    print("Controls:")
    print("  - Start/Stop: Start or stop animation")
    print("  - Step: Advance one generation")
    print("  - Clear: Clear the grid")
    print("  - Random: Generate random configuration (25% alive)")
    print("  - Cannon: Load Gosper Glider Gun")
    print("  - Click cells: Toggle cell state")
    print("  - Speed: Change animation speed (ms)")
    print("\nClose window to exit.")
    print("-" * 50)

    controller.run()

    print("\nApplication closed.")


if __name__ == "__main__":
    """
    Entry point when running as main module.
    """
    main()
