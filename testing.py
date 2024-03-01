from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QMainWindow # importing PyQt5 modules. So we can use the GUI functionality of PyQt5.
from PyQt5.QtCore import QTimer, QTime # This allows us to display the time in the GUI.
from PyQt5.QtGui import QPalette, QColor # This allows us to change the background color of the GUI.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # This allows us to display the figure in the GUI by using the canvas.
from matplotlib.figure import Figure # FigureCanvasQTAgg is the canvas to display the figure.
from random import randint # For generating a random array
import sys # mporting the sys module.
import time


# ---------------------- Algorithms ----------------------
def insertion_sort(arr, key=lambda x: x):
    for i in range(1, len(arr)): # for i in range from 1 to the length of the array
        key_value = arr[i] # set key_value to the value at index i
        j = i - 1 
        while j >= 0 and key(arr[j]) > key_value: # while j is greater than 0 and the key of the element at index j is greater than the key of the element at index i
            arr[j + 1] = arr[j] # set the element at index j + 1 to the element at index j
            j -= 1 # decrement j
            yield arr.copy() # return the current state of the array

        arr[j + 1] = key_value # set the element at index j + 1 to the key_value
        yield arr.copy() # return the current state of the array

def merge_sort(arr, key=lambda x: x):
    if len(arr) > 1: # if the length of the array is greater than 1 then 
        mid = len(arr) // 2 # divide the array into 2
        L, R = arr[:mid], arr[mid:] # set L to the first half of the array and R to the second half
        yield from merge_sort(L, key)  # call the merge_sort function on the first half
        yield from merge_sort(R, key)  # call the merge_sort function on the second half

        i = j = k = 0 
        while i < len(L) and j < len(R): # while i is less than the length of L and j is less than the length of R 
            if key(L[i]) < key(R[j]): # if the key of the element in L is less than the key of the element in R
                arr[k] = L[i] # set arr[k] to the element in L
                i += 1 # increment i
            else:
                arr[k] = R[j] # set arr[k] to the element in R
                j += 1  # increment j
            k += 1 # increment k
            yield arr.copy() # return the current state of the array

        while i < len(L): # while i is less than the length of L
            arr[k] = L[i] # set arr[k] to the element in L
            i += 1 # increment i
            k += 1 # increment k
            yield arr.copy() # return the current state of the array

        while j < len(R): # while j is less than the length of R
            arr[k] = R[j] # set arr[k] to the element in R
            j += 1 # increment j
            k += 1 # increment k
            yield arr.copy() # return the current state of the array

def quick_sort(arr, key=lambda x: x): #
    if len(arr) <= 1: # if the length of the array is less than or equal to 1, return the array
        return arr

    pivot = arr[0] # set the pivot to the first element of the array
    less = [x for x in arr[1:] if key(x) <= key(pivot)] # set less to all elements in the array that are less than or equal to the pivot
    greater = [x for x in arr[1:] if key(x) > key(pivot)] # set greater to all elements in the array that are greater than the pivot

    # yield from quick_sort(less) + [pivot] + quick_sort(greater)
    yield from quick_sort(less, key)  
    yield [pivot] 
    yield from quick_sort(greater, key) 

    arr.clear() # this is the same as arr = []
    arr.extend(less + [pivot] + greater) # this is the same as arr = less + [pivot] + greater
    yield arr.copy() # return the current state of the array

class RunningTimesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algorithm Running Times")
        self.setGeometry(100, 100, 640, 480)  # Set window size and position

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter array size:")
        self.layout.addWidget(self.label)

        self.text_box = QLineEdit()
        self.layout.addWidget(self.text_box)

        self.button = QPushButton("Update Running Times")
        self.button.clicked.connect(self.display_running_times)
        self.layout.addWidget(self.button)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def display_running_times(self):
        array_size = int(self.text_box.text()) if self.text_box.text().isdigit() else 500  # Default to 500 if input is invalid

        self.figure.clear()

        # Prepare the subplot
        ax = self.figure.add_subplot(111)
        ax.set_title('Running Times of Sorting Algorithms')
        ax.set_ylabel('Time (seconds)')
        ax.set_xlabel('Algorithm')

        # Generate a random array
        random_array = [randint(0, 100) for _ in range(array_size)]

        # Dictionary to hold execution times
        execution_times = {}

        # Run and time each sorting algorithm
        for algo_name, algo_func in [('Insertion Sort', insertion_sort),
                                     ('Merge Sort', merge_sort),
                                     ('Quick Sort', quick_sort)]:
            start_time = time.perf_counter()
            list(algo_func(random_array.copy(), key=lambda x: x))  # Run and exhaust the generator
            end_time = time.perf_counter()
            execution_times[algo_name] = end_time - start_time

        # Plotting
        algorithms = list(execution_times.keys())
        times = list(execution_times.values())
        ax.bar(algorithms, times, color=['blue', 'green', 'red'])

        self.canvas.draw()
