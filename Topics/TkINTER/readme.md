## TkInter Programs

TkInter programs use many additional packages beyond the TkInter module. A typical inclusion list in most programs is as shown below. 

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
<code>TkInter</code> package is dependent on <code>tk</code>. So, we need to install it using <code>apt install python3-tk</code>
Next, we will need to install them using pip in a virtual Python environment called <code>venv</code>. <code>Pop3</code> is the installer. The pip-installer is installed using the following command 
<br>
`sudo apt install python3-pip`
<br>
It depends on the `dnf` package, which also needs to be installed using the apt installer. The sequence of installation steps leading up to venv activation is as follows.
  
- <code>apt install python3-tk</code>
- `sudo apt install dnf`
- `sudo apt install python3-pip`
- `sudo apt install python3-venv`

Once the environment is installed, link it with the Python project directory using the command:
<br>
<code>python3 -m venv /home/path-to_python-project/</code>
<br>
Then the environment can be activated from the project directory by <code>source bin/activate</code>. Only other package outside pip installation ambit is 'PIL`. It is a part of a package called <code>pillow</code>.
