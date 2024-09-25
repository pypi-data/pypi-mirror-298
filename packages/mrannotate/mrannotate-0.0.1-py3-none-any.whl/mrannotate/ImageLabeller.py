import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

def load_tk_image(path: Path, max_width: int, max_height: int) -> ImageTk.PhotoImage:
    img = Image.open(path)
    w, h = img.size
    print(f"{img.size} -> ", end = "")

    if (w / h) >= (max_width / max_height):
        img = img.resize((max_width, int(h * (max_width / w))))
    else:
        img = img.resize((int(w * (max_height / h)), max_height))
    
    print(img.size)
    return ImageTk.PhotoImage(img)

class ImageLabeller():
    def __init__(
        self,
        image_paths: list[str | Path],
        labels: list[str],
        canvas_width: int = 960,
        img_max_height: int = 540
    ) -> None:
        self.image_paths: list[Path] = [Path(img_path) for img_path in image_paths]
        self.labels = labels
        self.img_labels: list[None | int] = [None] * len(self.image_paths)
        self.canvas_width = canvas_width
        self.img_max_height = img_max_height
    
    def run(self):

        window = tk.Tk()
        window.title(f"Image Labeller - {len(self.image_paths)} images, {len(self.labels)} labels")
        window.resizable(False, False)

        img_canvas = tk.Canvas(window, width = self.canvas_width, height = self.img_max_height)
        img_canvas.pack()

        detail_canvas = tk.Canvas(window, width = self.canvas_width, height = 30)
        detail_canvas.pack(pady = 5)

        label_canvas = tk.Canvas(window, width = self.canvas_width, height = 200)
        label_canvas.pack(pady = 10)

        btn_canvas = tk.Canvas(window, width = self.canvas_width, height = 50)
        btn_canvas.pack(pady = 10)

        img_index = 0
        current_label = tk.IntVar()
        current_label.set(None)

        img = load_tk_image(
            self.image_paths[img_index],
            self.canvas_width,
            self.img_max_height
        )
        img_container = img_canvas.create_image(
            self.canvas_width // 2,
            self.img_max_height // 2,
            anchor = tk.CENTER,
            image = img
        )

        img_title = detail_canvas.create_text(
            self.canvas_width // 2,
            15,
            text = self.image_paths[img_index].stem,
            fill = "black",
            font = "Helvetica 14 bold",
            anchor = tk.CENTER
        )

        def update_label():
            nonlocal img, img_index
            self.img_labels[img_index] = current_label.get()
            print(self.img_labels)

            img_index = (img_index + 1) % len(self.image_paths)
            current_label.set(self.img_labels[img_index])
            img = load_tk_image(
                self.image_paths[img_index],
                self.canvas_width,
                self.img_max_height
            )
            img_canvas.itemconfig(img_container, image = img)
            detail_canvas.itemconfig(img_title, text = self.image_paths[img_index].stem)
        
        for i, label in enumerate(self.labels):
            tk.Radiobutton(
                label_canvas,
                text = label,
                indicatoron = 0,
                width = 36, 
                padx = 5,
                pady = 5,
                variable = current_label,
                value = i,
                overrelief = "raised",
                offrelief = "groove",
                font = "Helvetica 11"
            ).grid(
                row = i // 3,
                column = i % 3,
                padx = 10,
                pady = 10
            )
        
        save_btn = tk.Button(
            btn_canvas,
            text = "Save label",
            font = "Helvetica 12 bold",
            width = 24,
            padx = 10,
            pady = 5,
            command = update_label
        )
        save_btn.pack(anchor = tk.N, pady = 10)

        window.mainloop()