import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from create_deck import create_new_deck_on_Elsa_in_Noxplayer
import tkinter.font as tkfont
import threading
from test_LiteLLM import TextSplitter

class ElsaApp:
    def __init__(self, root):
        self.root = root
        self.text_splitter = TextSplitter()
        self.root.title("ELSA Deck Creator")
        self.root.geometry("800x800")
        self.root.minsize(600, 720)
        self.root.configure(bg='#ADD8E6')  # Light gray background
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#E6F3F7')
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
        
        # Main container frame
        main_container = ttk.Frame(root, style='Custom.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Create canvas and scrollbar inside main container
        self.canvas = tk.Canvas(main_container, bg='#E6F3F7', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        
        # Create the scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas, style='Custom.TFrame')
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window in canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind canvas resizing
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Add mousewheel binding
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Content Frame
        content_frame = ttk.Frame(self.scrollable_frame, style='Custom.TFrame', padding=10)
        content_frame.pack(fill=tk.X)
        
        # Title
        title_label = ttk.Label(content_frame, 
                              text="ELSA Deck Creator", 
                              style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create content frame
        content_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        content_frame.pack(fill=tk.X)
        
        # Study Set Name
        name_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        name_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(name_frame, 
                 text="Study Set Name", 
                 style='Custom.TLabel').pack(anchor=tk.W)
        
        self.study_set_name = ttk.Entry(name_frame, 
                                      font=('Helvetica', 11),
                                      width=40)
        self.study_set_name.pack(pady=(5, 0))
        
        # Paragraph
        para_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        para_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(para_frame, 
                 text="Paragraph", 
                 style='Custom.TLabel').pack(anchor=tk.W)
        
        # Custom font for text area
        text_font = tkfont.Font(family="Helvetica", size=11)
        
        self.paragraph = scrolledtext.ScrolledText(
            para_frame,
            font=text_font,
            width=40,
            height=12,
            wrap=tk.WORD,
            borderwidth=1,
            relief="solid"
        )
        self.paragraph.pack(pady=(5, 0))
        
        # Model selection frame
        self.preview_frame = ttk.LabelFrame(content_frame, text="AI Split Results - Select One", style='Custom.TFrame')
        self.preview_frame.pack(fill=tk.X, pady=(15, 5))
        self.preview_frame.pack_forget()  # Initially hidden
        
        # Create preview text areas for each model
        self.preview_texts = {}
        self.preview_vars = {}
        
        # Create a single StringVar for radio button selection
        self.selected_model = tk.StringVar(value="")
        
        for model in self.text_splitter.models:
            frame = ttk.Frame(self.preview_frame, style='Custom.TFrame')
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Model header with radio button
            header_frame = ttk.Frame(frame, style='Custom.TFrame')
            header_frame.pack(fill=tk.X)
            
            # Radio button for selection
            radio = ttk.Radiobutton(
                header_frame,
                text=f"{model}",
                variable=self.selected_model,
                value=model,
                style='Custom.TRadiobutton'
            )
            radio.pack(side=tk.LEFT, padx=5)
            
            # Preview text area
            preview = scrolledtext.ScrolledText(
                frame,
                font=('Helvetica', 10),
                width=40,
                height=6,
                wrap=tk.WORD
            )
            preview.pack(pady=(5, 10))
            self.preview_texts[model] = preview
        
        # Button Frame - moved after preview frame
        button_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        button_frame.pack(pady=(0, 15))
        
        # Single Create Deck button
        self.create_button = ttk.Button(
            button_frame,
            text="Create Deck",
            command=self.handle_create_button,
            style='Custom.TButton'
        )
        self.create_button.pack(pady=5)
        
        # Status Frame - moved after button
        status_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        status_frame.pack(pady=(0, 15))
        
        # Status Label
        self.status_label = ttk.Label(
            status_frame,
            text="",
            style='Custom.TLabel',
            wraplength=500,
            justify='center'
        )
        self.status_label.pack(pady=5)
        
        # Add progress details label
        self.progress_label = ttk.Label(
            status_frame,
            text="",
            style='Custom.TLabel',
            wraplength=500,
            justify='center'
        )
        self.progress_label.pack(pady=5)
        
        # Move progress bar below progress label
        self.progress = ttk.Progressbar(
            status_frame,
            length=300,
            mode='determinate',
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress.pack(pady=5)
        
        # Configure progress bar style
        self.style.configure('Custom.Horizontal.TProgressbar',
                           troughcolor='#f0f0f0',
                           background='#2ecc71',
                           thickness=10)
        
        # Add result text area after status frame
        ttk.Label(content_frame, 
                 text="Result", 
                 style='Custom.TLabel').pack(anchor=tk.W, pady=(15, 5))
        
        self.result_text = scrolledtext.ScrolledText(
            content_frame,
            font=text_font,
            width=40,
            height=8,
            wrap=tk.WORD,
            borderwidth=1,
            relief="solid"
        )
        self.result_text.pack(pady=(0, 20))
        # Initially hide the result text area
        self.result_text.pack_forget()

    def _on_canvas_configure(self, event):
        """Handle canvas resize"""
        # Update the width of the scrollable frame when canvas is resized
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=event.width)

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_progress(self, message, progress_value=None):
        """Update progress message and bar"""
        self.progress_label.config(
            text=message,
            foreground="#3498db"
        )
        if progress_value is not None:
            self.progress['value'] = progress_value
        self.root.update()
        
        # Ensure the canvas scrolls to show progress
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)  # Scroll to bottom to show progress

    def handle_create_button(self):
        """Handle the create deck button press based on current state"""
        if self.preview_frame.winfo_ismapped():
            # If previews are showing, create deck with selection
            self.create_deck()
        else:
            # If previews aren't showing, show them
            self.show_model_previews()

    def show_model_previews(self):
        """Show the preview results from all models"""
        para = self.paragraph.get("1.0", tk.END).strip()
        study_set = self.study_set_name.get()
        
        if not study_set or not para:
            messagebox.showwarning("Warning", "Please enter both study set name and text")
            return
            
        # Show the preview frame
        self.preview_frame.pack()
        
        # Update status
        self.status_label.config(
            text="🤔 Processing text with AI models...",
            foreground="#3498db"
        )
        
        # Get splits from all models
        results = self.text_splitter.split_text_all_models(para)
        
        # Update preview text areas
        for model, segments in results.items():
            preview = self.preview_texts[model]
            preview.delete("1.0", tk.END)
            if segments:
                preview.insert("1.0", "\n\n".join(segments))
            else:
                preview.insert("1.0", "Error processing text with this model")
        
        # Update status and button
        self.status_label.config(
            text="👆 Please select one of the split options above",
            foreground="#2ecc71"
        )
        self.create_button.config(text="Create Selected Deck")
        
        self.root.update_idletasks()

    def create_deck(self):
        """Create deck with selected split option"""
        selected_model = self.selected_model.get()
        
        if not selected_model:
            messagebox.showwarning("Warning", "Please select a split option")
            return
            
        # Get the segments from the selected preview
        preview = self.preview_texts[selected_model]
        segments = [s.strip() for s in preview.get("1.0", tk.END).split("\n\n") if s.strip()]
        
        study_set = self.study_set_name.get()
        
        # Reset progress
        self.progress['value'] = 0
        self.progress['maximum'] = 100
        
        # Disable button and show status
        self.create_button.config(state='disabled')
        self.status_label.config(
            text="🔄 Creating deck in ELSA...",
            foreground="#3498db"
        )
        
        def run_creation():
            try:
                result = create_new_deck_on_Elsa_in_Noxplayer(
                    study_set, 
                    segments,
                    progress_callback=self.update_progress
                )
                
                if result:
                    try:
                        clipboard_content = self.root.clipboard_get()
                        self.status_label.config(
                            text="✅ Deck created successfully! Link copied to clipboard:",
                            foreground="#2ecc71"
                        )
                        
                        # Show and update result text area with the link
                        self.result_text.delete("1.0", tk.END)
                        self.result_text.insert("1.0", clipboard_content)
                        self.result_text.pack()  # Make sure it's visible
                        
                        # Reset UI for next use while keeping the result visible
                        self.preview_frame.pack_forget()
                        self.create_button.config(text="Create Deck")
                        self.study_set_name.delete(0, tk.END)
                        self.paragraph.delete("1.0", tk.END)
                        self.selected_model.set("")  # Clear radio selection
                        
                    except Exception as e:
                        print(f"Error getting clipboard content: {str(e)}")
                        self.status_label.config(
                            text="✅ Deck created successfully! (Could not retrieve link)",
                            foreground="#2ecc71"
                        )
                else:
                    self.status_label.config(
                        text="❌ Failed to create deck. Please try again.",
                        foreground="#e74c3c"
                    )
                    self.result_text.pack_forget()
                    
            except Exception as e:
                self.status_label.config(
                    text=f"⚠️ Error: {str(e)}",
                    foreground="#e74c3c"
                )
                self.result_text.pack_forget()
                
            finally:
                self.create_button.config(state='normal')
                self.progress_label.config(text="")
                
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
