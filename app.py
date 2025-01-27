import tkinter as tk
from tkinter import ttk, messagebox
import test
import threading
import os

class ModernElsaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ELSA Study Set Creator")
        self.root.geometry("800x900")
        
        # Configure style with larger fonts
        self.style = ttk.Style()
        self.style.configure('Header.TLabel', font=('Helvetica', 20, 'bold'))
        self.style.configure('Status.TLabel', font=('Helvetica', 12))
        self.style.configure('Modern.TButton', font=('Helvetica', 12))
        
        # Create main container with more padding
        self.main_container = ttk.Frame(root, padding="35")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        self.create_header()
        self.create_input_section()
        self.create_status_section()
        self.create_button_section()
        
        # Initialize variables
        self.is_running = False
        
        # Set theme colors
        self.root.configure(bg='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')
        
    def create_header(self):
        # Header Section
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        header_label = ttk.Label(
            header_frame, 
            text="ELSA Study Set Creator", 
            style='Header.TLabel'
        )
        header_label.grid(row=0, column=0, sticky="w")
        
        # Subtitle
        subtitle = ttk.Label(
            header_frame,
            text="Automate your study set creation process",
            style='Status.TLabel'
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(5, 0))

    def create_input_section(self):
        # Input Section
        input_frame = ttk.LabelFrame(self.main_container, text="Study Set Details", padding="20")
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 30))
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Study Set Name
        ttk.Label(input_frame, text="Study Set Name:").grid(row=0, column=0, sticky="w", padx=(0, 15))
        self.study_set_name = tk.StringVar()
        self.name_entry = ttk.Entry(input_frame, textvariable=self.study_set_name)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=(0, 20))
        
        # Paragraph Input with increased height
        ttk.Label(input_frame, text="Paragraph:").grid(row=1, column=0, sticky="nw", padx=(0, 15))
        self.paragraph_text = tk.Text(input_frame, height=16, width=60, wrap=tk.WORD)
        self.paragraph_text.grid(row=1, column=1, sticky="ew", pady=(0, 20))

    def create_status_section(self):
        # Status Section with more height
        status_frame = ttk.LabelFrame(self.main_container, text="Status", padding="15")
        status_frame.grid(row=2, column=0, sticky="ew", pady=(0, 25))
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Status message
        self.status_var = tk.StringVar(value="Ready to start")
        self.status_label = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            style='Status.TLabel'
        )
        self.status_label.grid(row=0, column=0, sticky="w", pady=(0, 15))
        
        # Progress bar (removed height parameter)
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky="ew", padx=5, pady=5)  # Added padding

    def create_button_section(self):
        # Button Section with wider buttons
        button_frame = ttk.Frame(self.main_container)
        button_frame.grid(row=3, column=0, sticky="ew")
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Start Button
        self.start_button = ttk.Button(
            button_frame,
            text="Start Creation",
            command=self.start_automation,
            style='Modern.TButton',
            width=20
        )
        self.start_button.grid(row=0, column=0, padx=10)
        
        # Exit Button
        self.exit_button = ttk.Button(
            button_frame,
            text="Exit",
            command=self.confirm_exit,
            style='Modern.TButton',
            width=20
        )
        self.exit_button.grid(row=0, column=2, padx=10)

    def confirm_exit(self):
        if self.is_running:
            if messagebox.askyesno("Confirm Exit", "Automation is running. Are you sure you want to exit?"):
                self.root.quit()
        else:
            self.root.quit()

    def start_automation(self):
        study_set_name = self.study_set_name.get().strip()
        paragraph = self.paragraph_text.get("1.0", tk.END).strip()
        
        if not study_set_name:
            messagebox.showwarning(
                "Input Required", 
                "Please enter a name for your study set",
                parent=self.root
            )
            return
        
        if not paragraph:
            messagebox.showwarning(
                "Input Required", 
                "Please enter a paragraph to process",
                parent=self.root
            )
            return
        
        self.is_running = True
        self.disable_controls()
        self.progress.start(10)
        self.status_var.set("Creating study set...")
        
        # Run automation in separate thread
        thread = threading.Thread(target=self.run_automation, args=(study_set_name, paragraph))
        thread.daemon = True
        thread.start()

    def run_automation(self, study_set_name, paragraph):
        try:
            self.status_var.set("Creating study set...")
            result = test.create_new_deck_on_Elsa_in_Noxplayer(study_set_name, paragraph)
            self.root.after(0, self.automation_complete, result)
        except Exception as e:
            self.root.after(0, self.automation_error, str(e))

    def automation_complete(self, success):
        self.is_running = False
        self.progress.stop()
        self.enable_controls()
        
        if success:
            self.status_var.set("Study set created and ready for phrases!")
            messagebox.showinfo(
                "Success",
                "Study set has been created and prepared for adding phrases!",
                parent=self.root
            )
        else:
            self.status_var.set("Failed to complete all steps")
            messagebox.showerror(
                "Error",
                "Failed to complete the automation process. Please try again.",
                parent=self.root
            )

    def automation_error(self, error_message):
        self.is_running = False
        self.progress.stop()
        self.enable_controls()
        self.status_var.set("Error occurred")
        
        messagebox.showerror(
            "Error",
            f"An error occurred:\n{error_message}",
            parent=self.root
        )

    def disable_controls(self):
        self.start_button.state(['disabled'])
        self.name_entry.state(['disabled'])
        self.paragraph_text.configure(state='disabled')

    def enable_controls(self):
        self.start_button.state(['!disabled'])
        self.name_entry.state(['!disabled'])
        self.paragraph_text.configure(state='normal')

def main():
    root = tk.Tk()
    root.configure(bg='#f0f0f0')
    app = ModernElsaApp(root)
    
    # Set window icon if available
    icon_path = os.path.join('images', 'app_icon.ico')
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    
    root.mainloop()

if __name__ == "__main__":
    main() 