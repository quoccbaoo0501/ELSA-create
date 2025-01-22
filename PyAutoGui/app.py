import tkinter as tk
from tkinter import ttk, messagebox
import threading
from test import create_new_deck_on_Elsa_in_Noxplayer
from move import select_category

class ElsaAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ELSA Automation Tool")
        self.root.geometry("400x500")  # Increased height for category
        
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
        
        # Category Selection
        category_label = ttk.Label(
            main_frame,
            text="Category:",
            font=('Helvetica', 10)
        )
        category_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.categories = [
            "TOEIC",
            "Work",
            "Culture",
            "Music and Movies",
            "IELTS",
            "Food",
            "Other",
            "Relationships",
            "Travel"
        ]
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            values=self.categories,
            width=37,
            state="readonly"
        )
        self.category_dropdown.grid(row=4, column=0, columnspan=2, pady=5)
        self.category_dropdown.set("Select Category")
        
        # Create buttons
        self.create_deck_btn = ttk.Button(
            main_frame,
            text="Create New Deck",
            command=self.run_create_deck,
            width=30
        )
        self.create_deck_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Thêm nút Test Category Selection
        self.test_category_btn = ttk.Button(
            main_frame,
            text="Test Category Selection",
            command=self.test_category_selection,
            width=30
        )
        self.test_category_btn.grid(row=8, column=0, columnspan=2, pady=10)
        
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
        if self.category_var.get() == "Select Category":
            messagebox.showerror("Error", "Please select a category")
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
            category = self.category_var.get()
            
            # Thêm thông báo chi tiết
            self.status_label.configure(text=f"Đang tạo deck '{study_set_name}' với category '{category}'...")
            
            result = create_new_deck_on_Elsa_in_Noxplayer(study_set_name, category)
            
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
            self.category_dropdown.set("Select Category")
        else:
            self.status_label.configure(text="Failed to create deck")
            messagebox.showerror("Error", "Failed to create new deck. Check console for details.")
    
    def show_error(self, error_message):
        self.progress.stop()
        self.create_deck_btn.configure(state='normal')
        self.status_label.configure(text="Error occurred")
        messagebox.showerror("Error", f"An error occurred:\n{error_message}")

    def test_category_selection(self):
        if self.category_var.get() == "Select Category":
            messagebox.showerror("Error", "Vui lòng chọn category trước")
            return
            
        self.test_category_btn.configure(state='disabled')
        self.status_label.configure(text="Đang test category selection...")
        self.progress.start()
        
        # Chạy test trong thread riêng
        thread = threading.Thread(target=self.run_category_test)
        thread.daemon = True
        thread.start()
    
    def run_category_test(self):
        try:
            category = self.category_var.get()
            result = select_category(category)
            
            # Cập nhật UI trong main thread
            self.root.after(0, self.complete_category_test, result)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
    
    def complete_category_test(self, success):
        self.progress.stop()
        self.test_category_btn.configure(state='normal')
        
        if success:
            self.status_label.configure(text="Category selection test thành công!")
            messagebox.showinfo("Success", "Test category selection thành công!")
        else:
            self.status_label.configure(text="Category selection test thất bại")
            messagebox.showerror("Error", "Không thể select category. Kiểm tra console để biết chi tiết.")

def main():
    root = tk.Tk()
    app = ElsaAutomationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 