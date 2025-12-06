import tkinter as tk
from PIL import Image, ImageTk
from decimal import Decimal, InvalidOperation
import os
import sys

# ------------------ CALCULATOR CLASS ------------------

class ImageCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Calculator")
        self.root.resizable(False, False)

        # Load button background image
        self.button_img = Image.open("bg.png").resize((90, 60))
        self.button_photo = ImageTk.PhotoImage(self.button_img)

        # Load display background image
        self.display_img = Image.open("bg.png").resize((360, 80))
        self.display_photo = ImageTk.PhotoImage(self.display_img)

        root.maxsize(390, 460)
        root.minsize(390, 460)

        # State variables
        self.display_value = "0"
        self.first = None
        self.op = None
        self.reset_next = False

        # Display Label (with background image)
        self.display_frame = tk.Label(
            root,
            image=self.display_photo,
            compound="center",
            font=("Arial", 28, "bold"),
            fg="black",      # HIGH CONTRAST
            text=self.display_value
        )
        self.display_frame.grid(row=0, column=0, columnspan=4)

        # Buttons layout (AC added)
        layout = [
            ["AC", "", "", ""],        # AC row
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
        ]

        for r, row in enumerate(layout):
            for c, char in enumerate(row):
                if char != "":
                    self.make_button(char, r + 1, c)

        # Bind the window close event to open a new instance
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- BUTTON MAKER ----------------
    def make_button(self, text, row, col):
        btn = tk.Button(
            self.root,
            image=self.button_photo,
            compound="center",
            text=text,
            fg="black",         # HIGH CONTRAST TEXT
            font=("Arial", 18, "bold"),
            borderwidth=0,
            command=lambda t=text: self.on_press(t)
        )
        btn.grid(row=row, column=col, padx=2, pady=2)

    # ---------------- DISPLAY UPDATE ----------------
    def update_display(self):
        self.display_frame.config(text=self.display_value)

    # ---------------- BUTTON PRESS HANDLER ----------------
    def on_press(self, key):

        # -------- AC BUTTON --------
        if key == "AC":
            self.display_value = "0"
            self.first = None
            self.op = None
            self.reset_next = False
            self.update_display()
            return

        # -------- DIGITS --------
        if key.isdigit():
            if self.reset_next:
                self.display_value = key
                self.reset_next = False
            else:
                self.display_value = (
                    key if self.display_value == "0" else self.display_value + key
                )
            self.update_display()
            return

        # -------- DECIMAL --------
        if key == ".":
            if self.reset_next:
                self.display_value = "0."
                self.reset_next = False
            elif "." not in self.display_value:
                self.display_value += "."
            self.update_display()
            return

        # -------- OPERATORS --------
        if key in ["+", "-", "*", "/"]:
            try:
                self.first = Decimal(self.display_value)
            except:
                self.first = Decimal(0)
            self.op = key
            self.reset_next = True
            return

        # -------- EQUALS --------
        if key == "=":
            if self.op is None:
                return

            try:
                second = Decimal(self.display_value)
                result = self.apply_op(self.first, second, self.op)

                # Format result cleanly
                result_str = str(result).rstrip("0").rstrip(".")
                self.display_value = result_str if result_str != "" else "0"

            except:
                self.display_value = "Error"

            self.update_display()
            self.reset_next = True

    # ---------------- OPERATION LOGIC ----------------
    def apply_op(self, a, b, op):
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/":
            if b == 0:
                raise ZeroDivisionError
            return a / b

    # ---------------- CLOSE HANDLER ----------------
    def on_close(self):
        # Close the current window
        self.root.destroy()
        # Reopen a new instance of the calculator
        os.system(f"python {sys.argv[0]}")

# ------------------ RUN ------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")  # Set window size to fit image
    app = ImageCalculator(root)
    root.mainloop()
