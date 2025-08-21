"""
Input forms for the Pharmaceutical Quiz Module.
Handles user input collection and validation.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from config.settings import (
    PROJECT_TYPES, CLIENT_SCENARIOS, EXPERIENCE_LEVELS, 
    SUPPORTED_FILE_TYPES, ERROR_MESSAGES
)


class InputForm(ttk.Frame):
    """Main input form for collecting user and project information."""
    
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.selected_files = []
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all input widgets."""
        # Main container with scrollable frame
        self.create_scrollable_frame()
        
        # Title
        title_label = ttk.Label(self.scroll_frame, text="Pharmaceutical Therapy Area Knowledge Quiz", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky='w')
        
        # Subtitle
        subtitle_label = ttk.Label(self.scroll_frame, 
                                  text="Please provide project and client information to customize your quiz:",
                                  style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky='w')
        
        current_row = 2
        
        # Required fields section
        required_frame = ttk.LabelFrame(self.scroll_frame, text="Required Information", padding=15)
        required_frame.grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        required_frame.columnconfigure(1, weight=1)
        
        # Project Name
        ttk.Label(required_frame, text="Project Name *:").grid(row=0, column=0, sticky='w', pady=5)
        self.project_name = ttk.Entry(required_frame, width=40)
        self.project_name.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Client Name
        ttk.Label(required_frame, text="Client Name *:").grid(row=1, column=0, sticky='w', pady=5)
        self.client_name = ttk.Entry(required_frame, width=40)
        self.client_name.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Primary Therapy Area
        ttk.Label(required_frame, text="Primary Therapy Area *:").grid(row=2, column=0, sticky='w', pady=5)
        self.therapy_area = ttk.Entry(required_frame, width=40)
        self.therapy_area.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Indication
        ttk.Label(required_frame, text="Indication *:").grid(row=3, column=0, sticky='w', pady=5)
        self.indication = ttk.Entry(required_frame, width=40)
        self.indication.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Project Type
        ttk.Label(required_frame, text="Project Type *:").grid(row=4, column=0, sticky='w', pady=5)
        self.project_type = ttk.Combobox(required_frame, values=PROJECT_TYPES, state='readonly', width=37)
        self.project_type.grid(row=4, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Client Scenario
        ttk.Label(required_frame, text="Client Scenario *:").grid(row=5, column=0, sticky='w', pady=5)
        self.client_scenario = ttk.Combobox(required_frame, values=CLIENT_SCENARIOS, state='readonly', width=37)
        self.client_scenario.grid(row=5, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        current_row += 1
        
        # Experience Level Section
        exp_frame = ttk.LabelFrame(self.scroll_frame, text="Experience Level Assessment", padding=15)
        exp_frame.grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        exp_frame.columnconfigure(0, weight=1)
        
        # Experience level instructions
        exp_instruction = ttk.Label(exp_frame, 
                                   text="Please select your experience level with this therapy area and project type:",
                                   style='Info.TLabel')
        exp_instruction.grid(row=0, column=0, sticky='w', pady=(0, 10))
        
        # Experience level scale
        self.experience_level = tk.IntVar(value=1)
        scale_frame = ttk.Frame(exp_frame)
        scale_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        scale_frame.columnconfigure(1, weight=1)
        
        ttk.Label(scale_frame, text="Experience Level *:").grid(row=0, column=0, sticky='w')
        self.exp_scale = ttk.Scale(scale_frame, from_=1, to=7, orient='horizontal', 
                                  variable=self.experience_level, length=300)
        self.exp_scale.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        
        # Current level display
        self.exp_display = ttk.Label(scale_frame, text="Level 1")
        self.exp_display.grid(row=0, column=2, padx=(10, 0))
        
        # Bind scale change event
        self.exp_scale.configure(command=self.update_experience_display)
        
        # Experience level definitions
        self.create_experience_definitions(exp_frame)
        
        current_row += 1
        
        # Optional fields section
        optional_frame = ttk.LabelFrame(self.scroll_frame, text="Optional Information", padding=15)
        optional_frame.grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        optional_frame.columnconfigure(1, weight=1)
        
        # Additional Therapy Area
        ttk.Label(optional_frame, text="Additional Therapy Area:").grid(row=0, column=0, sticky='w', pady=5)
        self.additional_therapy = ttk.Entry(optional_frame, width=40)
        self.additional_therapy.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Brand Name
        ttk.Label(optional_frame, text="Client Brand Name(s):").grid(row=1, column=0, sticky='w', pady=5)
        self.brand_name = ttk.Entry(optional_frame, width=40)
        self.brand_name.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # Generic Name
        ttk.Label(optional_frame, text="Generic Name(s):").grid(row=2, column=0, sticky='w', pady=5)
        self.generic_name = ttk.Entry(optional_frame, width=40)
        self.generic_name.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        current_row += 1
        
        # Document upload section
        self.create_document_upload_section(current_row)
        
        current_row += 1
        
        # Action buttons
        button_frame = ttk.Frame(self.scroll_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Start Quiz", command=self.start_quiz,
                  style='Navigation.TButton').pack(side='right', padx=(10, 0))
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form,
                  style='Quiz.TButton').pack(side='right')
        
        # Configure grid weights
        self.scroll_frame.columnconfigure(1, weight=1)
    
    def create_scrollable_frame(self):
        """Create a scrollable frame for the form."""
        # Create canvas and scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_experience_definitions(self, parent):
        """Create the experience level definitions display."""
        def_frame = ttk.Frame(parent)
        def_frame.grid(row=2, column=0, sticky='ew', pady=(10, 0))
        def_frame.columnconfigure(0, weight=1)
        
        # Title for definitions
        ttk.Label(def_frame, text="Experience Level Definitions:", 
                 style='Info.TLabel', font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        # Create text widget for definitions
        self.def_text = tk.Text(def_frame, height=8, width=80, wrap='word', 
                               font=('Arial', 9), bg='#f8f9fa', relief='flat')
        self.def_text.grid(row=1, column=0, sticky='ew')
        
        # Add definitions
        for level, description in EXPERIENCE_LEVELS.items():
            self.def_text.insert('end', f"{level}: {description}\n")
        
        self.def_text.config(state='disabled')
        
        # Highlight current level
        self.update_experience_display(1)
    
    def update_experience_display(self, value):
        """Update the experience level display."""
        level = int(float(value))
        self.experience_level.set(level)
        self.exp_display.config(text=f"Level {level}")
        
        # Highlight current level in definitions
        if hasattr(self, 'def_text'):
            self.def_text.config(state='normal')
            self.def_text.tag_remove('highlight', '1.0', 'end')
            
            # Find and highlight current level
            start_pos = f"{level}.0"
            end_pos = f"{level}.end"
            self.def_text.tag_add('highlight', start_pos, end_pos)
            self.def_text.tag_config('highlight', background='#e3f2fd', font=('Arial', 9, 'bold'))
            
            self.def_text.config(state='disabled')
    
    def create_document_upload_section(self, row):
        """Create the document upload section."""
        doc_frame = ttk.LabelFrame(self.scroll_frame, text="Background Documents (Optional)", padding=15)
        doc_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        doc_frame.columnconfigure(1, weight=1)
        
        # Instructions
        instruction = ttk.Label(doc_frame, 
                               text="Upload relevant documents to enhance question context (PDF, Word, PowerPoint, Excel):",
                               style='Info.TLabel')
        instruction.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))
        
        # File selection
        ttk.Button(doc_frame, text="Select Files", command=self.select_files,
                  style='Quiz.TButton').grid(row=1, column=0, sticky='w')
        
        # Selected files display
        self.files_label = ttk.Label(doc_frame, text="No files selected", style='Info.TLabel')
        self.files_label.grid(row=1, column=1, sticky='w', padx=(10, 0))
        
        # Clear files button
        self.clear_files_btn = ttk.Button(doc_frame, text="Clear Files", 
                                         command=self.clear_files, style='Quiz.TButton')
        self.clear_files_btn.grid(row=1, column=2, padx=(10, 0))
        self.clear_files_btn.configure(state='disabled')
    
    def select_files(self):
        """Open file dialog to select documents."""
        files = filedialog.askopenfilenames(
            title="Select Background Documents",
            filetypes=SUPPORTED_FILE_TYPES
        )
        
        if files:
            self.selected_files = list(files)
            self.update_files_display()
    
    def clear_files(self):
        """Clear selected files."""
        self.selected_files = []
        self.update_files_display()
    
    def update_files_display(self):
        """Update the files display label."""
        if self.selected_files:
            file_names = [os.path.basename(f) for f in self.selected_files]
            if len(file_names) == 1:
                display_text = file_names[0]
            else:
                display_text = f"{len(file_names)} files selected"
            
            self.files_label.config(text=display_text)
            self.clear_files_btn.configure(state='normal')
        else:
            self.files_label.config(text="No files selected")
            self.clear_files_btn.configure(state='disabled')
    
    def validate_input(self):
        """Validate required input fields."""
        required_fields = {
            'Project Name': self.project_name.get().strip(),
            'Client Name': self.client_name.get().strip(),
            'Primary Therapy Area': self.therapy_area.get().strip(),
            'Indication': self.indication.get().strip(),
            'Project Type': self.project_type.get(),
            'Client Scenario': self.client_scenario.get()
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        
        if missing_fields:
            messagebox.showerror("Missing Information", 
                               f"Please fill in the following required fields:\n• " + 
                               "\n• ".join(missing_fields))
            return False
        
        return True
    
    def collect_data(self):
        """Collect all form data into a dictionary."""
        return {
            'project_name': self.project_name.get().strip(),
            'client_name': self.client_name.get().strip(),
            'therapy_area': self.therapy_area.get().strip(),
            'additional_therapy': self.additional_therapy.get().strip(),
            'indication': self.indication.get().strip(),
            'brand_name': self.brand_name.get().strip(),
            'generic_name': self.generic_name.get().strip(),
            'project_type': self.project_type.get(),
            'client_scenario': self.client_scenario.get(),
            'experience_level': self.experience_level.get(),
            'selected_files': self.selected_files.copy()
        }
    
    def start_quiz(self):
        """Validate input and start the quiz."""
        if self.validate_input():
            user_data = self.collect_data()
            self.callback(user_data)
    
    def clear_form(self):
        """Clear all form fields."""
        self.project_name.delete(0, 'end')
        self.client_name.delete(0, 'end')
        self.therapy_area.delete(0, 'end')
        self.additional_therapy.delete(0, 'end')
        self.indication.delete(0, 'end')
        self.brand_name.delete(0, 'end')
        self.generic_name.delete(0, 'end')
        self.project_type.set('')
        self.client_scenario.set('')
        self.experience_level.set(1)
        self.selected_files = []
        self.update_files_display()
        self.update_experience_display(1)
