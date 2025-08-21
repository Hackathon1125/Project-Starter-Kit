#!/usr/bin/env python3
"""
Test script for the Pharmaceutical Quiz Module.
Tests basic functionality without requiring API keys.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_handler import DataHandler
from utils.document_processor import DocumentProcessor
from quiz_engine.quiz_logic import QuizLogic
from quiz_engine.feedback_system import FeedbackSystem


class TestPharmaceuticalQuiz(unittest.TestCase):
    """Test cases for the pharmaceutical quiz module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_user_data = {
            'project_name': 'Test Project',
            'client_name': 'Test Client',
            'therapy_area': 'Oncology',
            'indication': 'Breast Cancer',
            'project_type': 'ATU',
            'client_scenario': 'Scenario 1: New Client, Baseline Wave (Wave 1)',
            'experience_level': 3,
            'additional_therapy': '',
            'brand_name': 'TestDrug',
            'generic_name': 'testamab',
            'selected_files': []
        }
        
        self.sample_questions = [
            {
                'question': 'What is the primary mechanism of action for HER2-targeted therapies?',
                'type': 'multiple_choice',
                'options': [
                    'Inhibition of HER2 receptor signaling',
                    'DNA intercalation',
                    'Microtubule stabilization',
                    'Topoisomerase inhibition'
                ],
                'correct_answer': 'Inhibition of HER2 receptor signaling',
                'explanation': 'HER2-targeted therapies work by specifically blocking HER2 receptor signaling pathways.',
                'difficulty': 'intermediate',
                'category': 'Therapy Area Knowledge'
            },
            {
                'question': 'Which regulatory agencies must approve new oncology drugs in major markets?',
                'type': 'multiple_select',
                'options': [
                    'FDA (United States)',
                    'EMA (European Union)',
                    'PMDA (Japan)',
                    'WHO (Global)'
                ],
                'correct_answer': ['FDA (United States)', 'EMA (European Union)', 'PMDA (Japan)'],
                'explanation': 'FDA, EMA, and PMDA are the primary regulatory agencies for drug approval in major markets.',
                'difficulty': 'fundamental',
                'category': 'Regulatory & Market Access'
            }
        ]
    
    def test_data_handler_initialization(self):
        """Test DataHandler initialization."""
        handler = DataHandler()
        self.assertIsInstance(handler, DataHandler)
        self.assertEqual(handler.session_data, {})
    
    def test_data_handler_session_storage(self):
        """Test session data storage and retrieval."""
        handler = DataHandler()
        
        # Store data
        test_data = {'key': 'value', 'number': 42}
        handler.store_session_data('test_key', test_data)
        
        # Retrieve data
        retrieved_data = handler.get_session_data('test_key')
        self.assertEqual(retrieved_data, test_data)
        
        # Test default value
        default_data = handler.get_session_data('nonexistent_key', 'default')
        self.assertEqual(default_data, 'default')
    
    def test_document_processor_initialization(self):
        """Test DocumentProcessor initialization."""
        processor = DocumentProcessor()
        self.assertIsInstance(processor, DocumentProcessor)
        self.assertEqual(processor.supported_extensions, {'.pdf', '.docx', '.pptx', '.xlsx'})
    
    def test_document_processor_file_validation(self):
        """Test file validation logic."""
        processor = DocumentProcessor()
        
        # Test with empty file list
        result = processor.validate_files([])
        self.assertEqual(result['valid_files'], [])
        self.assertEqual(result['invalid_files'], [])
        self.assertEqual(result['errors'], [])
    
    @patch('utils.ai_integration.AIQuestionGenerator')
    def test_quiz_logic_initialization(self, mock_ai_generator):
        """Test QuizLogic initialization."""
        handler = DataHandler()
        quiz_logic = QuizLogic(self.test_user_data, handler)
        
        self.assertEqual(quiz_logic.user_data, self.test_user_data)
        self.assertEqual(quiz_logic.current_question_index, 0)
        self.assertFalse(quiz_logic.quiz_started)
        self.assertFalse(quiz_logic.quiz_completed)
    
    @patch('utils.ai_integration.AIQuestionGenerator')
    def test_quiz_logic_mock_questions(self, mock_ai_generator):
        """Test quiz logic with mock questions."""
        # Mock the AI generator
        mock_generator_instance = Mock()
        mock_generator_instance.generate_questions.return_value = self.sample_questions
        mock_ai_generator.return_value = mock_generator_instance
        
        handler = DataHandler()
        quiz_logic = QuizLogic(self.test_user_data, handler)
        
        # Test question generation
        result = quiz_logic.generate_questions(2)
        self.assertTrue(result)
        self.assertEqual(len(quiz_logic.questions), 2)
        
        # Test quiz start
        quiz_logic.start_quiz()
        self.assertTrue(quiz_logic.quiz_started)
        
        # Test getting current question
        current_question = quiz_logic.get_current_question()
        self.assertIsNotNone(current_question)
        self.assertIn('question', current_question)
        
        # Test progress tracking
        progress = quiz_logic.get_question_progress()
        self.assertEqual(progress['current'], 1)
        self.assertEqual(progress['total'], 2)
    
    @patch('utils.ai_integration.AIQuestionGenerator')
    def test_quiz_answer_submission(self, mock_ai_generator):
        """Test answer submission and feedback."""
        # Mock the AI generator
        mock_generator_instance = Mock()
        mock_generator_instance.generate_questions.return_value = self.sample_questions
        mock_ai_generator.return_value = mock_generator_instance
        
        handler = DataHandler()
        quiz_logic = QuizLogic(self.test_user_data, handler)
        quiz_logic.generate_questions(2)
        quiz_logic.start_quiz()
        
        # Test correct answer submission
        correct_answer = 'Inhibition of HER2 receptor signaling'
        feedback = quiz_logic.submit_answer(correct_answer)
        
        self.assertTrue(feedback['is_correct'])
        self.assertEqual(feedback['user_answer'], correct_answer)
        self.assertEqual(feedback['correct_answer'], correct_answer)
        
        # Test incorrect answer submission
        quiz_logic.go_to_next_question()
        incorrect_answer = ['FDA (United States)']  # Missing other correct answers
        feedback = quiz_logic.submit_answer(incorrect_answer)
        
        self.assertFalse(feedback['is_correct'])
        self.assertEqual(feedback['user_answer'], incorrect_answer)
    
    def test_feedback_system(self):
        """Test feedback system functionality."""
        feedback_system = FeedbackSystem()
        
        question = self.sample_questions[0]
        user_answer = 'Inhibition of HER2 receptor signaling'
        
        # Test correct answer feedback
        feedback = feedback_system.generate_feedback(question, user_answer, True)
        self.assertTrue(feedback['is_correct'])
        self.assertEqual(feedback['user_answer'], user_answer)
        self.assertIn('learning_points', feedback)
        
        # Test feedback text formatting
        feedback_text = feedback_system.format_feedback_text(feedback)
        self.assertIn('✓ Correct', feedback_text)
        self.assertIn('Explanation:', feedback_text)
    
    def test_configuration_loading(self):
        """Test configuration loading."""
        from config.settings import (
            EXPERIENCE_LEVELS, DIFFICULTY_DISTRIBUTION, 
            PROJECT_TYPES, CLIENT_SCENARIOS
        )
        
        # Test experience levels
        self.assertEqual(len(EXPERIENCE_LEVELS), 7)
        self.assertIn(1, EXPERIENCE_LEVELS)
        self.assertIn(7, EXPERIENCE_LEVELS)
        
        # Test difficulty distribution
        self.assertEqual(len(DIFFICULTY_DISTRIBUTION), 7)
        for level in range(1, 8):
            self.assertIn(level, DIFFICULTY_DISTRIBUTION)
            dist = DIFFICULTY_DISTRIBUTION[level]
            self.assertIn('fundamental', dist)
            self.assertIn('intermediate', dist)
            self.assertIn('advanced', dist)
            # Check percentages sum to 100
            total = dist['fundamental'] + dist['intermediate'] + dist['advanced']
            self.assertEqual(total, 100)
        
        # Test project types and scenarios
        self.assertIsInstance(PROJECT_TYPES, list)
        self.assertIsInstance(CLIENT_SCENARIOS, list)
        self.assertTrue(len(PROJECT_TYPES) > 0)
        self.assertTrue(len(CLIENT_SCENARIOS) > 0)


