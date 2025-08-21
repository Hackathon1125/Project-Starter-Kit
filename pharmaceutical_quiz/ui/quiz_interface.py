"""
Quiz interface for the Pharmaceutical Quiz Module.
Handles question display, answer collection, and navigation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Callable
from config.settings import COLORS


class QuizInterface(ttk.Frame):
    """Main quiz interface for displaying questions and collecting answers."""
    
    def __init__(self, parent, quiz_logic, completion_callback: Callable):
        super().__init__(parent)
        self.quiz_logic = quiz_logic
        self.completion_callback = completion_callback
        
        # Current question state
        self.current_answer = None
        self.answer_widgets = []
        
        # Start the quiz
        self.quiz_logic.start_quiz()
        
        self.create_widgets()
        self.load_current_question()
    
    def create_widgets(self):
        """Create and layout all quiz interface widgets."""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Quiz title
        title_label = ttk.Label(header_frame, text="Pharmaceutical Therapy Area Knowledge Quiz", 
                               style='Title.TLabel')
        title_label.pack(anchor='w')
        
        # Progress section
        progress_frame = ttk.Frame(header_frame)
        progress_frame.pack(fill='x', pady=(10, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack(side='left')
        
        # Progress text
        self.progress_label = ttk.Label(progress_frame, text="Question 1 of 15", 
                                       style='Info.TLabel')
        self.progress_label.pack(side='left', padx=(10, 0))
        
        # Question section
        question_frame = ttk.LabelFrame(main_frame, text="Question", padding=20)
        question_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Question text
        self.question_text = tk.Text(question_frame, height=4, wrap='word', 
                                    font=('Arial', 12), bg='white', relief='flat',
                                    state='disabled')
        self.question_text.pack(fill='x', pady=(0, 15))
        
        # Answer section
        self.answer_frame = ttk.LabelFrame(main_frame, text="Select Your Answer", padding=15)
        self.answer_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Navigation section
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill='x')
        
        # Navigation buttons
        self.back_button = ttk.Button(nav_frame, text="← Previous", 
                                     command=self.go_back, style='Navigation.TButton')
        self.back_button.pack(side='left')
        
        self.next_button = ttk.Button(nav_frame, text="Next →", 
                                     command=self.go_next, style='Navigation.TButton')
        self.next_button.pack(side='right')
        
        # Submit answer button (center)
        self.submit_button = ttk.Button(nav_frame, text="Submit Answer", 
                                       command=self.submit_answer, style='Quiz.TButton')
        self.submit_button.pack()
        
        # Feedback section (initially hidden)
        self.feedback_frame = ttk.LabelFrame(main_frame, text="Feedback", padding=15)
        self.feedback_text = tk.Text(self.feedback_frame, height=6, wrap='word',
                                    font=('Arial', 10), state='disabled')
        self.feedback_text.pack(fill='both', expand=True)
    
    def load_current_question(self):
        """Load and display the current question."""
        question = self.quiz_logic.get_current_question()
        if not question:
            self.completion_callback()
            return
        
        # Update progress
        progress = self.quiz_logic.get_question_progress()
        self.progress_var.set(progress['percentage'])
        self.progress_label.config(text=f"Question {progress['current']} of {progress['total']}")
        
        # Display question
        self.question_text.config(state='normal')
        self.question_text.delete('1.0', 'end')
        self.question_text.insert('1.0', question['question'])
        self.question_text.config(state='disabled')
        
        # Clear previous answer widgets
        self.clear_answer_widgets()
        
        # Create answer widgets based on question type
        self.create_answer_widgets(question)
        
        # Update navigation buttons
        self.update_navigation_buttons()
        
        # Hide feedback
        self.hide_feedback()
        
        # Load previous answer if exists
        self.load_previous_answer()
    
    def clear_answer_widgets(self):
        """Clear all answer widgets."""
        for widget in self.answer_widgets:
            widget.destroy()
        self.answer_widgets.clear()
        self.current_answer = None
    
    def create_answer_widgets(self, question: Dict):
        """Create answer widgets based on question type."""
        question_type = question['type']
        options = question['options']
        
        if question_type == 'multiple_choice':
            self.create_multiple_choice_widgets(options)
        elif question_type == 'multiple_select':
            self.create_multiple_select_widgets(options)
        elif question_type == 'true_false':
            self.create_true_false_widgets()
    
    def create_multiple_choice_widgets(self, options: List[str]):
        """Create radio button widgets for multiple choice questions."""
        self.current_answer = tk.StringVar()
        
        for i, option in enumerate(options):
            radio = ttk.Radiobutton(self.answer_frame, text=option, 
                                   variable=self.current_answer, value=option,
                                   command=self.on_answer_change)
            radio.pack(anchor='w', pady=5)
            self.answer_widgets.append(radio)
    
    def create_multiple_select_widgets(self, options: List[str]):
        """Create checkbox widgets for multiple select questions."""
        self.current_answer = {}
        
        instruction_label = ttk.Label(self.answer_frame, 
                                     text="Select all that apply:", 
                                     style='Info.TLabel', font=('Arial', 10, 'italic'))
        instruction_label.pack(anchor='w', pady=(0, 10))
        self.answer_widgets.append(instruction_label)
        
        for option in options:
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(self.answer_frame, text=option, 
                                      variable=var, command=self.on_answer_change)
            checkbox.pack(anchor='w', pady=5)
            self.answer_widgets.append(checkbox)
            self.current_answer[option] = var
    
    def create_true_false_widgets(self):
        """Create radio button widgets for true/false questions."""
        self.current_answer = tk.StringVar()
        
        true_radio = ttk.Radiobutton(self.answer_frame, text="True", 
                                    variable=self.current_answer, value="True",
                                    command=self.on_answer_change)
        true_radio.pack(anchor='w', pady=5)
        self.answer_widgets.append(true_radio)
        
        false_radio = ttk.Radiobutton(self.answer_frame, text="False", 
                                     variable=self.current_answer, value="False",
                                     command=self.on_answer_change)
        false_radio.pack(anchor='w', pady=5)
        self.answer_widgets.append(false_radio)
    
    def on_answer_change(self):
        """Handle answer selection changes."""
        # Enable submit button when an answer is selected
        self.submit_button.config(state='normal')
    
    def get_selected_answer(self) -> Any:
        """Get the currently selected answer."""
        question = self.quiz_logic.get_current_question()
        question_type = question['type']
        
        if question_type in ['multiple_choice', 'true_false']:
            return self.current_answer.get() if self.current_answer.get() else None
        
        elif question_type == 'multiple_select':
            selected = []
            for option, var in self.current_answer.items():
                if var.get():
                    selected.append(option)
            return selected if selected else None
        
        return None
    
    def load_previous_answer(self):
        """Load previously submitted answer for this question."""
        question_index = self.quiz_logic.current_question_index
        previous_answer = self.quiz_logic.user_answers[question_index]
        
        if previous_answer is None:
            self.submit_button.config(state='disabled')
            return
        
        question = self.quiz_logic.get_current_question()
        question_type = question['type']
        
        if question_type in ['multiple_choice', 'true_false']:
            self.current_answer.set(previous_answer)
        elif question_type == 'multiple_select':
            if isinstance(previous_answer, list):
                for option, var in self.current_answer.items():
                    var.set(option in previous_answer)
        
        self.submit_button.config(state='normal')
        
        # Show feedback if answer was already submitted
        result = self.quiz_logic.question_results[question_index]
        if result:
            self.show_feedback(result)
    
    def submit_answer(self):
        """Submit the current answer."""
        selected_answer = self.get_selected_answer()
        
        if selected_answer is None:
            messagebox.showwarning("No Answer Selected", 
                                 "Please select an answer before submitting.")
            return
        
        try:
            feedback = self.quiz_logic.submit_answer(selected_answer)
            self.show_feedback(feedback)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit answer: {str(e)}")
    
    def show_feedback(self, feedback: Dict):
        """Display feedback for the submitted answer."""
        # Show feedback frame
        self.feedback_frame.pack(fill='x', pady=(20, 0))
        
        # Prepare feedback text
        feedback_text = ""
        
        if feedback.get('is_correct', False):
            feedback_text += "✓ Correct!\n\n"
        else:
            feedback_text += "✗ Incorrect\n\n"
            feedback_text += f"Correct answer: {feedback.get('correct_answer', 'N/A')}\n\n"
        
        explanation = feedback.get('explanation', '')
        if explanation:
            feedback_text += f"Explanation:\n{explanation}"
        
        # Display feedback
        self.feedback_text.config(state='normal')
        self.feedback_text.delete('1.0', 'end')
        self.feedback_text.insert('1.0', feedback_text)
        self.feedback_text.config(state='disabled')
        
        # Configure text colors
        if feedback.get('is_correct', False):
            self.feedback_text.tag_add('correct', '1.0', '1.end')
            self.feedback_text.tag_config('correct', foreground=COLORS['success'], 
                                         font=('Arial', 10, 'bold'))
        else:
            self.feedback_text.tag_add('incorrect', '1.0', '1.end')
            self.feedback_text.tag_config('incorrect', foreground=COLORS['error'], 
                                         font=('Arial', 10, 'bold'))
        
        # Disable submit button after submission
        self.submit_button.config(state='disabled')
    
    def hide_feedback(self):
        """Hide the feedback frame."""
        self.feedback_frame.pack_forget()
    
    def update_navigation_buttons(self):
        """Update the state of navigation buttons."""
        # Back button
        if self.quiz_logic.can_go_back():
            self.back_button.config(state='normal')
        else:
            self.back_button.config(state='disabled')
        
        # Next button
        if self.quiz_logic.can_go_forward():
            self.next_button.config(text="Next →")
        else:
            self.next_button.config(text="Finish Quiz")
    
    def go_back(self):
        """Go to the previous question."""
        if self.quiz_logic.go_to_previous_question():
            self.load_current_question()
    
    def go_next(self):
        """Go to the next question or finish the quiz."""
        # Check if current question is answered
        current_result = self.quiz_logic.question_results[self.quiz_logic.current_question_index]
        if current_result is None:
            response = messagebox.askyesno("Unanswered Question", 
                                         "You haven't answered this question yet. Continue anyway?")
            if not response:
                return
        
        if self.quiz_logic.go_to_next_question():
            if self.quiz_logic.quiz_completed:
                self.completion_callback()
            else:
                self.load_current_question()
    
    def get_quiz_status(self) -> Dict:
        """Get current quiz status information."""
        progress = self.quiz_logic.get_question_progress()
        answered_count = sum(1 for result in self.quiz_logic.question_results if result is not None)
        
        return {
            'current_question': progress['current'],
            'total_questions': progress['total'],
            'answered_questions': answered_count,
            'progress_percentage': progress['percentage']
        }
