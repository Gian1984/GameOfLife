# Game of Life (Q54) - TODO List

## Project Overview

**Goal**: Convert a procedural "Game of Life" application into an Object-Oriented application using MVC architecture.

**Theme**: Conway's Game of Life cellular automaton

**Files to Create**:
- `livemodel.py` - All Model classes
- `liveview.py` - All View classes
- `livecontroller.py` - All Controller classes
- `livecounter.py` - Counter class (optional)
- `main.py` - Application entry point

**Key OOP Concepts to Apply**:
- Encapsulation (private attributes/methods with accessors)
- Inheritance & Polymorphism (different cell types from abstract base class)
- Composition (grid is composed of cells)
- Aggregation (game is a collection of objects)
- Design Patterns: Factory, Iterator, Singleton, Observer, Strategy

---

## Phase 0: Setup & Understanding

### Step 0.1: Environment Setup
- [ ] Create project directory structure
- [ ] Set up Python virtual environment (if needed)
- [ ] Install tkinter (usually comes with Python)
- [ ] Test that tkinter works with a simple window

**Learning Objective**: Prepare development environment

**Files**: None yet

---

### Step 0.2: Study Reference Materials
- [ ] Read `OOP_REFERENCE.md` - Focus on:
  - Encapsulation (Section 1.1)
  - Inheritance (Section 1.2)
  - MVC Architecture (Section 2.1)
  - Observer Pattern (Section 3.2)
  - Iterator Pattern (Section 3.6)
- [ ] Download and run `GameOfLife_procedural.py` to understand requirements
- [ ] Study `MvcSample_oop.py` to understand MVC structure
- [ ] Review `GameOfLife_MvcArchitecture.png` architecture diagram

**Learning Objective**: Understand MVC pattern and Game of Life rules

**Reference**: OOP_REFERENCE.md sections 2.1 (MVC), 3.2 (Observer)

---

### Step 0.3: Understand Game of Life Rules
- [ ] Read about Conway's Game of Life rules:
  - Any live cell with 2-3 neighbors survives
  - Any dead cell with exactly 3 neighbors becomes alive
  - All other cells die or stay dead
- [ ] Identify key components:
  - Grid/Canvas
  - Cells (alive/dead states)
  - Neighbors counting logic
  - Generation evolution

**Learning Objective**: Understand domain logic before coding

**Reference**: Wikipedia link in project description

---

## Phase 1: Model Layer - Core Game Logic

### Step 1.1: Create LiveCell Class (livemodel.py)
- [ ] Create `LiveCell` class with:
  - Private attributes: `__state` (alive/dead), `__neighbors_count`
  - Constructor: `__init__(self, state=False)`
  - Property decorator for `state` (getter/setter)
  - Method: `count_neighbors()` or store neighbors count
  - Magic method: `__str__()` for debugging
- [ ] Test LiveCell independently (print states, toggle states)

**Learning Objective**: Encapsulation with private attributes and properties

**Expected**:
```python
class LiveCell:
    def __init__(self, state=False):
        self.__state = state
        self.__neighbors_count = 0

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value
```

**Reference**: OOP_REFERENCE.md Section 1.1 (Encapsulation)

**Files**: `livemodel.py`

---

### Step 1.2: Create LiveModel Class - Basic Structure
- [ ] Create `LiveModel` class with:
  - Private attributes:
    - `__grid` (2D list/matrix of LiveCell objects)
    - `__width` and `__height` (grid dimensions)
    - `__generation` (current generation number)
  - Constructor: `__init__(self, width, height)`
  - Method: `__create_grid()` - Initialize grid with dead cells
  - Property: `grid` (getter only - no setter)
  - Property: `generation` (getter only)
- [ ] Initialize a 50x50 grid and verify it's created correctly

**Learning Objective**: Composition (grid is composed of cells)

**Expected**: 6 public methods total for LiveModel

**Reference**: Composition pattern from course

**Files**: `livemodel.py`

---

### Step 1.3: LiveModel - Neighbor Counting Logic
- [ ] Add method: `__count_neighbors(self, row, col)` - PRIVATE
  - Count alive neighbors for cell at (row, col)
  - Handle edge cases (borders wrap around or stay as boundaries)
  - Return count (0-8)
