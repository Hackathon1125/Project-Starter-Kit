"""
Core quiz logic for the Pharmaceutical Quiz Module.
Handles quiz flow, scoring, and state management.
"""

import random
import logging
from typing import List, Dict, Optional, Any
from utils.ai_integration import AIQuestionGenerator
from utils.document_processor import DocumentProcessor
from config.settings import DEFAULT_QUESTION_COUNT, PASS_THRESHOLD


class QuizLogic:
    """Main quiz logic controller."""
    
    def __init__(self, user_data: Dict, data_handler):
        self.user_data = user_data
        self.data_handler = data_handler
        self.ai_generator = AIQuestionGenerator()
        self.doc_processor = DocumentProcessor()
        
        # Quiz state
        self.questions: List[Dict] = []
        self.current_question_index = 0
        self.user_answers: List[Any] = []
        self.question_results: List[Dict] = []
        self.quiz_started = False
        self.quiz_completed = False
        
        # Document context
        self.document_context = ""
        
        # Process uploaded documents if any
        self._process_documents()
    
    def _process_documents(self):
        """Process uploaded documents to extract context."""
        if self.user_data.get('selected_files'):
            try:
                self.document_context = self.doc_processor.process_files(
                    self.user_data['selected_files']
                )
                logging.info(f"Processed {len(self.user_data['selected_files'])} documents")
            except Exception as e:
                logging.warning(f"Failed to process documents: {e}")
                self.document_context = ""
    
    def generate_questions(self, question_count: int = DEFAULT_QUESTION_COUNT) -> bool:
        """
        Generate quiz questions using AI.
        
        Args:
            question_count: Number of questions to generate
            
        Returns:
            True if questions were successfully generated, False otherwise
        """
        try:
            # Add document context to user data if available
            enhanced_user_data = self.user_data.copy()
            if self.document_context:
                enhanced_user_data['document_context'] = self.document_context
            
            # Generate questions
            self.questions = self.ai_generator.generate_questions(
                enhanced_user_data, question_count
            )
            
            if not self.questions:
                logging.error("No questions were generated")
                return False
            
            # Shuffle questions for variety
            random.shuffle(self.questions)
            
            # Initialize answer tracking
            self.user_answers = [None] * len(self.questions)
            self.question_results = [None] * len(self.questions)
            
            logging.info(f"Generated {len(self.questions)} questions")
            return True
            
        except Exception as e:
            logging.error(f"Failed to generate questions: {e}")
            return False
    
    def start_quiz(self):
        """Start the quiz."""
        if not self.questions:
            raise Exception("No questions available. Generate questions first.")
        
        self.quiz_started = True
        self.current_question_index = 0
        logging.info("Quiz started")
    
    def get_current_question(self) -> Optional[Dict]:
        """Get the current question."""
        if not self.quiz_started or self.current_question_index >= len(self.questions):
            return None
        
        return self.questions[self.current_question_index]
    
    def get_question_progress(self) -> Dict:
        """Get current progress information."""
        return {
            'current': self.current_question_index + 1,
            'total': len(self.questions),
            'percentage': int((self.current_question_index / len(self.questions)) * 100) if self.questions else 0
        }
    
    def submit_answer(self, answer: Any) -> Dict:
        """
        Submit an answer for the current question.
        
        Args:
            answer: The user's answer (string for single choice, list for multiple choice)
            
        Returns:
            Dictionary with feedback information
        """
        if not self.quiz_started or self.current_question_index >= len(self.questions):
            raise Exception("No active question to answer")
        
        current_question = self.questions[self.current_question_index]
        correct_answer = current_question['correct_answer']
        
        # Store the user's answer
        self.user_answers[self.current_question_index] = answer
        
        # Check if answer is correct
        is_correct = self._check_answer(answer, correct_answer, current_question['type'])
        
        # Create result record
        result = {
            'question_index': self.current_question_index,
            'user_answer': answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'question': current_question,
            'timestamp': self.data_handler.get_timestamp()
        }
        
        self.question_results[self.current_question_index] = result
        
        # Prepare feedback
        feedback = {
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'explanation': current_question.get('explanation', ''),
            'user_answer': answer
        }
        
        logging.info(f"Question {self.current_question_index + 1} answered: {'Correct' if is_correct else 'Incorrect'}")
        
        return feedback
    
    def _check_answer(self, user_answer: Any, correct_answer: Any, question_type: str) -> bool:
        """Check if the user's answer is correct."""
        if question_type == 'multiple_select':
            # For multiple select, both answers should be lists
            if not isinstance(user_answer, list) or not isinstance(correct_answer, list):
                return False
            
            # Sort both lists for comparison
            user_sorted = sorted(user_answer) if user_answer else []
            correct_sorted = sorted(correct_answer) if correct_answer else []
            
            return user_sorted == correct_sorted
        
        elif question_type in ['multiple_choice', 'true_false']:
            # For single choice questions
            return str(user_answer).strip().lower() == str(correct_answer).strip().lower()
        
        return False
    
    def can_go_back(self) -> bool:
        """Check if user can go back to previous question."""
        return self.current_question_index > 0
    
    def can_go_forward(self) -> bool:
        """Check if user can go forward to next question."""
        return self.current_question_index < len(self.questions) - 1
    
    def go_to_previous_question(self) -> bool:
        """Go to the previous question."""
        if self.can_go_back():
            self.current_question_index -= 1
            return True
        return False
    
    def go_to_next_question(self) -> bool:
        """Go to the next question."""
        if self.can_go_forward():
            self.current_question_index += 1
            return True
        elif self.current_question_index == len(self.questions) - 1:
            # Last question - complete the quiz
            self.complete_quiz()
            return True
        return False
    
    def complete_quiz(self):
        """Complete the quiz and calculate final results."""
        self.quiz_completed = True
        logging.info("Quiz completed")
    
    def get_results(self) -> Dict:
        """Get comprehensive quiz results."""
        if not self.quiz_completed:
            raise Exception("Quiz not completed yet")
        
        # Calculate basic statistics
        total_questions = len(self.questions)
        answered_questions = sum(1 for result in self.question_results if result is not None)
        correct_answers = sum(1 for result in self.question_results 
                            if result is not None and result['is_correct'])
        
        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        passed = score_percentage >= (PASS_THRESHOLD * 100)
        
        # Category breakdown
        category_stats = self._calculate_category_stats()
        
        # Difficulty breakdown
        difficulty_stats = self._calculate_difficulty_stats()
        
        # Grade calculation
        grade = self._calculate_grade(score_percentage)
        
        results = {
            'user_data': self.user_data,
            'total_questions': total_questions,
            'answered_questions': answered_questions,
            'correct_answers': correct_answers,
            'score_percentage': round(score_percentage, 1),
            'passed': passed,
            'grade': grade,
            'category_breakdown': category_stats,
            'difficulty_breakdown': difficulty_stats,
            'question_results': self.question_results,
            'completion_time': self.data_handler.get_timestamp(),
            'recommendations': self._generate_recommendations(category_stats, difficulty_stats)
        }
        
        return results
    
    def _calculate_category_stats(self) -> Dict:
        """Calculate statistics by question category."""
        categories = {}
        
        for result in self.question_results:
            if result is None:
                continue
                
            category = result['question'].get('category', 'General')
            
            if category not in categories:
                categories[category] = {'total': 0, 'correct': 0}
            
            categories[category]['total'] += 1
            if result['is_correct']:
                categories[category]['correct'] += 1
        
        # Calculate percentages
        for category, stats in categories.items():
            stats['percentage'] = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        return categories
    
    def _calculate_difficulty_stats(self) -> Dict:
        """Calculate statistics by question difficulty."""
        difficulties = {}
        
        for result in self.question_results:
            if result is None:
                continue
                
            difficulty = result['question'].get('difficulty', 'intermediate')
            
            if difficulty not in difficulties:
                difficulties[difficulty] = {'total': 0, 'correct': 0}
            
            difficulties[difficulty]['total'] += 1
            if result['is_correct']:
                difficulties[difficulty]['correct'] += 1
        
        # Calculate percentages
        for difficulty, stats in difficulties.items():
            stats['percentage'] = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        
        return difficulties
    
    def _calculate_grade(self, score_percentage: float) -> str:
        """Calculate letter grade based on score percentage."""
        if score_percentage >= 95:
            return 'A+'
        elif score_percentage >= 90:
            return 'A'
        elif score_percentage >= 85:
            return 'A-'
        elif score_percentage >= 80:
            return 'B+'
        elif score_percentage >= 75:
            return 'B'
        elif score_percentage >= 70:
            return 'B-'
        elif score_percentage >= 65:
            return 'C+'
        elif score_percentage >= 60:
            return 'C'
        elif score_percentage >= 55:
            return 'C-'
        elif score_percentage >= 50:
            return 'D'
        else:
            return 'F'
    
    def _generate_recommendations(self, category_stats: Dict, difficulty_stats: Dict) -> List[str]:
        """Generate personalized recommendations based on performance."""
        recommendations = []
        
        # Category-based recommendations
        for category, stats in category_stats.items():
            if stats['percentage'] < 60:
                recommendations.append(
                    f"Focus on improving {category} knowledge - scored {stats['percentage']:.1f}%"
                )
        
        # Difficulty-based recommendations
        for difficulty, stats in difficulty_stats.items():
            if stats['percentage'] < 50:
                recommendations.append(
                    f"Work on {difficulty} level concepts - scored {stats['percentage']:.1f}%"
                )
        
        # General recommendations based on overall performance
        overall_score = sum(stats['correct'] for stats in category_stats.values()) / \
                       sum(stats['total'] for stats in category_stats.values()) * 100
        
        if overall_score < 70:
            recommendations.append("Consider additional training before project onboarding")
        elif overall_score < 85:
            recommendations.append("Review weak areas and consider mentoring support")
        else:
            recommendations.append("Excellent performance - ready for project onboarding")
        
        return recommendations
    
    def reset_quiz(self):
        """Reset the quiz to initial state."""
        self.current_question_index = 0
        self.user_answers = [None] * len(self.questions)
        self.question_results = [None] * len(self.questions)
        self.quiz_started = False
        self.quiz_completed = False
        logging.info("Quiz reset")
    
    def get_quiz_summary(self) -> Dict:
        """Get a summary of the quiz configuration."""
        return {
            'user_data': self.user_data,
            'question_count': len(self.questions),
            'has_documents': bool(self.document_context),
            'experience_level': self.user_data.get('experience_level', 1),
            'therapy_area': self.user_data.get('therapy_area', ''),
            'project_type': self.user_data.get('project_type', '')
        }
