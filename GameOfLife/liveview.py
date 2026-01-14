"""
Game of Life - View Layer
Contains all GUI components

Following OOP principles:
- Private attributes with property decorators
- Composition: View contains Canvas and CommandBar
- Separation from Model: View uses pixels, Model uses indices
- No business logic in View
"""

from tkinter import *
from tkinter import colorchooser


class LiveCanvas:
    """
    Represents the grid display area.

    Responsibilities:
    - Draw grid and cells on canvas
    - Convert between model coordinates (0,1,2...) and canvas pixels (0,10,20...)
    - Handle visual representation only

    Important: Uses PIXELS for display (0, 10, 20...)
               Model uses standard indices (0, 1, 2...)
    """

    def __init__(self, parent, width, height, cell_size=10):
        """
        Initialize the canvas.

        Args:
            parent: Parent tkinter widget
            width (int): Number of cells horizontally
            height (int): Number of cells vertically
            cell_size (int): Size of each cell in pixels
        """
        self.__width = width
        self.__height = height
        self.__cell_size = cell_size

        # Calculate canvas dimensions in pixels
        canvas_width = width * cell_size
        canvas_height = height * cell_size

        # Create canvas widget
        self.__canvas = Canvas(
            parent,
            width=canvas_width,
            height=canvas_height,
            bg='white'
        )
        self.__canvas.pack(side=TOP, padx=5, pady=5)

        # Color configuration (Wikipedia Game of Life conventions)
        self.__colors = {
            'color_dead': 'white',
            'color_grid': 'gray',
            'color_initial': '#888888',            # Gray - initial state (before any evolution)
            'color_newly_born': '#44DD44',         # Green - newly born cell (age = 1, will survive)
            'color_long_lived': '#4444FF',         # Blue - stable cell (alive for >= 2 generations)
            'color_will_die': '#FF4444',           # Red - cell that will die next generation (after living >= 2 gens)
            'color_born_and_die': '#FFDD44',       # Yellow - ephemeral cell (born AND will die next generation)
        }

    @property
    def canvas(self):
        """Get the tkinter canvas widget"""
        return self.__canvas

    @property
    def cell_size(self):
        """Get the cell size in pixels"""
        return self.__cell_size

    def set_colors(self, surviving_color=None, born_color=None, dying_color=None,
                   dead_color=None, grid_color=None):
        """
        Set colors for cells and grid (Wikipedia conventions).

        Args:
            surviving_color (str): Blue - cells that stay alive
            born_color (str): Green - cells that will be born
            dying_color (str): Red - cells that will die
            dead_color (str): Color for dead cells
            grid_color (str): Color for grid lines
        """
        if surviving_color:
            self.__colors['surviving'] = surviving_color
        if born_color:
            self.__colors['born'] = born_color
        if dying_color:
            self.__colors['dying'] = dying_color
        if dead_color:
            self.__colors['dead'] = dead_color
        if grid_color:
            self.__colors['grid'] = grid_color

    def get_cell_from_click(self, event):
        """
        Public method: Get model cell coordinates from a click event.

        Args:
            event: Tkinter event with x, y attributes

        Returns:
            tuple: (row, col) model indices
        """
        return self.__canvas_to_model(event.x, event.y)

    def draw_grid(self):
        """
        Draw grid lines on canvas.
        Uses pixel coordinates for display.
        """
        canvas_width = self.__width * self.__cell_size
        canvas_height = self.__height * self.__cell_size

        # Vertical lines
        for col in range(self.__width + 1):
            x = col * self.__cell_size
            self.__canvas.create_line(
                x, 0, x, canvas_height,
                fill=self.__colors['color_grid'],
                width=1
            )

        # Horizontal lines
        for row in range(self.__height + 1):
            y = row * self.__cell_size
            self.__canvas.create_line(
                0, y, canvas_width, y,
                fill=self.__colors['color_grid'],
                width=1
            )

    def draw_cell(self, row, col, cell_obj):
        """
        Draw a single cell with colors based on its properties.

        Args:
            row (int): Model row index
            col (int): Model column index
            cell_obj (LiveCell): The cell object from the model
        """
        x1, y1, x2, y2 = self.__model_to_canvas(row, col)

        fill_color = self.__colors['color_dead'] # Default to dead color

        if cell_obj.state: # Only consider special colors if the cell is alive
            if cell_obj.is_newly_born and cell_obj.will_die_next_gen:
                fill_color = self.__colors['color_born_and_die'] # Yellow
            elif cell_obj.is_newly_born:
                fill_color = self.__colors['color_newly_born'] # Green
            elif cell_obj.will_die_next_gen:
                fill_color = self.__colors['color_will_die'] # Red
            elif cell_obj.is_long_lived:
                fill_color = self.__colors['color_long_lived'] # Blue
            else:
                fill_color = self.__colors['color_initial'] # Gray - initial state

        self.__canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=fill_color,
            outline=''  # No outline for cells (grid lines handle that)
        )

    def clear(self):
        """
        Clear the entire canvas.
        """
        self.__canvas.delete(ALL)

    def display_grid(self, grid):
        """
        Display the entire grid from model.

        This is the main display method called by controller.
        Separates visualization from game logic.

        ITERATOR PATTERN: Uses __grid_iterator() instead of nested loops.

        Args:
            grid: 2D list of LiveCell objects from model
        """
        # Clear previous display
        self.clear()

        # Draw all cells FIRST using ITERATOR PATTERN
        # Uses cell.fate for Wikipedia color conventions
        for row, col, cell in self.__grid_iterator(grid):
            self.draw_cell(row, col, cell)

        # Draw grid lines AFTER cells (so they appear on top)
        self.draw_grid()

    def bind_click(self, callback):
        """
        Bind a click event to the canvas.

        Args:
            callback: Function to call on click (receives event)
        """
        self.__canvas.bind("<Button-1>", callback)

    # ========================================================================
    # Private Methods
    # ========================================================================

    def __model_to_canvas(self, row, col):
        """
        Private method: Convert model indices to canvas pixel coordinates.

        Important: This is the ONLY place where we convert indices to pixels.
        Uses direct multiplication, NOT divisions or modulo.

        Args:
            row (int): Model row index (0, 1, 2...)
            col (int): Model column index (0, 1, 2...)

        Returns:
            tuple: (x1, y1, x2, y2) rectangle coordinates in pixels
        """
        x1 = col * self.__cell_size
        y1 = row * self.__cell_size
        x2 = x1 + self.__cell_size
        y2 = y1 + self.__cell_size
        return (x1, y1, x2, y2)

    def __canvas_to_model(self, x, y):
        """
        Private method: Convert canvas pixel coordinates to model indices.

        Important: Uses integer division (//) NOT modulo (%)
        This is cleaner than the procedural version's event.x % c

        Args:
            x (int): Canvas x coordinate in pixels
            y (int): Canvas y coordinate in pixels

        Returns:
            tuple: (row, col) model indices
        """
        col = x // self.__cell_size
        row = y // self.__cell_size
        return (row, col)

    def __grid_iterator(self, grid):
        """
        ITERATOR PATTERN: Generator that yields all cells with their coordinates.

        This is a private iterator method that implements the Iterator Pattern
        to traverse the grid in a clean, memory-efficient way.

        Args:
            grid: 2D list of LiveCell objects

        Yields:
            tuple: (row, col, cell) for each cell in the grid
        """
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                yield (row, col, grid[row][col])


