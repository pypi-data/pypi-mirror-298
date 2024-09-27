from tkinter import *


class GUI:
    def __init__(self):
        self.root = None

    def loop_start(self, **kwargs: dict):
        winIcon = kwargs.get("winIcon",'ico/hackerakos.ico')
        winX = kwargs.get("winX",400)
        winY = kwargs.get("winY",400)
        winTitle = kwargs.get("winTitle", "Hackerakos")
        self.boxing = kwargs.get("boxing", "pack")



        winSize = f"{winX}x{winY}"

        self.root = Tk()
        self.root.geometry(winSize)
        self.root.title(winTitle)
        self.root.iconbitmap(winIcon)














        

    def loop_close(self):
        self.root.mainloop()


    def label(self, **kwargs: dict) -> Tk:
        text_str = kwargs.get("text", "")
        var_name = kwargs.get("var_name", "")

        row = kwargs.get("row", 0)
        column = kwargs.get("column", 0)

        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)

        label = Label(self.root, text=text_str)

        if self.boxing == "pack":
            label.pack()
        elif self.boxing == "grid":
            if row == 0 and column == 0:
                print("Please specify a row and column for the grid layout")
            else:
                label.grid(row=row, column=column)
        elif self.boxing == "place":
            label.place(x= x, y= y)
        else:
            print("Invalid layout manager. Please use 'pack' or 'grid' or 'place'.")

        setattr(self, var_name, label)

        return label




#    def add(sel, **kwargs: dict):
#        text_str = kwargs.get("text", "")









# Create a GUI instance
gui = GUI()

# Export the GUI functions
loop_start = gui.loop_start
label = gui.label
loop_close = gui.loop_close