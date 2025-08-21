"""
PDF report generation utilities for the Pharmaceutical Quiz Module.
Creates professional PDF reports of quiz results using fpdf.
"""

from fpdf import FPDF
import io
from datetime import datetime
from typing import Dict, Optional
import logging


class PDFReportGenerator:
    """Generates professional PDF reports for quiz results."""
    
    def __init__(self):
        self.pdf = None
        self.colors = {
            'primary': (31, 78, 121),      # #1f4e79
            'secondary': (46, 117, 182),   # #2e75b6
            'success': (40, 167, 69),      # #28a745
            'error': (220, 53, 69),        # #dc3545
            'gray': (108, 117, 125)        # #6c757d
        }
    
    def generate_report(self, results: Dict) -> Optional[bytes]:
        """
        Generate a comprehensive PDF report from quiz results.
        
        Args:
            results: Quiz results dictionary
            
        Returns:
            PDF data as bytes if successful, None otherwise
        """
        try:
            self.pdf = FPDF()
            self.pdf.add_page()
            self.pdf.set_auto_page_break(auto=True, margin=15)
            
            # Generate report sections
            self._add_header(results)
            self._add_executive_summary(results)
            self._add_performance_breakdown(results)
            self._add_recommendations(results)
            self._add_question_details(results)
            self._add_footer()
            
            # Return PDF as bytes
            return bytes(self.pdf.output())
            
        except Exception as e:
            logging.error(f"Error generating PDF report: {e}")
            return None
    
    def _add_header(self, results: Dict):
        """Add report header with company branding."""
        user_data = results['user_data']
        
        # Title
        self.pdf.set_font('Arial', 'B', 20)
        self.pdf.set_text_color(*self.colors['primary'])
        self.pdf.cell(0, 15, 'Pharmaceutical Therapy Area Knowledge Quiz', ln=True, align='C')
        
        # Subtitle
        self.pdf.set_font('Arial', '', 14)
        self.pdf.set_text_color(*self.colors['gray'])
        self.pdf.cell(0, 10, 'Assessment Report', ln=True, align='C')
        
        self.pdf.ln(10)
        
        # Project information
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(0, 8, 'Project Information', ln=True)
        
        self.pdf.set_font('Arial', '', 10)
        info_items = [
            f"Project: {user_data.get('project_name', 'N/A')}",
            f"Client: {user_data.get('client_name', 'N/A')}",
            f"Therapy Area: {user_data.get('therapy_area', 'N/A')}",
            f"Indication: {user_data.get('indication', 'N/A')}",
            f"Project Type: {user_data.get('project_type', 'N/A')}",
            f"Completion Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ]
        
        for item in info_items:
            self.pdf.cell(0, 6, item, ln=True)
        
        self.pdf.ln(10)
    
    def _add_executive_summary(self, results: Dict):
        """Add executive summary section."""
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*self.colors['primary'])
        self.pdf.cell(0, 10, 'Executive Summary', ln=True)
        
        # Overall performance
        score = results['score_percentage']
        grade = results['grade']
        passed = results['passed']
        
        # Score display
        if passed:
            self.pdf.set_text_color(*self.colors['success'])
            status = "PASSED"
        else:
            self.pdf.set_text_color(*self.colors['error'])
            status = "NEEDS IMPROVEMENT"
        
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 12, f"Overall Score: {score}% (Grade: {grade})", ln=True)
        self.pdf.cell(0, 10, f"Status: {status}", ln=True)
        
        # Key statistics
        self.pdf.set_font('Arial', '', 10)
        self.pdf.set_text_color(0, 0, 0)
        
        stats = [
            f"Questions Answered: {results['answered_questions']}/{results['total_questions']}",
            f"Correct Answers: {results['correct_answers']}",
            f"Experience Level: Level {results['user_data'].get('experience_level', 'N/A')}"
        ]
        
        for stat in stats:
            self.pdf.cell(0, 6, stat, ln=True)
        
        self.pdf.ln(10)
    
    def _add_performance_breakdown(self, results: Dict):
        """Add performance breakdown section."""
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*self.colors['primary'])
        self.pdf.cell(0, 10, 'Performance Breakdown', ln=True)
        
        # Category breakdown
        category_data = results.get('category_breakdown', {})
        if category_data:
            self.pdf.set_font('Arial', 'B', 12)
            self.pdf.set_text_color(0, 0, 0)
            self.pdf.cell(0, 8, 'By Knowledge Category:', ln=True)
            
            self.pdf.set_font('Arial', '', 10)
            for category, stats in category_data.items():
                percentage = stats['percentage']
                correct = stats['correct']
                total = stats['total']
                
                self.pdf.cell(0, 6, f"  {category}: {percentage:.1f}% ({correct}/{total})", ln=True)
        
        self.pdf.ln(5)
        
        # Difficulty breakdown
        difficulty_data = results.get('difficulty_breakdown', {})
        if difficulty_data:
            self.pdf.set_font('Arial', 'B', 12)
            self.pdf.cell(0, 8, 'By Question Difficulty:', ln=True)
            
            self.pdf.set_font('Arial', '', 10)
            for difficulty, stats in difficulty_data.items():
                percentage = stats['percentage']
                correct = stats['correct']
                total = stats['total']
                
                self.pdf.cell(0, 6, f"  {difficulty.title()}: {percentage:.1f}% ({correct}/{total})", ln=True)
        
        self.pdf.ln(10)
    
    def _add_recommendations(self, results: Dict):
        """Add recommendations section."""
        recommendations = results.get('recommendations', [])
        
        if not recommendations:
            return
        
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*self.colors['primary'])
        self.pdf.cell(0, 10, 'Recommendations', ln=True)
        
        self.pdf.set_font('Arial', '', 10)
        self.pdf.set_text_color(0, 0, 0)
        
        for i, recommendation in enumerate(recommendations, 1):
            # Wrap long text
            wrapped_text = self._wrap_text(f"{i}. {recommendation}", 80)
            for line in wrapped_text:
                self.pdf.cell(0, 6, line, ln=True)
            self.pdf.ln(2)
        
        self.pdf.ln(5)
    
    def _add_question_details(self, results: Dict):
        """Add detailed question analysis."""
        question_results = results.get('question_results', [])
        
        if not question_results:
            return
        
        self.pdf.set_font('Arial', 'B', 14)
        self.pdf.set_text_color(*self.colors['primary'])
        self.pdf.cell(0, 10, 'Question Details', ln=True)
        
        for i, result in enumerate(question_results, 1):
            if result is None:
                continue
            
            question = result['question']
            is_correct = result['is_correct']
            user_answer = result['user_answer']
            correct_answer = result['correct_answer']
            
            # Question header
            self.pdf.set_font('Arial', 'B', 11)
            if is_correct:
                self.pdf.set_text_color(*self.colors['success'])
                status = "CORRECT"
            else:
                self.pdf.set_text_color(*self.colors['error'])
                status = "INCORRECT"
            
            self.pdf.cell(0, 8, f"Question {i}: {status}", ln=True)
            
            # Question details
            self.pdf.set_font('Arial', '', 9)
            self.pdf.set_text_color(0, 0, 0)
            
            # Question text (wrapped)
            question_text = self._wrap_text(f"Q: {question['question']}", 90)
            for line in question_text:
                self.pdf.cell(0, 5, line, ln=True)
            
            # Answers
            self.pdf.cell(0, 5, f"Your Answer: {user_answer}", ln=True)
            self.pdf.cell(0, 5, f"Correct Answer: {correct_answer}", ln=True)
            
            # Category and difficulty
            category = question.get('category', 'N/A')
            difficulty = question.get('difficulty', 'N/A')
            self.pdf.cell(0, 5, f"Category: {category} | Difficulty: {difficulty.title()}", ln=True)
            
            self.pdf.ln(3)
            
            # Check if we need a new page
            if self.pdf.get_y() > 250:
                self.pdf.add_page()
    
    def _add_footer(self):
        """Add report footer."""
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'I', 8)
        self.pdf.set_text_color(*self.colors['gray'])
        self.pdf.cell(0, 5, f"Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M')}", ln=True, align='C')
        self.pdf.cell(0, 5, "Pharmaceutical Therapy Area Knowledge Quiz Module", ln=True, align='C')
    
    def _wrap_text(self, text: str, max_length: int) -> list:
        """Wrap text to fit within specified character length."""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_length:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
