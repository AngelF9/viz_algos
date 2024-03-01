from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox # importing PyQt5 modules. So we can use the GUI functionality of PyQt5.
from PyQt5.QtCore import QTimer, QTime # This allows us to display the time in the GUI.
from PyQt5.QtGui import QPalette, QColor # This allows us to change the background color of the GUI.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # This allows us to display the figure in the GUI by using the canvas.
from matplotlib.figure import Figure # FigureCanvasQTAgg is the canvas to display the figure.
from random import randint # For generating a random array
import sys # mporting the sys module.
import random 



# ---------------------- Algorithms ----------------------
def insertion_sort(arr, key=lambda x: x):
    for i in range(1, len(arr)):
        key_value = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) > key_value:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_value
        yield arr.copy() # return the current state of the array


def merge_sort(arr, key=lambda x: x):
    if len(arr) > 1:
        mid = len(arr) // 2
        L, R = arr[:mid], arr[mid:]
        yield from merge_sort(L, key) 
        yield from merge_sort(R, key)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if key(L[i]) < key(R[j]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            yield arr.copy() # return the current state of the array

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            yield arr.copy() # return the current state of the array

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            yield arr.copy() # return the current state of the array

def quick_sort(a, l=0, r=None, key=lambda x: x):
    if r is None:
        r = len(a) - 1
    if l >= r:
        return
    x = a[l]
    j = l
    for i in range(l + 1, r + 1):
        if key(a[i]) <= key(x):
            j += 1
            a[j], a[i] = a[i], a[j]
        yield a
    a[l], a[j]= a[j], a[l]
    yield a
 
    # yield from statement used to yield 
    # the array after dividing
    yield from quick_sort(a, l, j-1)
    yield from quick_sort(a, j + 1, r)
"""def quick_sort(arr, low=0, high=None, key=lambda x: x):
    if high is None:
        high = len(arr) - 1
    if high - low > 0:
        pi = partition(arr, low, high, key)
        yield from quick_sort(arr, low, pi - 1, key)
        yield from quick_sort(arr, pi + 1, high, key)
    yield arr

def partition(arr, low, high, key):
    pivot_index = random.randint(low, high)
    arr[high], arr[pivot_index] = arr[pivot_index], arr[high]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if key(arr[j]) <= key(pivot):
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1"""

# ---------------------- GUI ----------------------
class MainWindow(QWidget):  # creating a class that inherits from QWidget.
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()                         # creates 'Window' for where GUI will be displayed.

        self.label = QLabel("Enter array size:")            # creates prompt for user to enter array size.
        self.layout.addWidget(self.label)                   # adds the label to the layout 'Window'.

        self.text_box = QLineEdit()                         # creates a text box for user input.
        self.layout.addWidget(self.text_box)                # adds the text box to the layout 'Window'.

        self.button = QPushButton("Sort Array")             # creates a button for user to click to sort array.
        self.button.clicked.connect(self.animate_sort)   # connects the button to a function.
        self.layout.addWidget(self.button)                  # adds the button to the layout 'Window'.

        self.execution_time_label = QLabel("Total Execution Time: ") # creates a label to display the total execution time.
        self.layout.addWidget(self.execution_time_label) # adds the label to the layout 'Window'.

        self.figure = Figure()                              # creates a figure.
        self.canvas = FigureCanvas(self.figure)             # creates a canvas to display the figure.
        self.layout.addWidget(self.canvas)                  # adds the canvas to the layout 'Window'.

        self.setLayout(self.layout)                         # sets the layout of the window.               

        self.array_size = 0
        self.array_list = []
        self.timer = QTimer(self)
        self.start_time = None

# ---------------------- Helper Functions ----------------------
    def animate(self, arr): # function to animate the sorting
        self.figure.clear()                                 # clears the figure.
        ax = self.figure.add_subplot(111)                   # adds a subplot to the figure.
        ax.bar(range(len(arr)), arr, color='b')             # creates a bar chart with the array values.
        self.canvas.draw()   
    
    def start_next_sort(self):
        self.current_algorithm_index += 1
        if self.current_algorithm_index < len(self.sorting_algorithms):
            algo_name, algo_func = self.sorting_algorithms[self.current_algorithm_index]
            self.setWindowTitle(algo_name)  # set the window title to the name of the current sorting algorithm
            self.generator = algo_func(self.array_list.copy(), key=lambda x: x)
            self.figure.clear()                                 # clears the figure.
            # ... rest of the code to initialize the plot ...
            self.start_time = QTime.currentTime()
            self.timer.start(1000) # start the timer
        else:
            self.timer.stop()                               # draws the canvas.

    def generate_random_array(self): # generates a random array
        self.array_size = int(self.text_box.text()) # gets the text from the text box and converts it to an integer
        self.array_list = [randint(0, 50) for _ in range(self.array_size)] # generates a list of random numbers with values between 0 and 50        

    def animate_sort(self): # function to animate the sorting
        self.generate_random_array() # generates a random array

        self.sorting_algorithms = [
            ('Insertion Sort', insertion_sort),
            ('Merge Sort', merge_sort),
            ('Quick Sort', quick_sort),
        ]
        self.current_algorithm_index = -1
        
        def execution_time():
            try:
                A = next(self.generator)
                self.animate(A)
            except StopIteration:
                elapsed_time = self.start_time.elapsed() / 1000.0  # Convert to seconds
                self.execution_time_label.setText(f"Total Execution Time: {elapsed_time:.6f} seconds")
                self.start_next_sort()

        self.timer.timeout.connect(execution_time) # connect the timer to the execution_time function

        self.start_next_sort() # start the first sorting algorithm



# ---------------------- Main ----------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())