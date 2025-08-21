"""
AI integration module for question generation.
Supports both OpenAI and Anthropic Claude APIs.
"""

import json
import logging
from typing import List, Dict, Optional
import openai
import anthropic
from config.settings import (
    OPENAI_API_KEY, ANTHROPIC_API_KEY, AI_SYSTEM_PROMPT,
    DIFFICULTY_DISTRIBUTION, DEFAULT_QUESTION_COUNT, ERROR_MESSAGES
)


class AIQuestionGenerator:
    """Handles AI-powered question generation using OpenAI or Anthropic APIs."""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize AI API clients."""
        if OPENAI_API_KEY:
            try:
                self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
            except Exception as e:
                logging.warning(f"Failed to initialize OpenAI client: {e}")
        
        if ANTHROPIC_API_KEY:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            except Exception as e:
                logging.warning(f"Failed to initialize Anthropic client: {e}")
    
    def generate_questions(self, user_data: Dict, question_count: int = DEFAULT_QUESTION_COUNT) -> List[Dict]:
        """
        Generate quiz questions based on user data and experience level.
        
        Args:
            user_data: Dictionary containing user and project information
            question_count: Number of questions to generate
            
        Returns:
            List of question dictionaries
        """
        if not self.openai_client and not self.anthropic_client:
            raise Exception(ERROR_MESSAGES['api_key_missing'])
        
        # Calculate difficulty distribution
        experience_level = user_data.get('experience_level', 1)
        distribution = DIFFICULTY_DISTRIBUTION.get(experience_level, DIFFICULTY_DISTRIBUTION[1])
        
        # Calculate question counts by difficulty
        fundamental_count = int(question_count * distribution['fundamental'] / 100)
        intermediate_count = int(question_count * distribution['intermediate'] / 100)
        advanced_count = question_count - fundamental_count - intermediate_count
        
        # Generate questions for each difficulty level
        questions = []
        
        try:
            # Generate fundamental questions
            if fundamental_count > 0:
                fundamental_questions = self._generate_questions_by_difficulty(
                    user_data, "fundamental", fundamental_count
                )
                questions.extend(fundamental_questions)
            
            # Generate intermediate questions
            if intermediate_count > 0:
                intermediate_questions = self._generate_questions_by_difficulty(
                    user_data, "intermediate", intermediate_count
                )
                questions.extend(intermediate_questions)
            
            # Generate advanced questions
            if advanced_count > 0:
                advanced_questions = self._generate_questions_by_difficulty(
                    user_data, "advanced", advanced_count
                )
                questions.extend(advanced_questions)
            
            return questions
            
        except Exception as e:
            logging.error(f"Error generating questions: {e}")
            raise Exception(ERROR_MESSAGES['api_request_failed'])
    
    def _generate_questions_by_difficulty(self, user_data: Dict, difficulty: str, count: int) -> List[Dict]:
        """Generate questions for a specific difficulty level."""
        prompt = self._create_prompt(user_data, difficulty, count)
        
        # Try OpenAI first, then Anthropic
        if self.openai_client:
            try:
                return self._generate_with_openai(prompt)
            except Exception as e:
                logging.warning(f"OpenAI generation failed: {e}")
                if self.anthropic_client:
                    return self._generate_with_anthropic(prompt)
                else:
                    raise e
        elif self.anthropic_client:
            return self._generate_with_anthropic(prompt)
        else:
            raise Exception(ERROR_MESSAGES['api_key_missing'])
    
    def _create_prompt(self, user_data: Dict, difficulty: str, count: int) -> str:
        """Create a detailed prompt for question generation."""
        therapy_area = user_data.get('therapy_area', '')
        indication = user_data.get('indication', '')
        project_type = user_data.get('project_type', '')
        client_scenario = user_data.get('client_scenario', '')
        experience_level = user_data.get('experience_level', 1)
        
        additional_context = []
        if user_data.get('additional_therapy'):
            additional_context.append(f"Additional therapy area: {user_data['additional_therapy']}")
        if user_data.get('brand_name'):
            additional_context.append(f"Brand name(s): {user_data['brand_name']}")
        if user_data.get('generic_name'):
            additional_context.append(f"Generic name(s): {user_data['generic_name']}")
        
        context_str = "\n".join(additional_context) if additional_context else "No additional context provided."
        
        difficulty_descriptions = {
            "fundamental": "basic concepts, definitions, and general industry knowledge",
            "intermediate": "practical application, analysis, and methodology understanding",
            "advanced": "complex scenarios, strategic thinking, and expert-level insights"
        }
        
        prompt = f"""
{AI_SYSTEM_PROMPT}

