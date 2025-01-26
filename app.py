import tkinter as tk
from tkinter import ttk, messagebox
import threading
from test import create_new_deck_on_Elsa_in_Noxplayer

class ElsaAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ELSA Automation Tool")
        self.root.geometry("400x500")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create title label
        title_label = ttk.Label(
            main_frame, 
            text="ELSA Automation Tool", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Study Set Name Entry
        name_label = ttk.Label(
            main_frame,
            text="Study Set Name:",
            font=('Helvetica', 10)
        )
        name_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.name_entry = ttk.Entry(
            main_frame,
            width=40
        )
        self.name_entry.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Create buttons
        self.create_deck_btn = ttk.Button(
            main_frame,
            text="Create New Deck",
            command=self.run_create_deck,
            width=30
        )
        self.create_deck_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready",
            font=('Helvetica', 10)
        )
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=7, column=0, columnspan=2, pady=10)
    
    def validate_inputs(self):
        if not self.name_entry.get().strip():
            messagebox.showerror("Error", "Please enter a Study Set name")
            return False
        return True
    
    def run_create_deck(self):
        if not self.validate_inputs():
            return
            
        # Disable button while running
        self.create_deck_btn.configure(state='disabled')
        self.status_label.configure(text="Creating new deck...")
        self.progress.start()
        
        # Run the automation in a separate thread
        thread = threading.Thread(target=self.create_deck_thread)
        thread.daemon = True
        thread.start()
    
    def create_deck_thread(self):
        try:
            study_set_name = self.name_entry.get().strip()
            
            self.status_label.configure(text=f"Creating deck '{study_set_name}'...")
            
            result = create_new_deck_on_Elsa_in_Noxplayer(study_set_name)
            
            self.root.after(0, self.complete_task, result)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
    
    def complete_task(self, success):
        self.progress.stop()
        self.create_deck_btn.configure(state='normal')
        
        if success:
            self.status_label.configure(text="Successfully created new deck!")
            messagebox.showinfo("Success", "New deck created successfully!")
            # Clear inputs after successful creation
            self.name_entry.delete(0, tk.END)
        else:
            self.status_label.configure(text="Failed to create deck")
            messagebox.showerror("Error", "Failed to create new deck. Check console for details.")
    
    def show_error(self, error_message):
        self.progress.stop()
        self.create_deck_btn.configure(state='normal')
        self.status_label.configure(text="Error occurred")
        messagebox.showerror("Error", f"An error occurred:\n{error_message}")

def main():
    root = tk.Tk()
    app = ElsaAutomationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 