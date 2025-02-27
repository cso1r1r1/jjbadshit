#Easy to use cordinate "checker" for height reroll script.

import tkinter as tk
from tkinter import messagebox

class CoordinateSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("jjbad selectorxdlol")

        self.root.attributes("-fullscreen", True)

        self.root.attributes("-alpha", 0.7)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()


        self.canvas = tk.Canvas(root, bg="lightgray", width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)


        self.label_top_left = tk.Label(root, text="Top Left (X, Y): (0, 0)", fg="white", bg="black")
        self.label_top_left.pack(side=tk.TOP, anchor="w")

        self.label_width_height = tk.Label(root, text="Width, Height: (0, 0)", fg="white", bg="black")
        self.label_width_height.pack(side=tk.TOP, anchor="w")


        self.instruction_label = tk.Label(root, text="Click and drag to select a box on the screen.", fg="white", bg="black")
        self.instruction_label.pack(side=tk.TOP, anchor="w")


        self.center_text = tk.Label(root, text="PRESS ESCAPE TO CLOSE", font=("Helvetica", 20), fg="white", bg="black")
        self.center_text.place(relx=0.5, rely=0.5, anchor="center")  # Position in the center


        self.start_x = None
        self.start_y = None
        self.rect = None
        self.is_drawing = False

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)


        self.root.bind("<Escape>", self.close_program)

    def on_button_press(self, event):
        """Start drawing the rectangle."""
        self.start_x = event.x
        self.start_y = event.y
        self.is_drawing = True


        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)

    def on_mouse_drag(self, event):
        """Update rectangle size as the user drags the mouse."""
        if self.is_drawing:

            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
            
            self.update_coordinates(event.x, event.y)

    def on_button_release(self, event):
        """Finish drawing the rectangle."""
        self.is_drawing = False
        self.update_coordinates(event.x, event.y)

        print(f"Selected area: ({self.start_x}, {self.start_y}) to ({event.x}, {event.y})")
        messagebox.showinfo("Coordinates", f"Top Left: ({self.start_x}, {self.start_y})\nWidth, Height: ({event.x - self.start_x}, {event.y - self.start_y})")

    def update_coordinates(self, end_x, end_y):
        """Update the displayed coordinates (X, Y, Width, Height)."""
        width = end_x - self.start_x
        height = end_y - self.start_y

        self.label_top_left.config(text=f"Top Left (X, Y): ({self.start_x}, {self.start_y})")
        self.label_width_height.config(text=f"Width, Height: ({width}, {height})")

    def close_program(self, event=None):
        """Close the program when Escape key is pressed."""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    coord_selector = CoordinateSelector(root)
    root.mainloop()
