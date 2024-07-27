# from tkinter import Tk, simpledialog

# class UIHandler:
#     def input_id(self):
#         root = Tk()
#         root.withdraw()  # Hide the main window
#         id_to_delete = simpledialog.askinteger("Input", "Enter the ID of the bounding box to delete:")
#         root.destroy()
#         return id_to_delete

from tkinter import Tk, simpledialog

class UIHandler:
    def input_id(self):
        root = Tk()
        root.withdraw()  # Hide the main window
        id_to_delete = simpledialog.askinteger("Input", "Enter the ID of the bounding box to delete:")
        root.destroy()
        return id_to_delete