class LiveCommandBar:
    """
    Represents the command button bar.

    Responsibilities:
    - Create and manage control buttons
    - No game logic - just UI components
    """

    def __init__(self, parent):
        """
        Initialize the command bar.

        Args:
            parent: Parent tkinter widget
        """
        self.__frame = Frame(parent)
        self.__frame.pack(side=TOP, fill=X, padx=5, pady=5)

        self.__buttons = {}

    def create_button(self, text, command):
        """
        Create a button and add it to the command bar.

        Args:
            text (str): Button label
            command: Function to call when clicked

        Returns:
            Button: The created button widget
        """
        button = Button(self.__frame, text=text, command=command)
        button.pack(side=LEFT, padx=3, pady=3)
        self.__buttons[text] = button
        return button

    def create_entry(self, label_text, callback):
        """
        Create an entry field with label.

        Args:
            label_text (str): Label text
            callback: Function to call on Enter key

        Returns:
            Entry: The created entry widget
        """
        # Entry FIRST (with side=RIGHT, last created appears leftmost)
        entry = Entry(self.__frame, width=10)
        entry.bind("<Return>", callback)
        entry.pack(side=RIGHT, padx=3)

        # Label AFTER (appears to the left of entry)
        label = Label(self.__frame, text=label_text)
        label.pack(side=RIGHT, padx=3)

        return entry

    def get_button(self, text):
        """
        Get a button by its text.

        Args:
            text (str): Button label

        Returns:
            Button: The button widget or None
        """
        return self.__buttons.get(text)


