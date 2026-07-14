## TkInter Programs

TkInter programs use many additional packages beyond the TkInter module. A typical inclusion list in most programs is shown below. 

<code> 
import tkinter as tk
from linkedListOps import LinkedList # Import linked list class
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox as mb 
from array import array
import os
import fitz 
import time
from PIL import Image, ImageTk
</code>
<br>

<code>TkInter</code> package is dependent on <code>tk</code>. First, we need to install it using <code>apt install python3-tk</code>. To install a Python module inside the virtual environment code>venv</code>, we <code>pip</code> installer. It is installed using the following command 
<br>
`sudo apt install python3-pip`
<br>
<code>Pip</code> depends on the `dnf` package, which also needs to be installed using the apt installer. The sequence of installation steps leading up to `venv` activation is as follows.
<br>
- <code>apt install python3-tk</code>
- `sudo apt install dnf`
- `sudo apt install python3-pip`
- `sudo apt install python3-venv`


After installing the virtual environment, link it with the Python project directory using the command:
<br>
<br>
<code>python3 -m venv /home/path-to_python-project/</code>
<br>
<br>
Then the environment can be activated from the project directory by <code>source bin/activate</code>. The pip-installer can then install all other Python packages from the safe environment. The typical installation steps are:
<br>
<code>
pip install fitz # module for importing PyMuPDF
pip install PyMuPDF # installs PDF viewer
pip3 install Pillow # installs Image package
</code>

The idea behind installing a Micro PDF viewer is to provide a brief explanation of the PDF's data structure before the user begins exploring the animation. This way we can let the user make the connection between the animation and the organization of a specific data structure.

The code is organized into directories, one for the animation of a separate data structure. Most programs have three basic files: one defines the class for the data representation and the implementation of the allowable operations, the second for the animation of the operations, and the third a PDF file explaining the data structure and the associated animation program. 
