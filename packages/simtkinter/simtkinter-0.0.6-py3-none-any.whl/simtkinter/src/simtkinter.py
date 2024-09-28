from tkinter import *
from tkinter import colorchooser
from PIL import ImageTk, Image
import requests
from io import BytesIO

def hex_colors_palette():
    color = colorchooser.askcolor()[1]
    print(f"\nSelected color: {color}")









def name_color_chart():
    url = "http://hacker-bin.com/files/simple_tkinter.ico"
    response = requests.get(url)
    img_data = response.content


    temp_icon = "temp.ico"
    with open(temp_icon, "wb") as f:
        f.write(img_data)

    top = Toplevel()
    top.title("Simple Tkinter package name color chart")
    top.resizable(False, False)
    top.iconbitmap(temp_icon)

    # Open the image and resize it
    colors = Image.open("ico/colors.png")
    colors.thumbnail((1500, 1500))

    myImg = ImageTk.PhotoImage(colors)

    label = Label(top, image=myImg)
    label.grid(row=0, column=0)

    top.mainloop()



class GUI:
    def __init__(self):
        self.root = None

    def loop_start(self, **kwargs: dict):

        url = "http://hacker-bin.com/files/simple_tkinter.ico"
        response = requests.get(url)
        img_data = response.content


        temp_icon = "temp.ico"
        with open(temp_icon, "wb") as f:
            f.write(img_data)
    



        winIcon = kwargs.get("winIcon", temp_icon)
        winSize = kwargs.get("winSize","400x400")
        winTitle = kwargs.get("winTitle", "Simple Tkinter")
        self.boxing = kwargs.get("boxing", "pack")



        

        self.root = Tk()
        self.root.geometry(winSize)
        self.root.title(winTitle)
        self.root.iconbitmap(winIcon)






        

    def loop_close(self):
        self.root.mainloop()


    def label(self, **kwargs: dict) -> Tk:
        # Text
        text_str = kwargs.get("text", "This is a text for a label")

        label = Label(self.root, text=text_str)

        # Lable Name
        var_name = kwargs.get("var_name", "")

        # Colors
        #bg
        bc = kwargs.get("bc", "SystemButtonFace")
    
        def bc_valid():
            try:
                label.config(bg=bc)
                return True
            except TclError:
                return False

        if bc_valid():
            label.config(bg=bc)
        else:
            print("\nBackround color is not valid.")


        #fg
        tc = kwargs.get("tc", "SystemButtonText")

        def tc_valid():
            try:
                label.config(fg=tc)
                return True
            except TclError:
                return False

        if tc_valid():
            label.config(fg=tc)
        else:
            print("\Foreground color is not valid.")


        





        # Boxing
        row = kwargs.get("row", 0)
        column = kwargs.get("column", 0)

        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)

        

        if self.boxing == "pack":
            label.pack()
        elif self.boxing == "grid":
            if row == 0 and column == 0:
                print("Specify a row and column for the grid layout")
            else:
                label.grid(row=row, column=column)
        elif self.boxing == "place":
            label.place(x= x, y= y)
        else:
            print("Invalid layout manager. Please use 'pack' or 'grid' or 'place'.")





        setattr(self, var_name, label)

        return label






# Create a GUI instance
gui = GUI()

# Export the GUI functions
loop_start = gui.loop_start
label = gui.label
loop_close = gui.loop_close