"""
Feedback system for the Pharmaceutical Quiz Module.
Provides detailed explanations and learning guidance.
"""

import logging
from typing import Dict, List, Any
from config.settings import COLORS


class FeedbackSystem:
    """Handles feedback generation and display for quiz questions."""
    
    def __init__(self):
        self.feedback_templates = {
            'correct': [
                "Excellent! That's the correct answer.",
                "Well done! You got it right.",
                "Correct! Great job.",
                "Perfect! That's exactly right."
            ],
            'incorrect': [
                "Not quite right, but good effort!",
                "That's incorrect, but let's learn from this.",
                "Close, but not the right answer.",
                "Incorrect, but this is a learning opportunity."
            ]
        }
    
    def generate_feedback(self, question: Dict, user_answer: Any, is_correct: bool) -> Dict:
        """
        Generate comprehensive feedback for a question response.
        
        Args:
            question: The question dictionary
            user_answer: The user's submitted answer
            is_correct: Whether the answer was correct
            
        Returns:
            Dictionary containing feedback information
        """
        feedback = {
            'is_correct': is_correct,
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'explanation': question.get('explanation', ''),
            'category': question.get('category', 'General'),
            'difficulty': question.get('difficulty', 'intermediate'),
            'learning_points': self._extract_learning_points(question, is_correct),
            'color_code': COLORS['success'] if is_correct else COLORS['error']
        }
        
        # Add detailed option analysis for multiple choice questions
        if question['type'] == 'multiple_choice':
            feedback['option_analysis'] = self._analyze_options(question, user_answer)
        
        return feedback
    
    def _extract_learning_points(self, question: Dict, is_correct: bool) -> List[str]:
        """Extract key learning points from the question."""
        learning_points = []
        
        # Add category-specific learning points
        category = question.get('category', '').lower()
        if 'therapy area' in category:
            learning_points.append("Focus on understanding the specific therapeutic mechanisms and pathways")
        elif 'competitive' in category:
            learning_points.append("Review current market landscape and competitor positioning")
        elif 'regulatory' in category:
            learning_points.append("Study regulatory requirements and market access considerations")
        elif 'methodology' in category:
            learning_points.append("Practice pharmaceutical research methodologies and best practices")
        
        # Add difficulty-specific guidance
        difficulty = question.get('difficulty', 'intermediate')
        if difficulty == 'fundamental' and not is_correct:
            learning_points.append("Review basic concepts in this therapy area")
        elif difficulty == 'advanced' and not is_correct:
            learning_points.append("Consider advanced training or mentoring in this topic")
        
        return learning_points
    
    def _analyze_options(self, question: Dict, user_answer: Any) -> Dict:
        """Analyze why each option is correct or incorrect."""
        analysis = {}
        correct_answer = question['correct_answer']
        
        for option in question['options']:
            if option == correct_answer:
                analysis[option] = {
                    'status': 'correct',
                    'reason': 'This is the correct answer based on current pharmaceutical standards and practices.'
                }
            else:
                analysis[option] = {
                    'status': 'incorrect',
                    'reason': 'This option is incorrect because it does not align with established guidelines or best practices.'
                }
        
        return analysis
    
    def format_feedback_text(self, feedback: Dict) -> str:
        """Format feedback into a readable text format."""
        text_parts = []
        
        # Status
        if feedback['is_correct']:
            text_parts.append("✓ Correct Answer!")
        else:
            text_parts.append("✗ Incorrect Answer")
            text_parts.append(f"Correct answer: {feedback['correct_answer']}")
        
        # Explanation
        if feedback['explanation']:
            text_parts.append(f"\nExplanation:\n{feedback['explanation']}")
        
        # Learning points
        if feedback['learning_points']:
            text_parts.append("\nKey Learning Points:")
            for point in feedback['learning_points']:
                text_parts.append(f"• {point}")
        
        return "\n".join(text_parts)
    
    def get_performance_insights(self, results: List[Dict]) -> Dict:
        """Generate performance insights from multiple question results."""
        if not results:
            return {}
        
        total_questions = len(results)
        correct_count = sum(1 for r in results if r and r.get('is_correct', False))
        
        # Category performance
        category_performance = {}
        for result in results:
            if not result:
                continue
            category = result.get('category', 'General')
            if category not in category_performance:
                category_performance[category] = {'total': 0, 'correct': 0}
            category_performance[category]['total'] += 1
            if result.get('is_correct', False):
                category_performance[category]['correct'] += 1
        
        # Difficulty performance
        difficulty_performance = {}
        for result in results:
            if not result:
                continue
            difficulty = result.get('difficulty', 'intermediate')
            if difficulty not in difficulty_performance:
                difficulty_performance[difficulty] = {'total': 0, 'correct': 0}
            difficulty_performance[difficulty]['total'] += 1
            if result.get('is_correct', False):
                difficulty_performance[difficulty]['correct'] += 1
        
        # Generate insights
        insights = {
            'overall_score': (correct_count / total_questions * 100) if total_questions > 0 else 0,
            'strengths': [],
            'areas_for_improvement': [],
            'category_performance': category_performance,
            'difficulty_performance': difficulty_performance
        }
        
        # Identify strengths and weaknesses
        for category, perf in category_performance.items():
            percentage = (perf['correct'] / perf['total'] * 100) if perf['total'] > 0 else 0
            if percentage >= 80:
                insights['strengths'].append(f"Strong performance in {category} ({percentage:.1f}%)")
            elif percentage < 60:
                insights['areas_for_improvement'].append(f"Needs improvement in {category} ({percentage:.1f}%)")
        
        return insights
    
    def generate_study_recommendations(self, insights: Dict, user_data: Dict) -> List[str]:
        """Generate personalized study recommendations."""
        recommendations = []
        
        therapy_area = user_data.get('therapy_area', '')
        experience_level = user_data.get('experience_level', 1)
        
        # Overall performance recommendations
        overall_score = insights.get('overall_score', 0)
        if overall_score < 50:
            recommendations.append(f"Consider foundational training in {therapy_area} before project onboarding")
        elif overall_score < 70:
            recommendations.append("Review key concepts and seek mentoring support")
        elif overall_score < 85:
            recommendations.append("Focus on specific weak areas identified in the results")
        else:
            recommendations.append("Excellent performance - ready for advanced project responsibilities")
        
        # Category-specific recommendations
        for area in insights.get('areas_for_improvement', []):
            if 'Therapy Area Knowledge' in area:
                recommendations.append(f"Study clinical guidelines and treatment pathways for {therapy_area}")
            elif 'Competitive Landscape' in area:
                recommendations.append("Research current market competitors and their positioning strategies")
            elif 'Regulatory' in area:
                recommendations.append("Review FDA/EMA guidelines and market access requirements")
            elif 'Methodology' in area:
                recommendations.append("Practice pharmaceutical research methodologies and data analysis")
        
        # Experience level recommendations
        if experience_level <= 3:
            recommendations.append("Consider pairing with a senior consultant for initial projects")
        elif experience_level >= 6:
            recommendations.append("Consider mentoring junior team members in your areas of strength")
        
        return recommendations[:5]  # Limit to top 5 recommendations
