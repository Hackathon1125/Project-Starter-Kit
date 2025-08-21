#!/usr/bin/env python3
"""
Pharmaceutical Therapy Area Knowledge Quiz Module
Main entry point for the Tkinter-based quiz application.

This module provides a comprehensive quiz system for pharmaceutical consultants
to assess their knowledge before project onboarding.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.input_forms import InputForm
from ui.quiz_interface import QuizInterface
from ui.results_display import ResultsDisplay
from quiz_engine.quiz_logic import QuizLogic
from utils.data_handler import DataHandler


class PharmaceuticalQuizApp:
    """Main application class for the Pharmaceutical Quiz Module."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pharmaceutical Therapy Area Knowledge Quiz")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # Initialize data handler
        self.data_handler = DataHandler()
        
        # Initialize quiz logic
        self.quiz_logic = None
        
        # Current view
        self.current_frame = None
        
        # Start with input form
        self.show_input_form()
    
    def setup_styles(self):
        """Configure ttk styles for consistent appearance."""
        style = ttk.Style()
        
        # Configure button style
        style.configure('Quiz.TButton', padding=(10, 5))
        style.configure('Navigation.TButton', padding=(15, 8))
        
        # Configure label styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))
    
    def clear_frame(self):
        """Clear the current frame."""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_input_form(self):
        """Display the input form for quiz configuration."""
        self.clear_frame()
        self.current_frame = InputForm(self.root, self.start_quiz)
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    def start_quiz(self, user_data):
        """Start the quiz with the provided user data."""
        try:
            # Initialize quiz logic with user data
            self.quiz_logic = QuizLogic(user_data, self.data_handler)
            
            # Generate questions
            if not self.quiz_logic.generate_questions():
                messagebox.showerror("Error", "Failed to generate quiz questions. Please check your API configuration.")
                return
            
            # Show quiz interface
            self.show_quiz_interface()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start quiz: {str(e)}")
    
    def show_quiz_interface(self):
        """Display the quiz interface."""
        self.clear_frame()
        self.current_frame = QuizInterface(self.root, self.quiz_logic, self.show_results)
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    def show_results(self):
        """Display the quiz results."""
        self.clear_frame()
        self.current_frame = ResultsDisplay(self.root, self.quiz_logic, self.restart_quiz)
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    def restart_quiz(self):
        """Restart the quiz from the beginning."""
        self.show_input_form()
    
    def run(self):
        """Start the application main loop."""
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Start the main loop
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = PharmaceuticalQuizApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {str(e)}")