- [ ] Add method: `__update_neighbors_count(self)` - PRIVATE
  - Loop through all cells
  - Update each cell's neighbors count
- [ ] Test with manual cell patterns (glider, blinker)

**Learning Objective**: Private helper methods, logic encapsulation

**Reference**: Game of Life rules

**Files**: `livemodel.py`

---

### Step 1.4: LiveModel - Evolution Logic
- [ ] Add method: `evolve(self)` - PUBLIC
  - Create new generation based on current state
  - Apply Game of Life rules:
    - Cell with 2-3 neighbors survives
    - Dead cell with 3 neighbors becomes alive
    - All others die
  - Update grid to new generation
  - Increment generation counter
- [ ] Test evolution with known patterns (oscillators, still lifes)

**Learning Objective**: Core game logic implementation

**Reference**: Game of Life rules

**Files**: `livemodel.py`

---

### Step 1.5: LiveModel - Cell State Manipulation
- [ ] Add method: `toggle_cell(self, row, col)` - PUBLIC
  - Toggle state of cell at (row, col)
  - Used for user interaction
- [ ] Add method: `clear_grid(self)` - PUBLIC
  - Reset all cells to dead state
  - Reset generation to 0
- [ ] Test both methods

**Learning Objective**: Public interface for external interaction

**Files**: `livemodel.py`

---

### Step 1.6: LiveModel - Initial Configurations
- [ ] Add method: `set_random_configuration(self, alive_percentage=0.25)` - PUBLIC
  - Randomly set cells alive (25% by default)
  - Use `random.random()` for each cell
- [ ] Add method: `set_cannon_configuration(self)` - PUBLIC
  - Set up "Gosper Glider Gun" pattern
  - Predefined pattern coordinates
- [ ] Test both configurations

**Learning Objective**: Different initialization strategies

**Note**: Strategy Pattern can be applied here as bonus (Step 4.4)

**Files**: `livemodel.py`

---

## Phase 2: View Layer - Graphical User Interface

### Step 2.1: Create LiveView Class - Basic Window (liveview.py)
- [ ] Create `LiveView` class with:
  - Private attribute: `__root` (tkinter root window)
  - Private attribute: `__title` (window title)
  - Constructor: `__init__(self, title="Game of Life")`
    - Create tkinter root window
    - Set window title
    - Set window size
  - Method: `run(self)` - Start tkinter main loop
- [ ] Test: Create and display empty window

**Learning Objective**: Basic tkinter GUI setup

**Expected**: 6 public methods total for LiveView

**Reference**: MvcSample_oop.py

**Files**: `liveview.py`

---

### Step 2.2: Create LiveCanvas Class - Grid Display
- [ ] Create `LiveCanvas` class with:
  - Private attributes:
    - `__canvas` (tkinter Canvas widget)
    - `__cell_size` (pixel size, e.g., 10)
    - `__width`, `__height` (grid dimensions)
    - `__colors` (dict: alive_color, dead_color, grid_color)
  - Constructor: `__init__(self, parent, width, height, cell_size=10)`
  - Method: `draw_grid(self)` - Draw grid lines
  - Method: `draw_cell(self, row, col, state)` - Draw single cell
  - Method: `clear(self)` - Clear canvas
- [ ] Test: Draw a static grid

**Learning Objective**: Canvas manipulation, composition in View

**Expected**: 4 public methods total for LiveCanvas

**Reference**: Procedural version for pixel logic

**Files**: `liveview.py`

---

### Step 2.3: LiveCanvas - Coordinate Conversion
- [ ] Add method: `__model_to_canvas(self, row, col)` - PRIVATE
  - Convert model indices (0, 1, 2...) to canvas pixels (0, 10, 20...)
  - Return (x1, y1, x2, y2) rectangle coordinates
- [ ] Add method: `__canvas_to_model(self, x, y)` - PRIVATE
  - Convert canvas pixel coordinates to model indices
  - Used for mouse clicks
  - Return (row, col)
