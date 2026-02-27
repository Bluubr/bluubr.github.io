from PIL import Image, ImageChops, ImageDraw, ImageFont
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk
import os

class PezutifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🅿️Ⓜ️ Pezutifier - Image Editor")
        self.root.geometry("600x800")
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Variables
        self.selected_color = (217, 217, 217)
        self.hex_color = "#d9d9d9"
        self.base_image = None
        self.base_image_path = None
        self.left_image_path = None
        self.right_image_path = None
        self.use_images = tk.BooleanVar()
        self.left_letter = tk.StringVar(value="A")
        self.right_letter = tk.StringVar(value="B")
        
        # Try to load default base image
        try:
            loaded_base = Image.open('Images/Base.png').convert("RGBA")
            self.base_image = self.crop_to_square(loaded_base)
            self.base_image_path = 'Images/Base.png'
        except Exception as e:
            # Base image will be selected by user
            print(e)
            pass

            
        self.setup_gui()
    
    def crop_to_square(self, image):
        """Crop image to 1:1 aspect ratio (square) from center"""
        width, height = image.size
        
        # Find the smaller dimension to make it square
        min_dimension = min(width, height)
        
        # Calculate crop box to center the crop
        left = (width - min_dimension) // 2
        top = (height - min_dimension) // 2
        right = left + min_dimension
        bottom = top + min_dimension
        
        # Crop to square
        return image.crop((left, top, right, bottom))
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="🎨 Pezutifier", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Base image selection
        base_frame = ttk.LabelFrame(main_frame, text="Base Image", padding="10")
        base_frame.pack(fill=tk.X, pady=5)
        
        base_button_frame = ttk.Frame(base_frame)
        base_button_frame.pack(fill=tk.X)
        
        ttk.Button(base_button_frame, text="Select Base Image", command=self.select_base_image).pack(side=tk.LEFT, padx=5)
        self.base_image_label = ttk.Label(base_button_frame, text="Base.png (Do not mess with unless you know what you are doing)" if self.base_image else "No base image selected")
        self.base_image_label.pack(side=tk.LEFT, padx=10)
        
        # Color selection
        color_frame = ttk.LabelFrame(main_frame, text="Color Selection", padding="10")
        color_frame.pack(fill=tk.X, pady=5)
        
        self.color_button = tk.Button(color_frame, text="Pick Color", command=self.pick_color,
                                     bg=self.hex_color, width=15, height=2)
        self.color_button.pack(side=tk.LEFT, padx=5)
        
        self.color_label = ttk.Label(color_frame, text=f"RGB: {self.selected_color}\nHex: {self.hex_color}")
        self.color_label.pack(side=tk.LEFT, padx=10)
        
        # Content type selection
        content_frame = ttk.LabelFrame(main_frame, text="Content Type", padding="10")
        content_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(content_frame, text="Letters", variable=self.use_images, 
                       value=False, command=self.toggle_content_type).pack(anchor=tk.W)
        ttk.Radiobutton(content_frame, text="Custom Images", variable=self.use_images, 
                       value=True, command=self.toggle_content_type).pack(anchor=tk.W)
        
        # Letter selection frame
        self.letter_frame = ttk.LabelFrame(main_frame, text="Letter Selection", padding="10")
        self.letter_frame.pack(fill=tk.X, pady=5)
        
        letter_input_frame = ttk.Frame(self.letter_frame)
        letter_input_frame.pack(fill=tk.X)
        
        ttk.Label(letter_input_frame, text="Left Letter:").pack(side=tk.LEFT, padx=(0,5))
        ttk.Entry(letter_input_frame, textvariable=self.left_letter, width=5).pack(side=tk.LEFT, padx=(0,20))
        
        ttk.Label(letter_input_frame, text="Right Letter:").pack(side=tk.LEFT, padx=(0,5))
        ttk.Entry(letter_input_frame, textvariable=self.right_letter, width=5).pack(side=tk.LEFT)
        
        # Image selection frame
        self.image_frame = ttk.LabelFrame(main_frame, text="Image Selection", padding="10")
        
        button_frame = ttk.Frame(self.image_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Select Left Image", command=self.select_left_image).pack(side=tk.LEFT, padx=5)
        self.left_image_label = ttk.Label(button_frame, text="No image selected")
        self.left_image_label.pack(side=tk.LEFT, padx=10)
        
        button_frame2 = ttk.Frame(self.image_frame)
        button_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame2, text="Select Right Image", command=self.select_right_image).pack(side=tk.LEFT, padx=5)
        self.right_image_label = ttk.Label(button_frame2, text="No image selected")
        self.right_image_label.pack(side=tk.LEFT, padx=10)
        
        # Process button
        ttk.Button(main_frame, text="🚀 Process Image", command=self.process_image).pack(pady=20)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready to process...")
        self.status_label.pack(pady=5)
        
    def pick_color(self):
        color = colorchooser.askcolor(title="Pick a color")
        if color[0]:
            (r, g, b), hex_value = color
            self.selected_color = (int(r), int(g), int(b))
            self.hex_color = hex_value
            self.color_button.configure(bg=hex_value)
            self.color_label.configure(text=f"RGB: {self.selected_color}\nHex: {hex_value}")
            
    def toggle_content_type(self):
        if self.use_images.get():
            self.letter_frame.pack_forget()
            self.image_frame.pack(fill=tk.X, pady=5)
        else:
            self.image_frame.pack_forget()
            self.letter_frame.pack(fill=tk.X, pady=5)
            
    def select_left_image(self):
        filename = filedialog.askopenfilename(
            title="Select Left Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if filename:
            self.left_image_path = filename
            self.left_image_label.configure(text=os.path.basename(filename))

    def select_right_image(self):
        filename = filedialog.askopenfilename(
            title="Select Right Image", 
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if filename:
            self.right_image_path = filename
            self.right_image_label.configure(text=os.path.basename(filename))
            
    def select_base_image(self):
        filename = filedialog.askopenfilename(
            title="Select Base Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if filename:
            try:
                loaded_image = Image.open(filename).convert("RGBA")
                self.base_image = self.crop_to_square(loaded_image)
                self.base_image_path = filename
                self.base_image_label.configure(text=f"{os.path.basename(filename)} (cropped to square)")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load base image: {e}")

    def process_image(self):
        try:
            # Check if base image is loaded
            if not self.base_image:
                messagebox.showwarning("Warning", "Please select a base image first!")
                return
                
            self.status_label.configure(text="Processing...")
            self.root.update()
            
            result_img = self.colorZut(self.base_image, (*self.selected_color, 150))
            
            if self.use_images.get():
                if not self.left_image_path or not self.right_image_path:
                    messagebox.showwarning("Warning", "Please select both left and right images!")
                    self.status_label.configure(text="Ready to process...")
                    return
                    
                final_img = self.add_content_to_image('', '', result_img, use_images=True,
                                                    img1_path=self.left_image_path,
                                                    img2_path=self.right_image_path)
                output_path = self.get_file_path('Images/outputs/output_with_actual_images.png')
            else:
                l1 = self.left_letter.get().strip() or 'A'
                l2 = self.right_letter.get().strip() or 'B'
                final_img = self.letterZut(l1, l2, result_img)
                output_path = self.get_file_path('Images/outputs/output_with_letters.png')
            
            final_img.save(output_path)
            self.status_label.configure(text=f"✅ Complete! Saved: {output_path}")
            messagebox.showinfo("Success", f"Image processed successfully!\nSaved to: {output_path}")
            
        except Exception as e:
            self.status_label.configure(text="❌ Error occurred")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def colorZut(self, image, color):
        zut_overlay = Image.new("RGBA", image.size, color)
        blended = Image.alpha_composite(image, zut_overlay)
        blek_loaded = Image.open(self.get_file_path('Images/Blek.png')).convert("RGBA")
        blek_square = self.crop_to_square(blek_loaded)
        blek = blek_square.resize(image.size)
        result = ImageChops.subtract(blended, blek)
        result.save(self.get_file_path('Images/outputs/output.png'))
        return result

    def tilt_image(self, img_path, side, target_size):
        try:
            loaded_img = Image.open(img_path).convert("RGBA")
            target_wh = (244, 244)
            loaded_img = loaded_img.resize(target_wh, Image.Resampling.LANCZOS)
            # Crop to square first, then resize
            square_img = self.crop_to_square(loaded_img)
            actual_img = square_img.copy()
            actual_img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
            
            temp_size = int(target_size * 2)
            temp_img = Image.new("RGBA", (temp_size, temp_size), (0,0,0,0))
            
            paste_x = (temp_size - actual_img.size[0]) // 2 - 1

            
            if side == "left":
                paste_y = (temp_size - actual_img.size[1]) // 2 - 17
                temp_img.paste(actual_img, (paste_x, paste_y), actual_img)
                transformed = temp_img.transform(
                    (int(temp_size * 0.8), int(temp_size * 1.2)),
                    Image.Transform.AFFINE,
                    (1.0, 0.0, 85, -0.415, 0.825, 227 + 43.5),
                    resample=Image.Resampling.BICUBIC
                )

            elif side == "right":
                paste_y = (temp_size - actual_img.size[1]) // 2 + 100
                temp_img.paste(actual_img, (paste_x, paste_y), actual_img)
                transformed = temp_img.transform(
                    (int(temp_size * 0.8), int(temp_size * 1.2)),
                    Image.Transform.AFFINE,
                    (0.99, 0, 212, 0.41, 0.82, 215),
                    resample=Image.Resampling.BICUBIC
                )
            return transformed
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            return None

    def tilt_letter(self, l1, side, font_size, font):
        temp_size = int(font_size * 2)
        temp_img = Image.new("RGBA", (temp_size, temp_size), (0,0,0,0))
        temp_draw = ImageDraw.Draw(temp_img)
        text_box = temp_draw.textbbox((0,0), l1, font)
        capture_text_width = text_box[2] - text_box[0]
        capture_text_height = text_box[3] - text_box[1]
        capture_text_x = (temp_size - capture_text_width) // 2
        capture_text_y = (temp_size - capture_text_height) // 2
        
        temp_draw.text((capture_text_x, capture_text_y), l1, font=font, fill=(255,255,255,255))

        if side == "left":
            transformed = temp_img.transform(
                (int(temp_size * 0.8), int(temp_size * 1.2)),
                Image.Transform.AFFINE,
                (1.0, 0.0, 90, -0.5, 1.0, 230),
                resample=Image.Resampling.BICUBIC
            )
        elif side == "right":
            transformed = temp_img.transform(
                (int(temp_size * 0.8), int(temp_size * 1.2)),
                Image.Transform.AFFINE,
                (1.0, 0, 200, 0.5, 1.0, 90),
                resample=Image.Resampling.BICUBIC
            )
        return transformed

    def letterZut(self, l1, l2, img):
        if img.mode == 'RGBA':
            img = img.convert('RGBA')
        w, h = img.size
        img_final = img.copy()
        font_size = int(w * 0.4)
        font = ImageFont.truetype("arial.ttf", font_size)
        # left side
        transformed_left_letter = self.tilt_letter(l1, 'left', font_size, font=font)
        capture_left_x = int(w * 0.05)
        capture_left_y = int(h * 0.35 - 35)
        img_final.paste(transformed_left_letter, (capture_left_x, capture_left_y), transformed_left_letter)

        # right side
        transformed_right_letter = self.tilt_letter(l2, 'right', font_size, font=font)
        capture_right_x = int(w * 0.55)
        capture_right_y = int(h * 0.35 - 35)
        img_final.paste(transformed_right_letter, (capture_right_x, capture_right_y), transformed_right_letter)
        return img_final

    def add_content_to_image(self, l1, l2, img, use_images=False, img1_path=None, img2_path=None):
        if img.mode == 'RGBA':
            img = img.convert('RGBA')
        w, h = img.size
        img_final = img.copy()
        target_size = int(w * 0.5)
        
        if use_images and img1_path and img2_path:
            transformed_left = self.tilt_image(img1_path, 'left', target_size)
            if transformed_left:
                capture_left_x = int(w * -0.05)
                capture_left_y = int(h * 0.25)
                img_final.paste(transformed_left, (capture_left_x, capture_left_y), transformed_left)
            
            transformed_right = self.tilt_image(img2_path, 'right', target_size)
            if transformed_right:
                capture_right_x = int(w * 0.45)
                capture_right_y = int(h * 0.27)
                img_final.paste(transformed_right, (capture_right_x, capture_right_y), transformed_right)
        else:
            font_size = target_size
            try:
                # Prefer a TrueType font for better quality if available
                font = ImageFont.truetype("arial.ttf", font_size)
            except OSError:
                try:
                    # Common fallback font on many systems
                    font = ImageFont.truetype("DejaVuSans.ttf", font_size)
                except OSError:
                    # Final fallback to basic default font
                    font = ImageFont.load_default()
            
            transformed_left_letter = self.tilt_letter(l1, 'left', font_size, font=font)
            capture_left_x = int(w * -0.05)
            capture_left_y = int(h * 0.20)
            img_final.paste(transformed_left_letter, (capture_left_x, capture_left_y), transformed_left_letter)

            transformed_right_letter = self.tilt_letter(l2, 'right', font_size, font=font)
            capture_right_x = int(w * 0.45)
            capture_right_y = int(h * 0.30)
            img_final.paste(transformed_right_letter, (capture_right_x, capture_right_y), transformed_right_letter)
        
        return img_final

    def get_file_path(self, file_path):
        # Example:
        # base_dir is 'User/Bluubr/Pycharm/Projects/Pezutifier/src'
        # file_path is 'Images/Bleck.png'
        # returned is 'User/Bluubr/Pycharm/Projects/Pezutifier/src/Images/Bleck.png'

        path = os.path.normpath(os.path.join(self.base_dir, file_path))
        os.makedirs(os.path.dirname(path), exist_ok=True)  # makedirs ensures your folder exists when you're saving an image
        return path

if __name__ == "__main__":
    root = tk.Tk()
    app = PezutifierGUI(root)
    root.mainloop()
