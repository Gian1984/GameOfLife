"""
Game of Life - Controller Layer
Coordinates Model and View, handles user events

Following OOP principles:
- No global variables
- Controller holds references to Model and View
- All user interactions go through Controller
- OBSERVER PATTERN: Controller observes Model changes
- STATISTICS: Integrates LiveCounter for population tracking
"""

from livemodel import Observer
from livecounter import LiveCounter


class LiveController(Observer):
    """
    Main controller for Game of Life.

    Responsibilities:
    - Coordinate Model and View
    - Handle all user events (buttons, clicks)
    - Manage animation loop
    - Update display based on model state

    Following MVC pattern: Controller is the mediator
    """

    def __init__(self, model, view):
        """
        Initialize the controller.

        Args:
            model (LiveModel): The game model
            view (LiveView): The game view
        """
        self.__model = model
        self.__view = view
        self.__counter = LiveCounter()  # Statistics tracker

        # OBSERVER PATTERN: Register this controller as an observer of the model
        self.__model.attach(self)

        # Animation state
        self.__is_running = False
        self.__animation_speed = 100  # milliseconds between generations

        # Setup the view components
        self.__setup_view()

        # Connect events
        self.__connect_events()

        # Initial display
        self.__update_display()

    # ========================================================================
    # OBSERVER PATTERN Implementation
    # ========================================================================

    def update(self, subject):
        """
        OBSERVER PATTERN: Called when the observed Model changes state.

        This method is required by the Observer interface.
        It's called automatically by the Model when state changes.

        Args:
            subject: The object that changed (LiveModel)
        """
        # Update the display to reflect the new model state
        self.__update_display()

    # ========================================================================
    # End of Observer Pattern
    # ========================================================================

    # Event Handlers - Public methods called by GUI events

    def on_start_stop(self):
        """
        Handle Start/Stop button click.
        Toggle animation state.
        """
        self.__is_running = not self.__is_running

        if self.__is_running:
            # Start animation
            button = self.__view.command_bar.get_button("Start")
            if button:
                button.config(text="Stop")
            self.__animate()
        else:
            # Stop animation
            button = self.__view.command_bar.get_button("Start")
            if button:
                button.config(text="Start")
            self.__update_display()

    def on_step(self):
        """
        Handle Step button click.
        Advance one generation.
        """
        self.__model.evolve()
        self.__update_display()

    def on_clear(self):
        """
        Handle Clear button click.
        Clear the grid and reset statistics.
        """
        self.__model.clear_grid()
        self.__counter.reset()  # Reset statistics
        self.__update_display()

    def on_random(self):
        """
        Handle Random button click.
        Set random configuration.
        """
        self.__model.set_random_configuration(alive_percentage=0.25)
        self.__update_display()

    def on_cannon(self):
        """
        Handle Cannon button click.
        Set Gosper Glider Gun configuration.
        """
        self.__model.set_cannon_configuration()
        self.__update_display()

    def on_canvas_click(self, event):
        """
        Handle canvas click event.
        Toggle clicked cell.

        Args:
            event: Tkinter event with x, y coordinates
        """
        # Get model coordinates from canvas click
        row, col = self.__view.canvas.get_cell_from_click(event)

        # Toggle cell in model
        self.__model.toggle_cell(row, col)

        # Update display
        self.__update_display()

    def on_change_speed(self, speed_text):
        """
        Handle speed change from entry field.

        Args:
            speed_text (str): Speed value as string
        """
        try:
            new_speed = int(speed_text)
            if new_speed > 0:
                self.__animation_speed = new_speed
                print(f"Speed changed to {new_speed} ms")
        except ValueError:
            print("Invalid speed value")

    def run(self):
        """
        Public method: Start the application.
        """
        self.__view.mainloop()

    # ========================================================================
    # Private Methods
    # ========================================================================

    def __setup_view(self):
        """
        Private method: Setup view components.
        """
        # Create canvas
        canvas = self.__view.create_canvas(
            width=self.__model.width,
            height=self.__model.height,
            cell_size=10
        )

        # Create command bar
        command_bar = self.__view.create_command_bar()

        # Create buttons
        command_bar.create_button("Start", self.on_start_stop)
        command_bar.create_button("Step", self.on_step)
        command_bar.create_button("Clear", self.on_clear)
        command_bar.create_button("Random", self.on_random)
        command_bar.create_button("Cannon", self.on_cannon)

        # Create speed control entry
        command_bar.create_entry(
            "Speed (ms):",
            lambda event: self.on_change_speed(event.widget.get())
        )

        # Create status bar
        self.__view.create_status_bar()

    def __connect_events(self):
        """
        Private method: Connect view events to controller methods.
        """
        # Canvas click event
        self.__view.canvas.bind_click(self.on_canvas_click)

    def __update_display(self):
        """
        Private method: Update the view to reflect current model state.

        This is the key method that separates view from model.
        Gets data from model and sends to view for display.
        """
        # Calculate cell fates for Wikipedia color display
        self.__model.update_cell_fates()

        # Get grid from model
        grid = self.__model.grid

        # Update statistics
        alive_count = self.__counter.count_alive_cells(grid)

        # Display on canvas (uses cell.fate for colors)
        self.__view.canvas.display_grid(grid)

        # Update status with population
        status = "Running" if self.__is_running else "Paused"
        self.__view.update_status(
            self.__model.generation,
            f"{status} | Population: {alive_count}"
        )

    def __animate(self):
        """
        Private method: Animation loop.

        This method calls itself recursively using after()
        to create the animation effect.
        """
        if self.__is_running:
            # Evolve one generation
            self.__model.evolve()

            # Update display
            self.__update_display()

            # Schedule next animation frame
            self.__view.root.after(self.__animation_speed, self.__animate)


# Simple test
if __name__ == "__main__":
    print("Testing LiveController...")
    print("Note: This test requires livemodel and liveview to be in the same directory")

    try:
        from livemodel import LiveModel
        from liveview import LiveView

        # Create model
        model = LiveModel(width=40, height=40)

        # Create view
        view = LiveView("Test Controller")

        # Create controller
        controller = LiveController(model, view)

        # Run
        print("Controller created. Starting GUI...")
        controller.run()

    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure livemodel.py and liveview.py are in the same directory")