# ---------------------- GUI ----------------------
class MainWindow(QWidget):
    def __init__(self): # creating a class that inherits from QWidget.
        super().__init__() # calling the constructor of the parent class

        self.layout = QVBoxLayout() # creates 'Window' for where GUI will be displayed.

        self.label = QLabel("Enter array size:") # creates prompt for user to enter array size.
        self.layout.addWidget(self.label) # adds the label to the layout 'Window'.

        self.text_box = QLineEdit() # creates a text box for user input.
        self.layout.addWidget(self.text_box) # adds the text box to the layout 'Window'.

        self.algorithm_combo = QComboBox() # creates a combo box for user to choose sorting algorithm.
        self.algorithm_combo.addItems(['Insertion Sort', 'Merge Sort', 'Quick Sort']) # adds the sorting algorithms to the combo box.
        self.layout.addWidget(self.algorithm_combo) # adds the combo box to the layout 'Window'.

        self.button = QPushButton("Sort Array") # creates a button for user to click to sort array.
        self.button.clicked.connect(self.animate_sort) # connects the button to a function.
        self.layout.addWidget(self.button) # adds the button to the layout 'Window'.

        self.pause_button = QPushButton("Pause") # creates a button for user to pause the animation.
        self.pause_button.clicked.connect(self.pause_animation) # connects the button to a function.
        self.layout.addWidget(self.pause_button) # adds the button to the layout 'Window'.

        self.resume_button = QPushButton("Resume") # creates a button for user to resume the animation.
        self.resume_button.clicked.connect(self.resume_animation) # connects the button to a function.
        self.layout.addWidget(self.resume_button) # adds the button to the layout 'Window'.

        self.running_times_button = QPushButton("Show Running Times") # creates a button for user to view the running times of the algorithms.
        self.running_times_button.clicked.connect(self.show_running_times) # connects the button to a function.
        self.layout.addWidget(self.running_times_button) # adds the button to the layout 'Window'.

        self.execution_time_label = QLabel("Total Execution Time: ") # creates a label to display the total execution time.
        self.layout.addWidget(self.execution_time_label) # adds the label to the layout 'Window'.

        self.figure = Figure() # creates a figure.
        self.canvas = FigureCanvas(self.figure) # creates a canvas to display the figure.
        self.layout.addWidget(self.canvas) # adds the canvas to the layout 'Window'.

        self.setLayout(self.layout) # sets the layout 'Window'

        self.array_size = 0 # stores the size of the array
        self.array_list = [] # stores the list of elements in the array

        self.timer = QTimer(self) # creates a timer
        self.start_time = None # stores the start time of the animation

        self.generator = None # stores the generator that is used to generate the array

# ---------------------- Helper Functions ----------------------
    def show_running_times(self):
        self.running_times_window = RunningTimesWindow()
        self.running_times_window.show()    
    
    def generate_random_array(self): # generates a random array
        self.array_size = int(self.text_box.text()) # gets the text from the text box and converts it to an integer
        self.array_list = [randint(0, 50) for _ in range(self.array_size)] # generates a list of random numbers with values between 0 and 50

    def animate_sort(self): # function to animate the sorting
        self.generate_random_array() # generates a random array

        sorting_algorithms = { # dictionary of sorting algorithms
            'Insertion Sort': insertion_sort,
            'Merge Sort': merge_sort,
            'Quick Sort': quick_sort,
        }

        algo_name = self.algorithm_combo.currentText() # gets the name of the sorting algorithm from the combo box
        algorithm_func = sorting_algorithms[algo_name] # gets the function of the sorting algorithm from the dictionary
        self.generator = algorithm_func(self.array_list.copy(), key=lambda x: x) # creates a generator for the sorting algorithm

        self.figure.clear() # clears the figure
        ax = self.figure.add_subplot(111) # adds a subplot to the figure
        ax.set_xlabel('Algorithm')                          # sets the x-axis label.
        ax.set_ylabel('Time (s)')                           # sets the y-axis label.
        bars = ax.bar(range(len(self.array_list)), self.array_list, align="edge", width=0.8) # creates a bar chart with the array list as the height of the bars
        ax.set_xlim(0, len(self.array_list)) # sets the x-axis limits
        ax.set_ylim(0, int(1.1 * max(self.array_list))) # sets the y-axis limits
        ax.set_title("Algorithm : " + algo_name ,
                    fontdict={'fontsize': 12, 'fontweight': 'medium', 'color': '#E4365D'}) # sets the title of the chart
        text = ax.text(0.01, 0.95, "", transform=ax.transAxes, color="#E4365D")
        iteration = [0] # stores the number of iterations

        self.start_time = QTime.currentTime() # get the current time

        def animate(frame): # frame is the current state of the array
            for rect, val in zip(bars, frame): # zip combines the two lists
                rect.set_height(val) # set the height of the bar to the value of the current state of the array
            iteration[0] += 1
            text.set_text("iterations : {}".format(iteration[0]))
            self.canvas.draw() # redraw the canvas

        def execution_time(): # function to get the execution time
            try:
                A = next(self.generator) # get the next state of the array
                animate(A)
            except StopIteration: # if the array is empty
                self.timer.stop() # stop the timer
                elapsed_time = self.start_time.elapsed() / 1000.0  # Convert to seconds
                self.execution_time_label.setText(f"Total Execution Time: {elapsed_time:.6f} seconds")

        self.timer.timeout.connect(execution_time) # connect the timer to the execution_time function
        self.timer.start(50) # start the timer

    def pause_animation(self): # function to pause the animation
        self.timer.stop()

    def resume_animation(self): # function to resume the animation
        if self.generator:
            self.timer.start(50)

# ---------------------- Main ----------------------
# Existing main block...
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())