Generate {count} {difficulty} level questions for a pharmaceutical consultant with experience level {experience_level}/7.

Project Context:
- Therapy Area: {therapy_area}
- Indication: {indication}
- Project Type: {project_type}
- Client Scenario: {client_scenario}
- {context_str}

Question Requirements:
- Difficulty Level: {difficulty} ({difficulty_descriptions[difficulty]})
- Question Types: Mix of multiple choice (4-5 options), multiple select (3-6 options), and true/false
- Focus Areas: Therapy area knowledge, competitive landscape, regulatory considerations, market access, methodology
- Professional Relevance: Questions should be directly applicable to pharmaceutical consulting work

Response Format:
Return ONLY a valid JSON array of question objects. No other text or formatting.

Example structure:
[
  {{
    "question": "Question text here",
    "type": "multiple_choice",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer": "Option 1",
    "explanation": "Detailed explanation here",
    "difficulty": "{difficulty}",
    "category": "Therapy Area Knowledge"
  }}
]

IMPORTANT: Return ONLY the JSON array, no markdown formatting, no explanatory text.

Ensure questions are:
1. Specific to {therapy_area} and {indication}
2. Appropriate for {difficulty} difficulty level
3. Relevant to {project_type} methodology
4. Professionally written and accurate
5. Include clear, educational explanations
"""
        
        return prompt
    
    def _generate_with_openai(self, prompt: str) -> List[Dict]:
        """Generate questions using OpenAI API."""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert pharmaceutical consultant quiz generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            questions = json.loads(content)
            
            # Validate question format
            return self._validate_questions(questions)
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse OpenAI response as JSON: {e}")
            raise Exception("Invalid response format from AI service")
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            raise e
    
    def _generate_with_anthropic(self, prompt: str) -> List[Dict]:
        """Generate questions using Anthropic Claude API."""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text
            
            # Debug: Log the raw response
            logging.info(f"Raw Anthropic response: {content}")
            
            # Clean and extract JSON from response
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            questions = json.loads(content)
            
            # Validate question format
            return self._validate_questions(questions)
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse Anthropic response as JSON: {e}")
            raise Exception("Invalid response format from AI service")
        except Exception as e:
            logging.error(f"Anthropic API error: {e}")
            raise e
    
    def _validate_questions(self, questions: List[Dict]) -> List[Dict]:
        """Validate and clean up generated questions."""
        validated_questions = []
        
        for i, question in enumerate(questions):
            try:
                # Check for essential fields only
                if 'question' not in question or not question['question']:
                    logging.warning(f"Question {i+1} missing question text, skipping")
                    continue
                
                # Set default type if missing
                if 'type' not in question:
                    question['type'] = 'multiple_choice'
                
                # Handle correct_answer field
                if 'correct_answer' not in question:
                    # Try to use first option as default
                    if 'options' in question and question['options']:
                        question['correct_answer'] = question['options'][0]
                    else:
                        logging.warning(f"Question {i+1} missing correct_answer and options, skipping")
                        continue
                
                # Set default values for missing optional fields
                if 'options' not in question:
                    if question['type'] == 'true_false':
                        question['options'] = ['True', 'False']
                    else:
                        question['options'] = ['Option A', 'Option B', 'Option C', 'Option D']
                
                if 'explanation' not in question:
                    question['explanation'] = 'No explanation provided.'
                
                # Validate question type
                if question['type'] not in ['multiple_choice', 'multiple_select', 'true_false']:
                    logging.warning(f"Question {i+1} has invalid type, skipping")
                    continue
                
                # Ensure options is a list
                if not isinstance(question['options'], list):
                    logging.warning(f"Question {i+1} options not a list, skipping")
                    continue
                
                # Add default values for optional fields
                question.setdefault('difficulty', 'intermediate')
                question.setdefault('category', 'Therapy Area Knowledge')
                
                validated_questions.append(question)
                
            except Exception as e:
                logging.warning(f"Error validating question {i+1}: {e}")
                continue
        
        return validated_questions