- [ ] Test coordinate conversions

**Learning Objective**: Separation between Model and View coordinate systems

**Note**: Model uses standard indices (0,1,2...), View uses pixels (0,10,20...)

**Files**: `liveview.py`

---

### Step 2.4: LiveCanvas - Display Grid from Model
- [ ] Add method: `display_grid(self, grid)` - PUBLIC
  - Take grid (2D list of LiveCell objects) as parameter
  - Clear canvas
  - Draw grid lines
  - Loop through grid and draw each cell based on state
- [ ] Test with a LiveModel instance

**Learning Objective**: View displays Model data

**Files**: `liveview.py`

---

### Step 2.5: Create LiveCommandBar Class - Control Buttons
- [ ] Create `LiveCommandBar` class with:
  - Private attribute: `__frame` (tkinter Frame)
  - Private attribute: `__buttons` (dict of button widgets)
  - Constructor: `__init__(self, parent)`
  - Method: `create_button(self, text, command)` - Create button with callback
  - Buttons to create:
    - "Start/Stop" - Toggle animation
    - "Step" - Advance one generation
    - "Clear" - Clear grid
    - "Random" - Set random configuration
    - "Cannon" - Set cannon configuration
- [ ] Test: Display button bar (commands can be empty for now)

**Learning Objective**: GUI component creation

**Expected**: 1 public method for LiveCommandBar

**Files**: `liveview.py`

---

### Step 2.6: LiveView - Assemble Components
- [ ] In `LiveView`, add:
  - Private attribute: `__canvas` (LiveCanvas instance)
  - Private attribute: `__command_bar` (LiveCommandBar instance)
  - Method: `__create_components(self)` - PRIVATE
    - Create and pack LiveCanvas
    - Create and pack LiveCommandBar
  - Call `__create_components()` in constructor
- [ ] Test: Full GUI with grid and buttons

**Learning Objective**: Composition in View (View contains Canvas and CommandBar)

**Files**: `liveview.py`

---

### Step 2.7: LiveView - Color Configuration
- [ ] Add method: `set_colors(self, alive_color, dead_color, grid_color)` - PUBLIC
  - Allow user to change colors
  - Pass colors to LiveCanvas
- [ ] Add color selection dialog (optional: use tkinter.colorchooser)
- [ ] Test color changes

**Learning Objective**: User customization, View configuration

**Files**: `liveview.py`

---

### Step 2.8: LiveView - Status Display
- [ ] Add private attribute: `__status_label` (tkinter Label)
- [ ] Add method: `update_status(self, generation)` - PUBLIC
  - Display current generation number
  - Display running/paused state
- [ ] Place status label in GUI
- [ ] Test status updates

**Learning Objective**: Information display to user

**Files**: `liveview.py`

---

## Phase 3: Controller Layer - Event Handling & Coordination

### Step 3.1: Create LiveController Class - Basic Structure
- [ ] Create `LiveController` class with:
  - Private attributes:
    - `__model` (LiveModel instance)
    - `__view` (LiveView instance)
    - `__is_running` (boolean for animation state)
    - `__animation_speed` (milliseconds between generations)
  - Constructor: `__init__(self, model, view)`
    - Store model and view references
    - Initialize state variables
- [ ] No testing yet (need to connect events)

**Learning Objective**: Controller holds Model and View references

**Expected**: ~10 public methods total for LiveController (7 for GUI events)

**Files**: `livecontroller.py`

---

### Step 3.2: LiveController - Connect View Events
- [ ] Add method: `__connect_events(self)` - PRIVATE
  - Connect button commands to controller methods:
    - Start/Stop → `on_start_stop()`
    - Step → `on_step()`
    - Clear → `on_clear()`
    - Random → `on_random()`
    - Cannon → `on_cannon()`
  - Connect canvas click → `on_canvas_click(event)`
- [ ] Call `__connect_events()` in constructor
- [ ] Create empty event handler methods (stubs)

**Learning Objective**: Controller handles all user events

**Files**: `livecontroller.py`

---

