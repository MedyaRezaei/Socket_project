import tkinter as tk
from interface.gui.client_gui import ChatClientGUI

if __name__ == '__main__':
    root = tk.Tk()
    gui = ChatClientGUI(root)
    root.mainloop()
