# image processing
from PIL import Image, ImageTk
import cv2

# gui
import tkinter as tk
from tkinter import filedialog, ttk

# maths
import numpy as np


# main_App class
class My_Image_App:
    def __init__(self, root):
        # define root
        self.root = root
        # title
        self.root.title("Image Processing APP")
        
        # Variables define for app

        self.my_original_image = None

        # display
        self.my_display_image = None
        
        # crop
        self.my_cropped_image = None
        self.crop_start = None

        # rect
        self.current_crop_rect = None
        
        self.temp_image = None
        
        # Create GUI of app
        self.App_create_widgets()
        
    def App_create_widgets(self):
        # image display Frame
        self.my_image_frame = tk.Frame(self.root)
        
        self.my_image_frame.pack(pady=10)
        # Original image label's canvas 
        self.my_original_canvas = tk.Canvas(self.my_image_frame, width=500, height=400, bg='gray')
        self.my_original_canvas.pack(side=tk.LEFT, padx=10)
        # Original to be None
        self.original_image_on_canvas = None
        
        # Lable of Cropped image
        self.cropped_label = tk.Label(self.my_image_frame)
        self.cropped_label.pack(side=tk.LEFT, padx=10)
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=10)
        
        # button of load,save and slider
        self.load_button = tk.Button(self.controls_frame, text="Load My Image", command=self.load_my_image)
        self.load_button.pack(side=tk.LEFT, padx=6)
        self.save_button = tk.Button(self.controls_frame, text="Save My Image", command=self.save_my_image)
        self.save_button.pack(side=tk.LEFT, padx=6)
        self.resize_label = tk.Label(self.controls_frame, text="Resize My Image:")
        self.resize_label.pack(side=tk.LEFT, padx=6)
        self.resize_slider = ttk.Scale(self.controls_frame, from_=10, to=200, value=100, 
                                     command=self.resize_my_image)
        self.resize_slider.pack(side=tk.LEFT, padx=6)
        self.resize_value_label = tk.Label(self.controls_frame, text="100%")
        self.resize_value_label.pack(side=tk.LEFT)
        
        # Bind mouse events for cropping
        self.my_original_canvas.bind("<ButtonPress-1>", self.start_image_croping)
        self.my_original_canvas.bind("<B1-Motion>", self.update_image_croping)
        self.my_original_canvas.bind("<ButtonRelease-1>", self.end_my_image_scrop)
    
    def load_my_image(self):
        # load image from device
        my_file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        self.my_original_image = cv2.imread(my_file_path)
        self.my_display_image = self.my_original_image.copy()
        self.show_my_original_image()
        self.cropped_label.config(image='')
        self.current_crop_rect = None
        self.crop_start = None
    
    def show_my_original_image(self):
       
        # BGR  to RGB conversion
        image_rgb = cv2.cvtColor(self.my_original_image, cv2.COLOR_BGR2RGB)
        my_pil_image = Image.fromarray(image_rgb)
        # Aspect ratio of image calculate 
        img_width, img_height = my_pil_image.size
        canvas_width = self.my_original_canvas.winfo_width()
        canvas_height = self.my_original_canvas.winfo_height()
        scale = min(canvas_width/img_width, canvas_height/img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        # In canvas fit the rize image
        my_pil_image = my_pil_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Imge into Tkinter's format
        self.tk_original_image = ImageTk.PhotoImage(my_pil_image)
        # Clear canvas 
        self.my_original_canvas.delete("all")
        self.original_image_on_canvas = self.my_original_canvas.create_image(
            canvas_width//2, canvas_height//2, 
            anchor=tk.CENTER, 
            image=self.tk_original_image
        )
        self.scale_factor = scale
    
    def start_image_croping(self, event):
        self.crop_start = (event.x, event.y)
        self.current_crop_rect = None
    
    def update_image_croping(self, event):
        if self.crop_start and self.my_original_image is not None:
            # clean last rectangle
            if self.current_crop_rect:
                self.my_original_canvas.delete(self.current_crop_rect)
            # mouse position
            x1, y1 = self.crop_start
            # store position of mouse
            x2, y2 = event.x, event.y
            
            # Green Rectange make
            self.current_crop_rect = self.my_original_canvas.create_rectangle(
                x1, y1, x2, y2, 
                outline='green', 
                width=3
                # 
            )
    
    def end_my_image_scrop(self, event):
        # get end point 
        x1, y1 = self.crop_start
        x2, y2 = event.x, event.y
    #    top-left and bottom-right 
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        canvas_width = self.my_original_canvas.winfo_width()
        canvas_height = self.my_original_canvas.winfo_height()
        
        #image position calculation on Canvas
        img_x = (canvas_width - self.tk_original_image.width()) // 2
        img_y = (canvas_height - self.tk_original_image.height()) // 2
        # Adjusting coordinates 
        x1 = max(x1 - img_x, 0)
        y1 = max(y1 - img_y, 0)
        x2 = min(x2 - img_x, self.tk_original_image.width())
        y2 = min(y2 - img_y, self.tk_original_image.height())
        # coordinates Scale
        x1 = int(x1 / self.scale_factor)
        y1 = int(y1 / self.scale_factor)
        x2 = int(x2 / self.scale_factor)
        y2 = int(y2 / self.scale_factor)
        
        # checking the area 
        if x2 > x1 and y2 > y1:
            # Croping
            self.my_cropped_image = self.my_original_image[y1:y2, x1:x2]
            # display my croped imagey
            self.show_cropped_image()
            # sider
            self.resize_slider.set(100)
            self.resize_value_label.config(text="100%")
    # display croped image
    def show_cropped_image(self):
        image_rgb = cv2.cvtColor(self.my_cropped_image, cv2.COLOR_BGR2RGB)
        my_pil_image = Image.fromarray(image_rgb)
        tk_image = ImageTk.PhotoImage(my_pil_image)
        self.cropped_label.config(image=tk_image)
        self.cropped_label.image = tk_image
    
    def resize_my_image(self, value):
        try:
            scale = float(value) / 100
            self.resize_value_label.config(text=f"{int(scale*100)}%")
            # check scale
            if scale > 0:
                # dimensions cal
                height, width = self.my_cropped_image.shape[:2]
                new_width = int(width * scale)
                new_height = int(height * scale)
                # img resize 
                resized = cv2.resize(self.my_cropped_image, (new_width, new_height), 
                                interpolation=cv2.INTER_AREA)
                # Convert BRG to RBB
                image_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                my_pil_image = Image.fromarray(image_rgb)
                tk_image = ImageTk.PhotoImage(my_pil_image)
                self.cropped_label.config(image=tk_image)
                self.cropped_label.image = tk_image
        except Exception as e:
            print(f"Error in resizing my image, please try it again: {e}")

    # save my image
    def save_my_image(self):
    
        my_file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if my_file_path:
            # scale 
            scale = float(self.resize_slider.get()) / 100
            if scale != 1.0:
                # Resize image to save it 
                height, width = self.my_cropped_image.shape[:2]
                my_resized_image = cv2.resize(self.my_cropped_image, 
                                    (int(width * scale), int(height * scale)), 
                                    interpolation=cv2.INTER_AREA)
                cv2.imwrite(my_file_path, my_resized_image)
            else:
                cv2.imwrite(my_file_path, self.my_cropped_image)

if __name__ == "__main__":
    root_of_app = tk.Tk()
    app = My_Image_App(root_of_app)
    root_of_app.mainloop()