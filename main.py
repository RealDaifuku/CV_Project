import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import cv2
import os

class PageManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page UI")
        self.geometry("600x600")  # Fixed window size
        self.resizable(False, False)  # Make the window non-resizable

        self.container = tk.Frame(self, width=600, height=600)
        self.container.pack(fill="both", expand=True)

        self.pages = {}  # Store different pages

        for PageClass in (MainPage, Page1, Page2, Page3, Page4, CameraPage):
            page = PageClass(self.container, self)
            self.pages[PageClass] = page
            page.place(x=0, y=0, width=600, height=600)

        self.show_page(MainPage)  # Show main page initially

    def show_page(self, page_class):
        """Switch between pages."""
        page = self.pages[page_class]
        page.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        label = tk.Label(self, text="Main Page", font=("Arial", 16), bg="white")
        label.place(relx=0.5, rely=0.3, anchor="center")

        button_frame = tk.Frame(self, bg="white")
        button_frame.place(relx=0.5, rely=0.7, anchor="center")

        buttons = [
            ("Page 1", Page1),
            ("Page 2", Page2),
            ("Page 3", Page3),
            ("Page 4", Page4),
            ("Camera Page", CameraPage)
        ]

        for text, page in buttons:
            btn = tk.Button(button_frame, text=text, command=lambda p=page: controller.show_page(p))
            btn.pack(side="left", padx=10, pady=10)

class ImagePage(tk.Frame):
    def __init__(self, parent, controller, bg_color, title):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=bg_color)

        label = tk.Label(self, text=title, font=("Arial", 16), bg=bg_color)
        label.place(relx=0.5, rely=0.1, anchor="center")

        self.image_label = tk.Label(self, bg="white", relief="solid")
        self.image_label.place(relx=0.5, rely=0.4, anchor="center")

        upload_btn = tk.Button(self, text="Upload Image", command=self.upload_image)
        upload_btn.place(relx=0.35, rely=0.7, anchor="center")

        delete_btn = tk.Button(self, text="Delete Image", command=self.delete_image)
        delete_btn.place(relx=0.65, rely=0.7, anchor="center")

        back_btn = tk.Button(self, text="Back to Main", command=lambda: controller.show_page(MainPage))
        back_btn.place(relx=0.5, rely=0.9, anchor="center")

        self.current_image = None
        self.image_path = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path)
            width, height = img.size
            scale_factor = min(500 / width, 300 / height)  # Maintain aspect ratio
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            self.current_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_image)
            self.image_label.image = self.current_image  # Prevent garbage collection
            self.image_label.config(width=new_width, height=new_height)  # Adjust label size
            self.image_path = file_path

    def delete_image(self):
        self.image_label.config(image="", text="", width=0, height=0)
        self.current_image = None
        self.image_path = None

class Page1(ImagePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "lightgray", "This is Page 1")

class Page2(ImagePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "lightblue", "This is Page 2")

class Page3(ImagePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "lightgreen", "This is Page 3")

class Page4(ImagePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "lightyellow", "This is Page 4")

class CameraPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="black")

        self.cap = None
        self.label = tk.Label(self)
        self.label.place(relx=0.5, rely=0.4, anchor="center")

        capture_btn = tk.Button(self, text="Open Camera", command=self.start_camera)
        capture_btn.place(relx=0.3, rely=0.8, anchor="center")

        capture_btn = tk.Button(self, text="Capture Image", command=self.capture_image)
        capture_btn.place(relx=0.5, rely=0.8, anchor="center")

        back_btn = tk.Button(self, text="Back to Main", command=self.close_camera)
        back_btn.place(relx=0.7, rely=0.8, anchor="center")

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.update_frame()

    def update_frame(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((400, 300))
                self.photo = ImageTk.PhotoImage(img)
                self.label.config(image=self.photo)
            self.after(10, self.update_frame)

    def capture_image(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                filename = simpledialog.askstring("Save Image", "Enter filename:")
                if filename:
                    save_path = os.path.join(os.path.expanduser("~"), "Downloads", f"{filename}.png")
                    cv2.imwrite(save_path, frame)
                    messagebox.showinfo("Success", f"Image saved as {save_path}")

    def close_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.controller.show_page(MainPage)

if __name__ == "__main__":
    app = PageManager()
    app.mainloop()
