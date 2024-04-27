#!/usr/bin/env python
# coding: utf-8

# # SNIPPING TOOL (CAPTURE DOCUMENTS & PICUTRES)

# import libraries 

#     import sys: Imports the sys module, which provides system-specific functionality.
#     from PyQt5.QtWidgets import ...: Imports necessary classes and functions from PyQt5's QtWidgets module for building GUI applications.
#     from PyQt5.QtGui import ...: Imports classes for graphical user interface functionality from PyQt5's QtGui module.
#     from PyQt5.QtCore import ...: Imports core classes and functionalities from PyQt5's QtCore module.
#     from PIL import ImageGrab: Imports the ImageGrab module from PIL (Python Imaging Library) to capture screenshots.
#     import cv2: Imports the OpenCV library for image processing tasks.
#     import numpy as np: Imports the NumPy library for numerical operations.
#     import os: Imports the os module for interacting with the operating system (e.g., file system operations).

# In[1]:


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QRect
from PIL import ImageGrab
import cv2
import numpy as np
import os


# SnippingWidget: Defines a custom widget (QWidget) named SnippingWidget for capturing screen regions.
# num_snip, is_snipping, background: Class-level variables to keep track of the number of snips taken, snipping status, and background state.
# __init__(self, parent=None): Constructor method called when creating an instance of SnippingWidget.
# Sets the window flags to keep the widget on top of other windows (Qt.WindowStaysOnTopHint).
# Retrieves the desktop dimensions to set the widget size to match the screen (screen_width, screen_height).
# Initializes begin and end as QPoint objects to store the starting and ending points of the snipping region.

# In[2]:


class SnippingWidget(QWidget):
    num_snip = 0
    is_snipping = False
    background = True

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        root = QApplication.desktop()
        screen_width = root.width()
        screen_height = root.height()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.begin = QPoint()
        self.end = QPoint()

    def start(self):
        SnippingWidget.background = False
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.3)
        QApplication.setOverrideCursor(Qt.CrossCursor)
        print('Capture the screen...')
        print('Press q if you want to quit...')
        self.show()

    def paintEvent(self, event):
        if SnippingWidget.is_snipping:
            brush_color = QColor(128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            # Reset points, so the rectangle won't show up again.
            self.begin = QPoint()
            self.end = QPoint()
            brush_color = QColor(0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QPainter(self)
        qp.setPen(QPen(Qt.black, lw))
        qp.setBrush(brush_color)
        rect = QRect(self.begin, self.end)
        qp.drawRect(rect)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            print('Quit')
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        SnippingWidget.num_snip += 1
        SnippingWidget.is_snipping = False
        QApplication.restoreOverrideCursor()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.repaint()
        QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img_np = np.array(img)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

        # Specify the directory path to save the image
        save_dir = r"C:\Users\User\Downloads"
        os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists
        
        # Create the filename for the image
        img_filename = os.path.join(save_dir, f"snipp_{SnippingWidget.num_snip}.jpg")

        # Save the image using OpenCV
        cv2.imwrite(img_filename, img_cv)
        print(f"Saved {img_filename}")


# start(self): Method to start the snipping process.
# Updates the snipping status and background state.
# Sets the window opacity to 0.3 for transparency.
# Sets the cursor to a crosshair cursor (Qt.CrossCursor) to indicate snipping mode.
# Prints instructions in the console for capturing the screen.

# paintEvent(self, event): Method to handle painting (drawing) on the widget.
# Checks the is_snipping status to determine the drawing parameters (brush color, line width, opacity).
# Uses QPainter to draw a rectangle (qp.drawRect(rect)) based on the begin and end points.

# This method (keyPressEvent) is an event handler that gets triggered when a key is pressed while the widget has focus.
# It checks if the key pressed is Qt.Key_Q (the 'Q' key on the keyboard).
# If the 'Q' key is pressed, it prints 'Quit' to the console and then closes the widget (self.close()).
# event.accept() indicates that the event has been processed.

# This method (mousePressEvent) is triggered when a mouse button is pressed within the widget.
# It records the position (event.pos()) where the mouse button was pressed as self.begin (start point of selection).
# It sets self.end to the same position as self.begin to initialize the selection.
# self.update() is called to trigger a repaint/update of the widget.

# This method (mouseMoveEvent) is triggered when the mouse is moved within the widget while a mouse button is pressed.
# It continuously updates the self.end position to track the end point of the selection (updating the selection rectangle).
# self.update() is called to repaint/update the widget with the new selection rectangle.

# This method (mouseReleaseEvent) is triggered when a mouse button is released within the widget.
# It finalizes the selection and performs actions to save the selected region as an image.
# Updates the num_snip counter to track the number of snips taken.
# Sets is_snipping to False to indicate that the snipping process is complete.
# Restores the cursor to its default state using QApplication.restoreOverrideCursor().
# Calculates the bounding box (x1, y1, x2, y2) of the selected region.
# Repaints the widget to clear the selection rectangle.
# QApplication.processEvents() ensures any pending events are processed before continuing.
# Captures the screen region (ImageGrab.grab(bbox=(x1, y1, x2, y2))), converts it to a NumPy array (img_np), and then to RGB format (img_cv) using OpenCV.
# Defines the directory path (save_dir) where the image will be saved.
# Creates the filename (img_filename) for the saved image based on the num_snip counter.
# Saves the image to the specified directory using OpenCV's cv2.imwrite.
# Prints a message indicating that the image has been saved

# MainApplication class represents the main application window (QMainWindow) where the GUI elements are displayed.
# 
# __init__(self): Constructor method initializes the main application window.
#         Creates an instance of SnippingWidget (self.snipping_widget) to handle screen capturing.
#         Calls setup_ui() to set up the user interface.
# 
# setup_ui(self): Method to set up the user interface (UI) of the main application window.
#         Sets the window title and geometry (self.setWindowTitle(), self.setGeometry()).
#         Creates buttons (snip_button, quit_button) and a label (save_comment) to display UI elements.
#         Sets up a vertical box layout (layout) to organize the buttons and label vertically.
#         Creates a central widget (central_widget) to hold the layout and sets it as the central widget of the main window.
# 
# start_snipping(self): Method to start the snipping process when the "Start Snipping" button is clicked.
#         Calls the start() method of snipping_widget to initiate the screen capture.
# 
# close_application(self): Method to close the application when the "Quit" button is clicked.
#         Calls self.close() to close the main application window.

# The main entry point of the application.
# Creates an instance of QApplication (app).
# Creates an instance of MainApplication (main_app), which initializes and displays the main application window.
# 
# Enters the main event loop (app.exec_()) to handle application events and execute the GUI application.
# sys.exit() ensures that the application exits cleanly when the event loop exits.

# In[3]:


class MainApplication(QMainWindow):
    def __init__(self):
        super(MainApplication, self).__init__()

        self.snipping_widget = SnippingWidget(self)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Snipping Tool")
        self.setGeometry(200, 200, 300, 200)

        snip_button = QPushButton("Start Snipping", self)
        snip_button.clicked.connect(self.start_snipping)

        quit_button = QPushButton("Quit", self)
        quit_button.clicked.connect(self.close_application)

        save_comment = QLabel("Automatically saved in: C:\\Users\\User\\Downloads", self)

        layout = QVBoxLayout()
        layout.addWidget(snip_button)
        layout.addWidget(quit_button)
        layout.addWidget(save_comment)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_snipping(self):
        self.snipping_widget.start()

    def close_application(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())


# In[ ]:




