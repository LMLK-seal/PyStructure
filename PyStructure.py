"LMLK-seal/PyStructure"

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
import sys
import pathlib
import threading
from PIL import Image

# We will try to import the Gemini library, but won't fail if it's not present yet.
# The user will be prompted to install it if needed.
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# --- Core AI and File Logic (separated from GUI) ---

def get_structure_from_image(image_path: str, api_key: str) -> str:
    """Uses the Gemini Vision model to extract a file structure from an image."""
    if not genai:
        raise ImportError("The 'google-generativeai' library is not installed. Please run: pip install google-generativeai")

    genai.configure(api_key=api_key)
    img = Image.open(image_path)
    
    # --- THIS IS THE UPDATED LINE ---
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    # --------------------------------

    prompt = """
    Analyze the provided image which shows a directory tree structure.
    Your task is to extract all folder and file paths, starting from the root folder shown in the image.
    
    Instructions:
    1. List every folder and file on a new line. The paths should be relative to the top-level folder in the image.
    2. For folders, ensure the path ends with a forward slash (`/`).
    3. For files, do not add a trailing slash.
    4. Ignore all comments (lines or parts of lines starting with '#').
    5. Ignore the tree-drawing characters (like `├──`, `└──`, `│`, `─`).
    6. The output should ONLY be the list of paths, nothing else.
    """
    
    response = model.generate_content([prompt, img])
    return response.text

def create_structure(base_dir: str, raw_text: str):
    """Parses the text from the AI and creates the folder/file structure."""
    if not raw_text:
        raise ValueError("AI returned an empty response. Cannot create structure.")

    paths = raw_text.strip().split('\n')
    created_items = []
    
    for path_str in paths:
        path_str = path_str.strip()
        if not path_str:
            continue
        
        # Create the full path relative to the selected base directory
        full_path = pathlib.Path(base_dir) / path_str.replace('\\', '/')

        # Check if the path from the AI indicates a directory
        if path_str.endswith('/'):
            full_path.mkdir(parents=True, exist_ok=True)
            created_items.append(f"Created directory: {full_path}")
        # Otherwise, it's a file
        else:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.touch()
            created_items.append(f"Created file     : {full_path}")
            
    return created_items

# --- GUI Application Class ---

class StructureGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Structure from Image Generator (Gemini 1.5 Flash)")
        self.root.geometry("700x550")
        
        # Style
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam') # A clean, modern theme

        # Frame for inputs
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # --- API Key ---
        ttk.Label(input_frame, text="Gemini API Key:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.api_key_entry = ttk.Entry(input_frame, width=60, show="*")
        self.api_key_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # --- Image Selection ---
        ttk.Label(input_frame, text="Source Image:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.image_path_label = ttk.Label(input_frame, text="No image selected", foreground="gray")
        self.image_path_label.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Button(input_frame, text="Select Image...", command=self.select_image).grid(row=1, column=2, padx=5)
        
        # --- Destination Folder ---
        ttk.Label(input_frame, text="Destination Folder:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.dest_folder_label = ttk.Label(input_frame, text="No folder selected", foreground="gray")
        self.dest_folder_label.grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Button(input_frame, text="Select Folder...", command=self.select_folder).grid(row=2, column=2, padx=5)

        input_frame.columnconfigure(1, weight=1) # Make entry and labels expand

        # --- Generate Button ---
        self.generate_button = ttk.Button(self.root, text="Generate Structure", command=self.start_generation_thread)
        self.generate_button.pack(pady=10)

        # --- Log/Status Area ---
        log_frame = ttk.Frame(self.root, padding="10")
        log_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        ttk.Label(log_frame, text="Log:").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15, state='disabled')
        self.log_text.pack(expand=True, fill=tk.BOTH)
        
        self.image_path = ""
        self.dest_folder = ""

    def log(self, message):
        """Adds a message to the log text area in a thread-safe way."""
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END) # Auto-scroll

    def select_image(self):
        path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp"), ("All files", "*.*")]
        )
        if path:
            self.image_path = path
            self.image_path_label.config(text=os.path.basename(path), foreground="black")

    def select_folder(self):
        path = filedialog.askdirectory(title="Select destination folder")
        if path:
            self.dest_folder = path
            self.dest_folder_label.config(text=path, foreground="black")

    def start_generation_thread(self):
        """Starts the generation process in a new thread to keep the GUI responsive."""
        api_key = self.api_key_entry.get()
        if not api_key:
            self.log("ERROR: Gemini API Key is required.")
            return
        if not self.image_path:
            self.log("ERROR: Please select a source image.")
            return
        if not self.dest_folder:
            self.log("ERROR: Please select a destination folder.")
            return
            
        self.generate_button.config(state='disabled', text="Generating...")
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')

        thread = threading.Thread(target=self.run_generation, args=(api_key, self.image_path, self.dest_folder))
        thread.daemon = True
        thread.start()

    def run_generation(self, api_key, image_path, dest_folder):
        """The actual workhorse function that runs in the background thread."""
        try:
            self.log(">>> Starting generation process using Gemini 1.5 Flash...")
            self.log(f"1. Analyzing image: {os.path.basename(image_path)}")
            structure_text = get_structure_from_image(image_path, api_key)
            self.log("✔ Image analysis complete. AI returned structure.")
            
            self.log("\n2. Creating files and folders...")
            created_items = create_structure(dest_folder, structure_text)
            
            for item in created_items:
                self.log(item)
            
            self.log(f"\n✔ Success! Created {len(created_items)} files and folders in '{dest_folder}'.")

        except Exception as e:
            self.log(f"\n--- AN ERROR OCCURRED ---")
            self.log(f"ERROR: {e}")
            if "API_KEY_INVALID" in str(e):
                self.log("TIP: Please check if your API key is correct and valid.")
        finally:
            self.root.after(0, self.generation_finished)

    def generation_finished(self):
        """Called when the thread is done to update the GUI."""
        self.generate_button.config(state='normal', text="Generate Structure")

def main():
    if genai is None:
        print("Required library not found.")
        print("Please install it by running: pip install google-generativeai pillow")
        sys.exit(1)

    root = tk.Tk()
    app = StructureGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
