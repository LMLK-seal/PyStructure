# LMLK-seal/PyStructure - Combined Image and Text Structure Generator

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
import sys
import pathlib
import threading

# --- Dependency Imports ---
# We try to import libraries but handle cases where they might be missing.
try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# --- Core Logic for Structure Generation ---

# --- Method 1: From Image (AI) ---
def get_structure_from_image(image_path: str, api_key: str) -> list[str]:
    """Uses the Gemini Vision model to extract a file structure from an image."""
    if not genai:
        raise ImportError("The 'google-generativeai' library is required for image mode. Please run: pip install google-generativeai")
    if not Image:
        raise ImportError("The 'Pillow' library is required for image mode. Please run: pip install Pillow")

    genai.configure(api_key=api_key)
    img = Image.open(image_path)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = """
    Analyze the provided image of a directory tree. Extract all folder and file paths.
    - List every folder and file on a new line, relative to the top-level folder in the image.
    - End folder paths with a forward slash (`/`).
    - Do not add a trailing slash to files.
    - Ignore all comments (starting with '#') and tree-drawing characters (`├──`, `└──`, `│`, `─`).
    - Output ONLY the list of paths.
    """
    
    response = model.generate_content([prompt, img])
    return response.text.strip().split('\n')

# --- Method 2: From Text (Parsing) ---
def parse_text_structure(raw_text: str) -> list[str]:
    """Parses tree-like text to build a list of file and folder paths."""
    lines = raw_text.strip().split('\n')
    paths = []
    level_parents = {}
    
    first_indented_line = next((line for line in lines if line and not line[0].isspace() and (line.lstrip() != line)), None)
    indent_size = len(first_indented_line) - len(first_indented_line.lstrip(' │├─└')) if first_indented_line else 4
    if indent_size == 0: indent_size = 4

    for line in lines:
        if not line.strip(): continue
        indentation = len(line) - len(line.lstrip(' │├─└'))
        level = indentation // indent_size
        clean_name = line.lstrip(' │├─└').split('#', 1)[0].strip()
        if not clean_name: continue

        parent_parts = [level_parents[i] for i in range(level) if i in level_parents]
        all_parts = parent_parts + [clean_name]
        full_path = os.path.join(*all_parts)
        paths.append(full_path.replace('\\', '/'))

        if clean_name.endswith('/'):
            level_parents[level] = clean_name.strip('/')
            deeper_levels_to_clear = [lvl for lvl in level_parents if lvl > level]
            for lvl in deeper_levels_to_clear:
                del level_parents[lvl]
    return paths

# --- Common Function: File Creation ---
def create_structure(base_dir: str, paths: list[str]):
    """Creates the folder/file structure from a list of relative paths."""
    if not paths:
        raise ValueError("The parser did not find any valid paths.")

    created_items = []
    for path_str in paths:
        if not path_str: continue
        full_path = pathlib.Path(base_dir) / path_str
        if path_str.endswith('/'):
            full_path.mkdir(parents=True, exist_ok=True)
            created_items.append(f"Created directory: {full_path}")
        else:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.touch()
            created_items.append(f"Created file     : {full_path}")
    return created_items

# --- GUI Application Class ---

class StructureGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyStructure - AI & Text Structure Generator")
        self.root.geometry("800x650")
        
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')

        # --- Main Tabbed Interface ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.image_tab = ttk.Frame(self.notebook, padding="10")
        self.text_tab = ttk.Frame(self.notebook, padding="10")
        
        self.notebook.add(self.image_tab, text='From Image (AI)')
        self.notebook.add(self.text_tab, text='From Text')

        # --- Build the UI ---
        self.setup_image_tab()
        self.setup_text_tab()
        self.setup_common_controls()
        
    def setup_image_tab(self):
        """Creates all widgets for the 'From Image' tab."""
        # ** THE FIX IS HERE **
        ttk.Label(self.image_tab, text="Generate structure from an image using the Gemini API.", font=("TkDefaultFont", 10, "italic")).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(self.image_tab, text="Gemini API Key:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.api_key_entry = ttk.Entry(self.image_tab, width=60, show="*")
        self.api_key_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=5)
        
        ttk.Label(self.image_tab, text="Source Image:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.image_path_label = ttk.Label(self.image_tab, text="No image selected", foreground="gray")
        self.image_path_label.grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Button(self.image_tab, text="Select Image...", command=self.select_image).grid(row=2, column=2, padx=5)
        self.image_tab.columnconfigure(1, weight=1)
        self.image_path = ""

    def setup_text_tab(self):
        """Creates all widgets for the 'From Text' tab."""
        # ** THE FIX IS HERE **
        ttk.Label(self.text_tab, text="Paste your folder structure text below.", font=("TkDefaultFont", 10, "italic")).pack(anchor=tk.W, pady=(0, 5))
        self.input_text = scrolledtext.ScrolledText(self.text_tab, wrap=tk.WORD, height=15, font=("Courier New", 10))
        self.input_text.pack(expand=True, fill=tk.BOTH)

    def setup_common_controls(self):
        """Creates shared controls and the log area below the tabs."""
        controls_frame = ttk.Frame(self.root, padding="10")
        controls_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        ttk.Label(controls_frame, text="Destination Folder:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.dest_folder_label = ttk.Label(controls_frame, text="No folder selected", foreground="gray")
        self.dest_folder_label.grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Button(controls_frame, text="Select Folder...", command=self.select_folder).grid(row=0, column=2, padx=5)
        
        self.generate_button = ttk.Button(controls_frame, text="Generate Structure", command=self.start_generation_thread)
        self.generate_button.grid(row=1, column=1, pady=10, sticky='w')
        controls_frame.columnconfigure(1, weight=1)
        
        log_frame = ttk.Frame(self.root, padding="10")
        log_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
        ttk.Label(log_frame, text="Log:").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10, state='disabled')
        self.log_text.pack(expand=True, fill=tk.BOTH)
        self.dest_folder = ""

    def log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp"), ("All files", "*.*")])
        if path:
            self.image_path = path
            self.image_path_label.config(text=os.path.basename(path), foreground="black")

    def select_folder(self):
        path = filedialog.askdirectory(title="Select destination folder")
        if path:
            self.dest_folder = path
            self.dest_folder_label.config(text=path, foreground="black")

    def start_generation_thread(self):
        """Validates inputs and starts the appropriate generation process in a thread."""
        selected_tab_index = self.notebook.index(self.notebook.select())
        
        if not self.dest_folder:
            self.log("ERROR: Please select a destination folder.")
            return

        self.generate_button.config(state='disabled', text="Generating...")
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        
        thread_args = {}
        # Image Mode
        if selected_tab_index == 0:
            api_key = self.api_key_entry.get()
            if not api_key: self.log("ERROR: Gemini API Key is required."); self.generation_finished(); return
            if not self.image_path: self.log("ERROR: Please select a source image."); self.generation_finished(); return
            thread_args = {"mode": "image", "api_key": api_key, "image_path": self.image_path, "dest_folder": self.dest_folder}
        
        # Text Mode
        elif selected_tab_index == 1:
            raw_text = self.input_text.get("1.0", tk.END).strip()
            if not raw_text: self.log("ERROR: The input text box is empty."); self.generation_finished(); return
            thread_args = {"mode": "text", "raw_text": raw_text, "dest_folder": self.dest_folder}
            
        thread = threading.Thread(target=self.run_generation, kwargs=thread_args)
        thread.daemon = True
        thread.start()

    def run_generation(self, **kwargs):
        """The actual workhorse function that runs in the background thread."""
        mode = kwargs.get("mode")
        dest_folder = kwargs.get("dest_folder")
        paths = []
        try:
            if mode == "image":
                self.log(">>> Starting generation process using Gemini 1.5 Flash...")
                self.log(f"1. Analyzing image: {os.path.basename(kwargs['image_path'])}")
                paths = get_structure_from_image(kwargs['image_path'], kwargs['api_key'])
                self.log("✔ Image analysis complete.")
            
            elif mode == "text":
                self.log(">>> Starting generation process from text...")
                self.log("1. Parsing input text to understand structure...")
                paths = parse_text_structure(kwargs['raw_text'])
                self.log("✔ Parsing complete.")

            self.log(f"\nFound {len(paths)} items to create.")
            self.log("\n2. Creating files and folders...")
            created_items = create_structure(dest_folder, paths)
            for item in created_items: self.log(item)
            self.log(f"\n✔ Success! Created {len(created_items)} files and folders.")

        except Exception as e:
            self.log(f"\n--- AN ERROR OCCURRED ---\nERROR: {e}")
        finally:
            self.root.after(0, self.generation_finished)

    def generation_finished(self):
        """Called when a thread is done to update the GUI."""
        self.generate_button.config(state='normal', text="Generate Structure")

def main():
    if genai is None or Image is None:
        print("INFO: Libraries for 'From Image' mode not found.")
        print("      You can still use the 'From Text' tab.")
        print("      To enable image processing, please run: pip install google-generativeai pillow")

    root = tk.Tk()
    app = StructureGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()