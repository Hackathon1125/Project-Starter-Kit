"""
Results display for the Pharmaceutical Quiz Module.
Shows comprehensive quiz results and performance analytics.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Callable
import math
from config.settings import COLORS, PASS_THRESHOLD


class ResultsDisplay(ttk.Frame):
    """Display comprehensive quiz results and analytics."""
    
    def __init__(self, parent, quiz_logic, restart_callback: Callable):
        super().__init__(parent)
        self.quiz_logic = quiz_logic
        self.restart_callback = restart_callback
        self.results = quiz_logic.get_results()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout all results display widgets."""
        # Main container with scrollable frame
        self.create_scrollable_frame()
        
        # Header section
        self.create_header_section()
        
        # Overall performance section
        self.create_performance_section()
        
        # Detailed breakdown section
        self.create_breakdown_section()
        
        # Recommendations section
        self.create_recommendations_section()
        
        # Action buttons
        self.create_action_buttons()
        
        # Configure grid weights
        self.scroll_frame.columnconfigure(0, weight=1)
    
    def create_scrollable_frame(self):
        """Create a scrollable frame for the results."""
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
    
    def create_header_section(self):
        """Create the header section with quiz information."""
        header_frame = ttk.Frame(self.scroll_frame)
        header_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=20)
        header_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="Quiz Results", style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky='w')
        
        # Quiz info
        user_data = self.results['user_data']
        info_text = f"Project: {user_data.get('project_name', 'N/A')} | " \
                   f"Client: {user_data.get('client_name', 'N/A')} | " \
                   f"Therapy Area: {user_data.get('therapy_area', 'N/A')}"
        
        info_label = ttk.Label(header_frame, text=info_text, style='Info.TLabel')
        info_label.grid(row=1, column=0, sticky='w', pady=(5, 0))
        
        # Completion time
        completion_time = self.results.get('completion_time', '')
        if completion_time:
            time_label = ttk.Label(header_frame, text=f"Completed: {completion_time[:19]}", 
                                  style='Info.TLabel')
            time_label.grid(row=2, column=0, sticky='w', pady=(2, 0))
    
    def create_performance_section(self):
        """Create the overall performance section."""
        perf_frame = ttk.LabelFrame(self.scroll_frame, text="Overall Performance", padding=20)
        perf_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=(0, 20))
        perf_frame.columnconfigure(1, weight=1)
        
        # Score display
        score_frame = ttk.Frame(perf_frame)
        score_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Large score display
        score_percentage = self.results['score_percentage']
        passed = self.results['passed']
        grade = self.results['grade']
        
        score_color = COLORS['success'] if passed else COLORS['error']
        
        score_label = tk.Label(score_frame, text=f"{score_percentage}%", 
                              font=('Arial', 36, 'bold'), fg=score_color)
        score_label.pack()
        
        grade_label = tk.Label(score_frame, text=f"Grade: {grade}", 
                              font=('Arial', 16, 'bold'), fg=score_color)
        grade_label.pack()
        
        status_text = "PASSED" if passed else "NEEDS IMPROVEMENT"
        status_label = tk.Label(score_frame, text=status_text, 
                               font=('Arial', 14, 'bold'), fg=score_color)
        status_label.pack()
        
        # Detailed statistics
        stats_frame = ttk.Frame(perf_frame)
        stats_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(3, weight=1)
        
        # Questions answered
        ttk.Label(stats_frame, text="Questions Answered:", style='Info.TLabel').grid(row=0, column=0, sticky='w', pady=2)
        ttk.Label(stats_frame, text=f"{self.results['answered_questions']}/{self.results['total_questions']}", 
                 style='Info.TLabel').grid(row=0, column=1, sticky='w', padx=(10, 20), pady=2)
        
        # Correct answers
        ttk.Label(stats_frame, text="Correct Answers:", style='Info.TLabel').grid(row=0, column=2, sticky='w', pady=2)
        ttk.Label(stats_frame, text=f"{self.results['correct_answers']}", 
                 style='Info.TLabel').grid(row=0, column=3, sticky='w', padx=(10, 0), pady=2)
        
        # Experience level
        ttk.Label(stats_frame, text="Experience Level:", style='Info.TLabel').grid(row=1, column=0, sticky='w', pady=2)
        ttk.Label(stats_frame, text=f"Level {self.results['user_data'].get('experience_level', 'N/A')}", 
                 style='Info.TLabel').grid(row=1, column=1, sticky='w', padx=(10, 20), pady=2)
        
        # Pass threshold
        ttk.Label(stats_frame, text="Pass Threshold:", style='Info.TLabel').grid(row=1, column=2, sticky='w', pady=2)
        ttk.Label(stats_frame, text=f"{int(PASS_THRESHOLD * 100)}%", 
                 style='Info.TLabel').grid(row=1, column=3, sticky='w', padx=(10, 0), pady=2)
    
    def create_breakdown_section(self):
        """Create the detailed breakdown section."""
        breakdown_frame = ttk.LabelFrame(self.scroll_frame, text="Performance Breakdown", padding=20)
        breakdown_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))
        breakdown_frame.columnconfigure(0, weight=1)
        breakdown_frame.columnconfigure(1, weight=1)
        
        # Category breakdown
        if self.results.get('category_breakdown'):
            cat_frame = ttk.LabelFrame(breakdown_frame, text="By Category", padding=15)
            cat_frame.grid(row=0, column=0, sticky='ew', padx=(0, 10))
            
            self.create_category_breakdown(cat_frame)
        
        # Difficulty breakdown
        if self.results.get('difficulty_breakdown'):
            diff_frame = ttk.LabelFrame(breakdown_frame, text="By Difficulty", padding=15)
            diff_frame.grid(row=0, column=1, sticky='ew', padx=(10, 0))
            
            self.create_difficulty_breakdown(diff_frame)
    
    def create_category_breakdown(self, parent):
        """Create category performance breakdown."""
        categories = self.results['category_breakdown']
        
        for i, (category, stats) in enumerate(categories.items()):
            # Category name
            cat_label = ttk.Label(parent, text=category, font=('Arial', 10, 'bold'))
            cat_label.grid(row=i*2, column=0, sticky='w', pady=(5, 2))
            
            # Performance bar and stats
            perf_frame = ttk.Frame(parent)
            perf_frame.grid(row=i*2+1, column=0, sticky='ew', pady=(0, 10))
            perf_frame.columnconfigure(0, weight=1)
            
            # Progress bar
            progress_var = tk.DoubleVar(value=stats['percentage'])
            progress_bar = ttk.Progressbar(perf_frame, variable=progress_var, maximum=100, length=200)
            progress_bar.grid(row=0, column=0, sticky='ew', padx=(0, 10))
            
            # Stats text
            stats_text = f"{stats['correct']}/{stats['total']} ({stats['percentage']:.1f}%)"
            stats_label = ttk.Label(perf_frame, text=stats_text, style='Info.TLabel')
            stats_label.grid(row=0, column=1)
    
    def create_difficulty_breakdown(self, parent):
        """Create difficulty performance breakdown."""
        difficulties = self.results['difficulty_breakdown']
        difficulty_order = ['fundamental', 'intermediate', 'advanced']
        
        row = 0
        for difficulty in difficulty_order:
            if difficulty in difficulties:
                stats = difficulties[difficulty]
                
                # Difficulty name
                diff_label = ttk.Label(parent, text=difficulty.capitalize(), font=('Arial', 10, 'bold'))
                diff_label.grid(row=row*2, column=0, sticky='w', pady=(5, 2))
                
                # Performance bar and stats
                perf_frame = ttk.Frame(parent)
                perf_frame.grid(row=row*2+1, column=0, sticky='ew', pady=(0, 10))
                perf_frame.columnconfigure(0, weight=1)
                
                # Progress bar
                progress_var = tk.DoubleVar(value=stats['percentage'])
                progress_bar = ttk.Progressbar(perf_frame, variable=progress_var, maximum=100, length=200)
                progress_bar.grid(row=0, column=0, sticky='ew', padx=(0, 10))
                
                # Stats text
                stats_text = f"{stats['correct']}/{stats['total']} ({stats['percentage']:.1f}%)"
                stats_label = ttk.Label(perf_frame, text=stats_text, style='Info.TLabel')
                stats_label.grid(row=0, column=1)
                
                row += 1
    
    def create_recommendations_section(self):
        """Create the recommendations section."""
        if not self.results.get('recommendations'):
            return
        
        rec_frame = ttk.LabelFrame(self.scroll_frame, text="Recommendations", padding=20)
        rec_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=(0, 20))
        rec_frame.columnconfigure(0, weight=1)
        
        # Recommendations text
        rec_text = tk.Text(rec_frame, height=6, wrap='word', font=('Arial', 10), 
                          bg='#f8f9fa', relief='flat')
        rec_text.grid(row=0, column=0, sticky='ew')
        
        for i, recommendation in enumerate(self.results['recommendations'], 1):
            rec_text.insert('end', f"{i}. {recommendation}\n")
        
        rec_text.config(state='disabled')
    
    def create_action_buttons(self):
        """Create action buttons."""
        button_frame = ttk.Frame(self.scroll_frame)
        button_frame.grid(row=4, column=0, pady=20)
        
        # Retake quiz button
        retake_button = ttk.Button(button_frame, text="Retake Quiz", 
                                  command=self.retake_quiz, style='Navigation.TButton')
        retake_button.pack(side='left', padx=(0, 10))
        
        # View detailed results button
        details_button = ttk.Button(button_frame, text="View Question Details", 
                                   command=self.show_question_details, style='Quiz.TButton')
        details_button.pack(side='left', padx=(0, 10))
        
        # Save results button
        save_button = ttk.Button(button_frame, text="Save Results", 
                                command=self.save_results, style='Quiz.TButton')
        save_button.pack(side='left')
    
    def retake_quiz(self):
        """Restart the quiz."""
        response = messagebox.askyesno("Retake Quiz", 
                                     "Are you sure you want to retake the quiz? " +
                                     "This will clear your current results.")
        if response:
            self.restart_callback()
    
    def show_question_details(self):
        """Show detailed question-by-question results."""
        details_window = tk.Toplevel(self)
        details_window.title("Question Details")
        details_window.geometry("800x600")
        details_window.resizable(True, True)
        
        # Create scrollable text widget
        text_frame = ttk.Frame(details_window)
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(text_frame, wrap='word', font=('Arial', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add question details
        for i, result in enumerate(self.results['question_results'], 1):
            if result is None:
                text_widget.insert('end', f"Question {i}: Not answered\n\n")
                continue
            
            question = result['question']
            is_correct = result['is_correct']
            user_answer = result['user_answer']
            correct_answer = result['correct_answer']
            
            # Question header
            status = "✓ CORRECT" if is_correct else "✗ INCORRECT"
            text_widget.insert('end', f"Question {i}: {status}\n")
            text_widget.insert('end', f"Category: {question.get('category', 'N/A')} | ")
            text_widget.insert('end', f"Difficulty: {question.get('difficulty', 'N/A')}\n\n")
            
            # Question text
            text_widget.insert('end', f"Q: {question['question']}\n\n")
            
            # Answer details
            text_widget.insert('end', f"Your answer: {user_answer}\n")
            text_widget.insert('end', f"Correct answer: {correct_answer}\n\n")
            
            # Explanation
            if question.get('explanation'):
                text_widget.insert('end', f"Explanation: {question['explanation']}\n")
            
            text_widget.insert('end', "-" * 80 + "\n\n")
        
        text_widget.config(state='disabled')
    
    def save_results(self):
        """Save quiz results to file."""
        try:
            data_handler = self.quiz_logic.data_handler
            filepath = data_handler.save_quiz_results(self.results)
            
            if filepath:
                messagebox.showinfo("Results Saved", 
                                  f"Quiz results have been saved to:\n{filepath}")
            else:
                messagebox.showerror("Save Failed", 
                                   "Failed to save quiz results. Please try again.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving results: {str(e)}")
    
    def get_performance_summary(self) -> str:
        """Get a brief performance summary."""
        score = self.results['score_percentage']
        grade = self.results['grade']
        passed = self.results['passed']
        
        summary = f"Score: {score}% (Grade: {grade})\n"
        summary += f"Status: {'PASSED' if passed else 'NEEDS IMPROVEMENT'}\n"
        summary += f"Questions: {self.results['correct_answers']}/{self.results['total_questions']} correct"
        
        return summary
