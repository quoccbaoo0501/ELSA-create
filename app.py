import tkinter as tk
from tkinter import ttk, scrolledtext
from test import create_new_deck_on_Elsa_in_Noxplayer
import tkinter.font as tkfont
import threading
from llm_splitter import TextSplitter

class ElsaApp:
    def __init__(self, root):
        self.root = root
        self.text_splitter = TextSplitter()
        self.root.title("ELSA Deck Creator")
        self.root.geometry("1024x800")
        self.root.minsize(800, 720)
        self.root.configure(bg='#ADD8E6')  # Light gray background
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#E6F3F7')  # Light blue-gray
        self.style.configure('Custom.TLabel', 
                           background='#E6F3F7',
                           font=('Helvetica', 11))
        self.style.configure('Title.TLabel', 
                           background='#E6F3F7',
                           font=('Helvetica', 24, 'bold'),
                           foreground='#2C3E50')  # Dark blue-gray for text
        self.style.configure('Custom.TButton', 
                           font=('Helvetica', 12),
                           padding=10)
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, style='Custom.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, 
                              text="ELSA Deck Creator", 
                              style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create content frame
        content_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Study Set Name
        ttk.Label(content_frame, 
                 text="Study Set Name", 
                 style='Custom.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.study_set_name = ttk.Entry(content_frame, 
                                      font=('Helvetica', 11),
                                      width=50)
        self.study_set_name.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Paragraph
        ttk.Label(content_frame, 
                 text="Paragraph", 
                 style='Custom.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Custom font for text area
        text_font = tkfont.Font(family="Helvetica", size=11)
        
        self.paragraph = scrolledtext.ScrolledText(
            content_frame,
            font=text_font,
            width=45,
            height=12,
            wrap=tk.WORD,
            borderwidth=1,
            relief="solid"
        )
        self.paragraph.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Button Frame
        button_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        button_frame.grid(row=4, column=0, pady=(0, 15))
        
        # Create Button with custom style
        self.create_button = ttk.Button(
            button_frame,
            text="Create Deck",
            command=self.create_deck,
            style='Custom.TButton'
        )
        self.create_button.pack(pady=5)
        
        # Status Frame
        status_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        status_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Status Label
        self.status_label = ttk.Label(
            status_frame,
            text="",
            style='Custom.TLabel',
            wraplength=600,  # Allow text to wrap
            justify='center'
        )
        self.status_label.grid(row=0, column=0, pady=5)
        
        # Add progress details label
        self.progress_label = ttk.Label(
            status_frame,
            text="",
            style='Custom.TLabel',
            wraplength=600,
            justify='center'
        )
        self.progress_label.grid(row=1, column=0, pady=5)
        
        # Move progress bar below progress label
        self.progress = ttk.Progressbar(
            status_frame,
            length=400,
            mode='determinate',  # Changed to determinate mode
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress.grid(row=2, column=0, pady=5)
        
        # Configure progress bar style
        self.style.configure('Custom.Horizontal.TProgressbar',
                           troughcolor='#f0f0f0',
                           background='#2ecc71',
                           thickness=10)
        
        # Add result text area after status frame
        ttk.Label(content_frame, 
                 text="Result", 
                 style='Custom.TLabel').grid(row=6, column=0, sticky=tk.W, pady=(15, 5))
        
        self.result_text = scrolledtext.ScrolledText(
            content_frame,
            font=text_font,
            width=45,
            height=8,
            wrap=tk.WORD,
            borderwidth=1,
            relief="solid"
        )
        self.result_text.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        # Initially hide the result text area
        self.result_text.grid_remove()

    def update_progress(self, message, progress_value=None):
        """Update progress message and bar"""
        self.progress_label.config(
            text=message,
            foreground="#3498db"
        )
        if progress_value is not None:
            self.progress['value'] = progress_value
        self.root.update()

    def create_deck(self):
        # Clear previous result
        self.result_text.delete("1.0", tk.END)
        self.result_text.grid_remove()
        
        # Get values
        study_set = self.study_set_name.get()
        para = self.paragraph.get("1.0", tk.END).strip()
        
        # Validate inputs
        if not study_set or not para:
            self.status_label.config(
                text="⚠️ Please fill in all fields!",
                foreground="#e74c3c"
            )
            return
        
        # Reset progress
        self.progress['value'] = 0
        self.progress['maximum'] = 100
        
        # Disable button and show initial status
        self.create_button.config(state='disabled')
        self.status_label.config(
            text="🔄 Creating deck...",
            foreground="#3498db"
        )
        
        def run_creation():
            try:
                # Update progress for text processing
                self.update_progress("Processing text with AI...", 5)
                
                # Split text using LightLLM
                segments = self.text_splitter.split_text(para)
                
                # Update progress for ELSA processing
                self.update_progress("Opening ELSA app...", 10)
                
                # Start deck creation with processed segments
                result = create_new_deck_on_Elsa_in_Noxplayer(
                    study_set, 
                    segments,  # Pass segments instead of raw paragraph
                    progress_callback=self.update_progress
                )
                
                if result:
                    # Get clipboard content
                    clipboard_content = self.root.clipboard_get()
                    
                    self.status_label.config(
                        text="✅ Deck created successfully! Result shown below:",
                        foreground="#2ecc71"
                    )
                    # Show and update result text area
                    self.result_text.grid()
                    self.result_text.delete("1.0", tk.END)
                    self.result_text.insert("1.0", clipboard_content)
                    self.progress['value'] = 100
                else:
                    self.status_label.config(
                        text="❌ Failed to create deck. Please try again.",
                        foreground="#e74c3c"
                    )
                    self.result_text.grid_remove()
                    
            except Exception as e:
                self.status_label.config(
                    text=f"⚠️ Error: {str(e)}",
                    foreground="#e74c3c"
                )
                self.result_text.grid_remove()
                
            finally:
                # Clear progress message
                self.progress_label.config(text="")
                # Re-enable button
                self.create_button.config(state='normal')
                
        # Run creation in separate thread
        thread = threading.Thread(target=run_creation)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    # Set window icon (if you have one)
    # root.iconbitmap('path/to/icon.ico')
    app = ElsaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