class LiveView:
    """
    Main view class for Game of Life.

    Responsibilities:
    - Create main window
    - Assemble canvas and command bar (COMPOSITION)
    - Display status information
    - Coordinate GUI components

    No game logic - pure presentation layer
    """

    def __init__(self, title="Game of Life"):
        """
        Initialize the main view.

        Args:
            title (str): Window title
        """
        self.__title = title
        self.__root = Tk()
        self.__root.title(self.__title)

        # Components will be created by public methods
        self.__canvas = None
        self.__command_bar = None
        self.__status_label = None

    @property
    def root(self):
        """Get the root window"""
        return self.__root

    @property
    def canvas(self):
        """Get the canvas component"""
        return self.__canvas

    @property
    def command_bar(self):
        """Get the command bar component"""
        return self.__command_bar

    def create_canvas(self, width, height, cell_size=10):
        """
        Create the canvas component.

        Args:
            width (int): Number of cells horizontally
            height (int): Number of cells vertically
            cell_size (int): Cell size in pixels

        Returns:
            LiveCanvas: The created canvas
        """
        self.__canvas = LiveCanvas(self.__root, width, height, cell_size)
        return self.__canvas

    def create_command_bar(self):
        """
        Create the command bar component.

        Returns:
            LiveCommandBar: The created command bar
        """
        self.__command_bar = LiveCommandBar(self.__root)
        return self.__command_bar

    def create_status_bar(self):
        """
        Create a status label at the bottom.

        Returns:
            Label: The status label
        """
        self.__status_label = Label(
            self.__root,
            text="Generation: 0 | Status: Ready",
            relief=SUNKEN,
            anchor=W
        )
        self.__status_label.pack(side=BOTTOM, fill=X)
        return self.__status_label

    def update_status(self, generation, status="Running"):
        """
        Update the status display.

        Args:
            generation (int): Current generation number
            status (str): Current status text
        """
        if self.__status_label:
            self.__status_label.config(
                text=f"Generation: {generation} | Status: {status}"
            )

    def mainloop(self):
        """
        Start the GUI main loop.
        """
        self.__root.mainloop()


# Simple test
if __name__ == "__main__":
    print("Testing LiveView...")

    # Create view
    view = LiveView("Test Game of Life")

    # Create canvas
    canvas = view.create_canvas(width=20, height=20, cell_size=15)

    # Create command bar
    command_bar = view.create_command_bar()

    # Add some test buttons
    command_bar.create_button("Test 1", lambda: print("Button 1 clicked"))
    command_bar.create_button("Test 2", lambda: print("Button 2 clicked"))

    # Create status bar
    view.create_status_bar()
    view.update_status(0, "Test mode")

    # Draw test pattern with Wikipedia colors
    canvas.draw_grid()
    canvas.draw_cell(5, 5, 'surviving')  # Blue - stays alive
    canvas.draw_cell(5, 6, 'born')       # Green - will be born
    canvas.draw_cell(5, 7, 'dying')      # Red - will die

    print("View created. Close window to exit.")
    view.mainloop()