def run_basic_functionality_test():
    """Run a basic functionality test without GUI."""
    print("Running Pharmaceutical Quiz Module Tests...")
    print("=" * 60)
    
    try:
        # Test 1: Configuration loading
        print("Testing configuration loading...")
        from config.settings import EXPERIENCE_LEVELS, PROJECT_TYPES
        assert len(EXPERIENCE_LEVELS) == 7
        assert len(PROJECT_TYPES) > 0
        print("  [PASS] Configuration loaded successfully")
        
        # Test 2: Data handler
        print("Testing data handler...")
        handler = DataHandler()
        handler.store_session_data('test', {'value': 123})
        retrieved = handler.get_session_data('test')
        assert retrieved['value'] == 123
        print("  [PASS] Data handler working correctly")
        
        # Test 3: Document processor
        print("Testing document processor...")
        processor = DocumentProcessor()
        validation = processor.validate_files([])
        assert 'valid_files' in validation
        print("  [PASS] Document processor initialized correctly")
        
        # Test 4: Feedback system
        print("Testing feedback system...")
        feedback_system = FeedbackSystem()
        sample_question = {
            'question': 'Test question?',
            'type': 'multiple_choice',
            'options': ['A', 'B', 'C'],
            'correct_answer': 'A',
            'explanation': 'A is correct because...',
            'category': 'Test Category',
            'difficulty': 'intermediate'
        }
        feedback = feedback_system.generate_feedback(sample_question, 'A', True)
        assert feedback['is_correct'] == True
        print("  [PASS] Feedback system working correctly")
        
        print("\nAll basic functionality tests passed!")
        print("The pharmaceutical quiz module is ready to use.")
        print("\nNext steps:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI or Anthropic API key to .env")
        print("  3. Run: python main.py")
        
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run basic functionality test
    success = run_basic_functionality_test()
    
    if success:
        print("\n" + "=" * 60)
        print("Ready to launch the Pharmaceutical Quiz Module!")
        print("   Run 'python main.py' to start the application.")
    else:
        print("\n" + "=" * 60)
        print("Some tests failed. Please check the error messages above.")
        
    # Optionally run unit tests
    print("\n" + "-" * 40)
    response = input("Run detailed unit tests? (y/n): ").lower().strip()
    if response == 'y':
        unittest.main(verbosity=2)
