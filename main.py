import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class PageManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page UI")
        self.geometry("600x600")  # Fixed window size
        self.resizable(False, False)  # Make the window non-resizable

        self.container = tk.Frame(self, width=600, height=600)
        self.container.pack(fill="both", expand=True)

        self.pages = {}  # Store different pages

        for PageClass in (MainPage, Page1, Page2, Page3, Page4):
            page = PageClass(self.container, self)
            self.pages[PageClass] = page
            page.place(x=0, y=0, width=600, height=600)

        self.show_page(MainPage)  # Show main page initially

    def show_page(self, page_class):
        """Switch between pages."""
        page = self.pages[page_class]
        page.tkraise()

class ImagePage(tk.Frame):
    def __init__(self, parent, controller, bg_color, title):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=bg_color)

        # Center the label
        label = tk.Label(self, text=title, font=("Arial", 16), bg=bg_color)
        label.place(relx=0.5, rely=0.1, anchor="center")

        # Reserved space for the image
        self.image_label = tk.Label(self, bg="white", relief="solid")
        self.image_label.place(relx=0.5, rely=0.4, anchor="center")

        # Upload button
        upload_btn = tk.Button(self, text="Upload Image", command=self.upload_image)
        upload_btn.place(relx=0.35, rely=0.7, anchor="center")

        # Delete button
        delete_btn = tk.Button(self, text="Delete Image", command=self.delete_image)
        delete_btn.place(relx=0.65, rely=0.7, anchor="center")

        # Back button
        back_btn = tk.Button(self, text="Back to Main", command=lambda: controller.show_page(MainPage))
        back_btn.place(relx=0.5, rely=0.9, anchor="center")

        self.current_image = None
        self.image_path = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path)

            # Ensure the image fits within the reserved space, scaling proportionally
            max_width, max_height = 300, 300
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            self.current_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_image, width=img.width, height=img.height)  # Wrap border around the image
            self.image_label.image = self.current_image  # Keep a reference to avoid garbage collection
            self.image_path = file_path

    def delete_image(self):
        self.image_label.config(image="", width=300, height=300)  # Reset to default size
        self.current_image = None
        self.image_path = None

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # Center the label
        label = tk.Label(self, text="Main Page", font=("Arial", 16), bg="white")
        label.place(relx=0.5, rely=0.3, anchor="center")

        # Center the buttons horizontally
        button_frame = tk.Frame(self, bg="white")
        button_frame.place(relx=0.5, rely=0.7, anchor="center")

        buttons = [
            ("Page 1", Page1),
            ("Page 2", Page2),
            ("Page 3", Page3),
            ("Page 4", Page4),
        ]

        for text, page in buttons:
            btn = tk.Button(button_frame, text=text, command=lambda p=page: controller.show_page(p))
            btn.pack(side="left", padx=10, pady=10)

class Page1(ImagePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="lightgray", title="This is Page 1")

class Page2(ImagePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="lightblue", title="This is Page 2")

class Page3(ImagePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="lightgreen", title="This is Page 3")

class Page4(ImagePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, bg_color="lightyellow", title="This is Page 4")

if __name__ == "__main__":
    app = PageManager()
    app.mainloop()