### Step 3.3: LiveController - Implement Event Handlers (Part 1)
- [ ] Implement `on_clear(self)`:
  - Call `model.clear_grid()`
  - Update view display
  - Update status
- [ ] Implement `on_random(self)`:
  - Call `model.set_random_configuration()`
  - Update view display
  - Update status
- [ ] Implement `on_cannon(self)`:
  - Call `model.set_cannon_configuration()`
  - Update view display
  - Update status
- [ ] Test these three buttons

**Learning Objective**: Controller coordinates Model and View

**Files**: `livecontroller.py`

---

### Step 3.4: LiveController - Implement Event Handlers (Part 2)
- [ ] Implement `on_step(self)`:
  - Call `model.evolve()`
  - Update view display
  - Update status with new generation
- [ ] Implement `on_canvas_click(self, event)`:
  - Get click coordinates (x, y)
  - Convert to model coordinates (row, col)
  - Call `model.toggle_cell(row, col)`
  - Update view display
- [ ] Test step evolution and cell toggling

**Learning Objective**: User interaction with grid

**Files**: `livecontroller.py`

---

### Step 3.5: LiveController - Animation Logic
- [ ] Implement `on_start_stop(self)`:
  - Toggle `__is_running` state
  - If starting: call `__animate()`
  - If stopping: animation will stop at next cycle
  - Update button text (Start/Stop)
- [ ] Implement `__animate(self)` - PRIVATE:
  - If `__is_running`:
    - Call `model.evolve()`
    - Update view display
    - Schedule next animation frame using `view.after()`
- [ ] Test animation start/stop

**Learning Objective**: Event-driven animation loop

**Files**: `livecontroller.py`

---

### Step 3.6: LiveController - Display Update
- [ ] Add method: `__update_display(self)` - PRIVATE
  - Get grid from model
  - Call `view.canvas.display_grid(grid)`
  - Call `view.update_status(model.generation)`
- [ ] Replace repeated update code in event handlers with this method
- [ ] Test that all updates still work

