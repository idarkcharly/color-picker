import tkinter as tk
import pyautogui
from PIL import Image, ImageTk


class ColorPicker:
    def __init__(self):
        self.selected_color_hex = "#FFFFFF"

        # Create main window
        self.window = tk.Tk()
        self.window.title("Color Picker")
        self.window.geometry("260x160")
        self.window.resizable(False, False)
        self.window.configure(bg="#f8f9fa")
        self.window.attributes("-topmost", True)  # Always on top

        # Label to display the selected color
        self.color_display = tk.Label(
            self.window,
            text=self.selected_color_hex,
            font=("Arial", 12, "bold"),
            width=12,
            height=2,
            bd=3,
            relief="ridge",
            bg=self.selected_color_hex,
            fg="black",
        )
        self.color_display.pack(pady=10)

        # Button container
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.pack(pady=5)

        button_style = {
            "font": ("Arial", 11, "bold"),
            "width": 10,
            "height": 1,
            "relief": "flat",
            "bd": 2,
            "highlightthickness": 1,
            "highlightbackground": "#ddd",
            "highlightcolor": "#ddd",
            "pady": 5,
        }

        # Copy color button
        self.copy_button = tk.Button(
            button_frame,
            text="Copy",
            command=self.copy_color,
            bg="#2bb673",
            fg="white",
            **button_style
        )
        self.copy_button.pack(side="left", padx=5)

        # Pick color button
        self.pick_button = tk.Button(
            button_frame,
            text="Pick",
            command=self.activate_eyedropper,
            bg="#4285F4",
            fg="white",
            **button_style
        )
        self.pick_button.pack(side="left", padx=5)

        self.window.mainloop()

    def activate_eyedropper(self):
        """Freezes the screen and allows color selection with real-time preview."""
        self.window.withdraw()
        self.screenshot = pyautogui.screenshot().convert("RGB")

        # Create color selection window
        self.selector = tk.Toplevel()
        self.selector.attributes("-fullscreen", True)
        self.selector.attributes("-topmost", True)
        self.selector.config(cursor="crosshair")  # Enlarged crosshair cursor
        self.selector.focus_force()

        # Convert screenshot for Tkinter
        self.img_tk = ImageTk.PhotoImage(self.screenshot)
        self.canvas = tk.Canvas(self.selector)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        # Color preview
        self.preview_size = 100
        self.preview_box = self.canvas.create_rectangle(
            0,
            0,
            self.preview_size,
            self.preview_size,
            outline="white",
            width=2,
            fill="white",
        )

        # Events
        self.selector.bind("<Motion>", self.update_color)
        self.selector.bind("<Button-1>", self.capture_color)
        self.selector.bind("<Escape>", self.cancel_selection)

    def update_color(self, event):
        """Updates the real-time color preview and repositions it."""
        x, y = event.x, event.y
        if 0 <= x < self.screenshot.width and 0 <= y < self.screenshot.height:
            color_rgb = self.screenshot.getpixel((x, y))
            color_hex = "#{:02x}{:02x}{:02x}".format(*color_rgb)

            # Update preview background color
            self.canvas.itemconfig(self.preview_box, fill=color_hex)

            # Reposition preview **below and to the right of the cursor**
            preview_x = min(x + 10, self.screenshot.width - self.preview_size)
            preview_y = min(y + 10, self.screenshot.height - self.preview_size)

            self.canvas.coords(
                self.preview_box,
                preview_x,
                preview_y,
                preview_x + self.preview_size,
                preview_y + self.preview_size,
            )

    def capture_color(self, event):
        """Saves the selected color and updates the main window."""
        x, y = event.x, event.y
        self.selected_color_hex = "#{:02x}{:02x}{:02x}".format(
            *self.screenshot.getpixel((x, y))
        )

        # Close selector and update the main window
        self.selector.destroy()
        self.color_display.config(
            text=self.selected_color_hex, bg=self.selected_color_hex
        )
        r, g, b = self.screenshot.getpixel((x, y))
        brightness = r * 0.299 + g * 0.587 + b * 0.114
        text_color = "black" if brightness > 150 else "white"
        self.color_display.config(fg=text_color)

        self.window.deiconify()

    def cancel_selection(self, event=None):
        """Cancels the color selection and closes the selection window."""
        self.selector.destroy()
        self.window.deiconify()

    def copy_color(self):
        """Copies the selected color to the clipboard."""
        self.window.clipboard_clear()
        self.window.clipboard_append(self.selected_color_hex)
        self.window.update()


if __name__ == "__main__":
    ColorPicker()