**Learning Objective**: DRY principle (Don't Repeat Yourself)

**Files**: `livecontroller.py`

---

### Step 3.7: Create main.py - Application Entry Point
- [ ] Create `main.py` with:
  - Import Model, View, Controller
  - Create LiveModel instance (50x50 grid)
  - Create LiveView instance
  - Create LiveController instance (pass model and view)
  - Set initial configuration (optional)
  - Start view main loop
- [ ] Test complete application

**Learning Objective**: MVC integration, application startup

**Expected**: Minimal code, just instantiation and launch

**Files**: `main.py`

---

## Phase 4: Design Patterns Implementation

### Step 4.1: Iterator Pattern for Canvas Display
- [ ] In `LiveCanvas`, implement Iterator Pattern:
  - Add `__iter__(self)` method - Returns self
  - Add `__next__(self)` method - Yields grid cells one by one
  - Modify `display_grid()` to use iterator:
    ```python
    for cell_info in self:
        # cell_info = (row, col, state)
        self.draw_cell(row, col, state)
    ```
- [ ] Test that display still works

**Learning Objective**: Iterator Pattern for collection traversal

**Reference**: OOP_REFERENCE.md Section 3.6 (Iterator Pattern)

**Files**: `liveview.py`

---

### Step 4.2: Observer Pattern - Model Notifies View
- [ ] Implement Observer Pattern:
  - Create `Observer` abstract base class (ABC) with `update()` method
  - Make LiveController inherit from Observer
  - Add to LiveModel:
    - List of observers: `__observers = []`
    - Method: `attach(observer)` - Add observer
    - Method: `notify_observers()` - Call `update()` on all observers
  - Call `notify_observers()` after grid changes
  - Implement `update()` in LiveController to refresh display
- [ ] Test automatic view updates

**Learning Objective**: Observer Pattern for loose coupling

**Reference**: OOP_REFERENCE.md Section 3.2 (Observer Pattern)

**Files**: `livemodel.py`, `livecontroller.py`

---

### Step 4.3: Singleton Pattern - Single Model Instance (Optional)
- [ ] Implement Singleton Pattern for LiveModel:
  - Add class attribute: `__instance = None`
  - Add class method: `singleton(cls, width=50, height=50)`
  - Modify `__init__` to prevent multiple instances
  - Update `main.py` to use `LiveModel.singleton()`
- [ ] Test that only one model instance exists

**Learning Objective**: Singleton Pattern for single instance

**Reference**: OOP_REFERENCE.md Section 3.1 (Singleton Pattern)

**Note**: This is optional but demonstrates the pattern

**Files**: `livemodel.py`, `main.py`

---

### Step 4.4: Strategy Pattern - Configuration Strategies
- [ ] Implement Strategy Pattern for initial configurations:
  - Create abstract `ConfigurationStrategy` class with `apply(grid)` method
  - Create concrete strategies:
    - `RandomStrategy` - 25% alive cells
    - `CannonStrategy` - Gosper Glider Gun
    - `EmptyStrategy` - All dead
  - Add to LiveModel:
    - Method: `set_configuration(strategy)` - Apply strategy
  - Update controller to use strategies
- [ ] Test different strategies

**Learning Objective**: Strategy Pattern for interchangeable algorithms

**Reference**: OOP_REFERENCE.md Section 3.3 (Strategy Pattern)

**Files**: `livemodel.py`

---

### Step 4.5: Factory Pattern - Cell Type Factory (Advanced)
- [ ] If implementing different cell types (bonus feature):
  - Create abstract `Cell` class
  - Create concrete cell types: `StandardCell`, `HighLifeCell`, etc.
  - Create `CellFactory` with `create_cell(cell_type)` method
  - Use factory in LiveModel when creating grid
- [ ] Test different cell types

**Learning Objective**: Factory Pattern for object creation

**Reference**: OOP_REFERENCE.md Section 3.4 (Factory Pattern)

**Note**: This is for advanced features (different Life rules)

**Files**: `livemodel.py`

---

## Phase 5: Additional Features

### Step 5.1: Cell Color Based on Neighbors
- [ ] Modify cell display to show different colors based on neighbor count:
  - 0-1 neighbors: Color A (dying)
  - 2-3 neighbors: Color B (stable)
  - 4-8 neighbors: Color C (overcrowded)
- [ ] Update LiveCanvas color logic
- [ ] Create color gradient or distinct colors
- [ ] Test visual difference

**Learning Objective**: Enhanced visualization

**Files**: `liveview.py`

---

### Step 5.2: LiveCounter Class - Generation Counter
- [ ] Create `LiveCounter` class in `livecounter.py`:
  - Track generation count
  - Track alive cells count
  - Track population history
  - Methods: increment, reset, get_stats
- [ ] Integrate with LiveModel
- [ ] Display stats in LiveView
- [ ] Test counter updates

**Learning Objective**: Separate concern for statistics

**Files**: `livecounter.py`, integrate with model and view

---

### Step 5.3: Speed Control
- [ ] Add speed control slider/buttons:
  - Slow (500ms), Normal (100ms), Fast (50ms), Very Fast (10ms)
- [ ] Update LiveCommandBar with speed controls
- [ ] Update LiveController to adjust `__animation_speed`
- [ ] Test different speeds

**Learning Objective**: User control over animation

**Files**: `liveview.py`, `livecontroller.py`

---

### Step 5.4: Grid Size Configuration
- [ ] Add ability to change grid size:
  - Input dialog for width/height
  - Recreate model with new dimensions
  - Update view accordingly
- [ ] Test with different grid sizes

**Learning Objective**: Dynamic reconfiguration

**Files**: `liveview.py`, `livecontroller.py`, `main.py`

---

### Step 5.5: Save/Load Patterns
- [ ] Add save pattern functionality:
  - Save current grid state to file (JSON or pickle)
  - Store pattern name, dimensions, alive cells
- [ ] Add load pattern functionality:
  - Load pattern from file
  - Apply to grid
- [ ] Test save and load

**Learning Objective**: File I/O, data persistence

**Files**: `livemodel.py`, `livecontroller.py`

---

## Phase 6: Code Quality & Testing

### Step 6.1: Code Review - Encapsulation
- [ ] Review all classes for proper encapsulation:
  - All attributes should be private (`__attribute`) or protected (`_attribute`)
  - Public interface through properties or methods
  - No direct access to private attributes from outside
- [ ] Add `@property` decorators where needed
- [ ] Refactor if necessary

**Learning Objective**: Proper encapsulation principles

**Reference**: OOP_REFERENCE.md Section 1.1, Section 4.2

---

### Step 6.2: Code Review - Method Ordering
- [ ] Reorder methods in each class according to specification:
  1. Class attributes
  2. Class methods (`@classmethod`)
  3. Creation methods (singleton, factory, `__new__`)
  4. Constructor (`__init__`)
  5. Destructor (`__del__`) if any
  6. Magic methods (`__str__`, `__iter__`, `__next__`, etc.)
  7. Accessors (properties)
  8. Public methods
  9. Protected methods (`_method`)
  10. Private methods (`__method`)
- [ ] Apply to all files

**Learning Objective**: Code organization standards

**Reference**: Project description ordering requirements

---

### Step 6.3: Add Documentation
- [ ] Add docstrings to all classes:
  - Class purpose
  - Attributes description
  - Public interface overview
- [ ] Add docstrings to all public methods:
  - Method purpose
  - Parameters description
  - Return value description
- [ ] Add inline comments for complex logic

**Learning Objective**: Code documentation

---

### Step 6.4: Add Magic Methods
- [ ] Add useful magic methods where appropriate:
  - `__str__()` - String representation for debugging
  - `__repr__()` - Official string representation
  - `__len__()` - For grid/collections
  - `__getitem__()` - For indexing if useful
- [ ] Test magic methods

**Learning Objective**: Python special methods

**Reference**: OOP_REFERENCE.md mentions magic methods

---

### Step 6.5: Unit Testing - Model
- [ ] Create `test_model.py` with unit tests:
  - Test LiveCell state changes
  - Test neighbor counting logic
  - Test evolution rules (known patterns)
  - Test configuration methods
- [ ] Use `unittest` or `pytest`
- [ ] Run tests and ensure all pass

**Learning Objective**: Unit testing for Model layer

**Files**: `test_model.py`

---

### Step 6.6: Unit Testing - View Components
- [ ] Create `test_view.py` (optional, GUI testing is complex):
  - Test coordinate conversions
  - Test color configurations
  - Mock tests for display methods
- [ ] Run tests

**Learning Objective**: Testing View layer (limited for GUI)

**Files**: `test_view.py`

---

### Step 6.7: Integration Testing
- [ ] Create `test_integration.py`:
  - Test Model-View-Controller interaction
  - Test complete user workflows:
    - Start → Random → Evolve → Stop
    - Click cells → Evolve
    - Clear → Cannon → Evolve
- [ ] Run tests

**Learning Objective**: Testing component integration

**Files**: `test_integration.py`

---

### Step 6.8: Performance Optimization
- [ ] Profile the application:
  - Identify slow methods (likely evolution or display)
  - Optimize neighbor counting
  - Optimize grid display
  - Consider using NumPy for large grids
- [ ] Test performance improvements

**Learning Objective**: Code optimization

---

### Step 6.9: Error Handling
- [ ] Add error handling:
  - Invalid cell coordinates
  - Invalid configuration parameters
  - File I/O errors (if save/load implemented)
  - GUI errors
- [ ] Use try-except blocks appropriately
- [ ] Test error scenarios

**Learning Objective**: Robust error handling

---

### Step 6.10: Final Code Cleanup
- [ ] Remove debug prints
- [ ] Remove unused imports
- [ ] Remove commented-out code
- [ ] Ensure consistent naming conventions
- [ ] Run linter (pylint, flake8)
- [ ] Format code (black, autopep8)

**Learning Objective**: Code cleanliness

---

## Phase 7: Final Submission

### Step 7.1: Verify All Requirements
- [ ] Check all required files exist:
  - `liveview.py`
  - `livemodel.py`
  - `livecontroller.py`
  - `livecounter.py`
  - `main.py`
- [ ] Verify MVC architecture is properly implemented
- [ ] Verify all required features work:
  - MVC separation
  - Color customization
  - Random configuration
  - Iterator pattern
  - Strategy pattern (bonus)
  - Cell colors by neighbor count

**Learning Objective**: Requirement verification

---

### Step 7.2: Create README
- [ ] Create `README.md` with:
  - Project description
  - How to run the application
  - Controls/usage instructions
  - Features implemented
  - Design patterns used
  - Known issues/limitations
  - Future improvements

**Learning Objective**: Project documentation

---

### Step 7.3: Create Architecture Diagram
- [ ] Document your MVC architecture:
  - Create diagram showing classes and relationships
  - Show Model-View-Controller connections
  - Show Observer pattern implementation
  - Show other design patterns
- [ ] Can be hand-drawn or using tools (draw.io, PlantUML)

**Learning Objective**: Architecture documentation

---

### Step 7.4: Final Testing
- [ ] Run complete application multiple times
- [ ] Test all features thoroughly
- [ ] Test edge cases (empty grid, full grid, small patterns)
- [ ] Test long-running simulations
- [ ] Ensure no crashes or errors

**Learning Objective**: Quality assurance

---

### Step 7.5: Prepare Submission
- [ ] Organize files in clean directory structure
- [ ] Ensure all files are properly named
- [ ] Remove any non-required files
- [ ] Create archive for submission if needed
- [ ] Double-check submission requirements

**Learning Objective**: Professional submission preparation

---

## Summary Checklist

### Core Requirements
- [ ] MVC Architecture properly implemented
- [ ] Model: LiveModel with cell matrix, evolution logic
- [ ] View: LiveView with LiveCanvas and LiveCommandBar
- [ ] Controller: LiveController handling all events
- [ ] Private/protected attributes with accessors
- [ ] Inheritance & polymorphism (cell types)
- [ ] Composition (grid of cells)

### Design Patterns
- [ ] Iterator Pattern (canvas display)
- [ ] Observer Pattern (model notifies controller)
- [ ] Strategy Pattern (configurations) - BONUS
- [ ] Singleton Pattern (optional)
- [ ] Factory Pattern (optional for cell types)

### Features
- [ ] Start/Stop animation
- [ ] Step-by-step evolution
- [ ] Clear grid
- [ ] Random configuration (25% alive)
- [ ] Cannon configuration (Glider Gun)
- [ ] Click to toggle cells
- [ ] Color customization
- [ ] Cell colors by neighbor count
- [ ] Generation counter display

### Code Quality
- [ ] All attributes private/protected
- [ ] Methods ordered correctly
- [ ] Documentation (docstrings)
- [ ] Magic methods where appropriate
- [ ] Unit tests
- [ ] No global variables accessed in classes
- [ ] Clean, readable code

---

## Tips for Success

1. **Work incrementally**: Complete each step before moving to the next
2. **Test frequently**: Test after each small change
3. **Commit often**: Use git to save your progress
4. **Refer to OOP_REFERENCE.md**: Check patterns and examples
5. **Study MvcSample_oop.py**: Use it as a reference for MVC structure
6. **Ask questions**: If stuck, review the procedural version for logic
7. **Start simple**: Get basic functionality working before adding patterns
8. **Refactor gradually**: Don't try to make it perfect on first pass

---

## Estimated Time per Phase

- Phase 0 (Setup): 1-2 hours
- Phase 1 (Model): 4-6 hours
- Phase 2 (View): 4-6 hours
- Phase 3 (Controller): 3-4 hours
- Phase 4 (Patterns): 3-4 hours
- Phase 5 (Features): 2-4 hours
- Phase 6 (Quality): 2-3 hours
- Phase 7 (Submission): 1-2 hours

**Total**: 20-31 hours

---

## References

- `OOP_REFERENCE.md` - OOP concepts and patterns from course
- `GameOfLife_procedural.py` - Functional requirements
- `MvcSample_oop.py` - MVC structure example
- `GameOfLife_MvcArchitecture.png` - Target architecture
- [Conway's Game of Life - Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

---

**Good luck with your project! Take it step by step and you'll build a great OOP application.**
