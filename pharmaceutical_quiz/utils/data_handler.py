"""
Data handling utilities for the Pharmaceutical Quiz Module.
Manages session data and temporary storage.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional


class DataHandler:
    """Handles session-based data storage and management."""
    
    def __init__(self):
        self.session_data = {}
        self.temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
        self.ensure_temp_directory()
    
    def ensure_temp_directory(self):
        """Ensure temporary directory exists."""
        try:
            if not os.path.exists(self.temp_dir):
                os.makedirs(self.temp_dir)
        except Exception as e:
            logging.warning(f"Could not create temp directory: {e}")
            self.temp_dir = None
    
    def store_session_data(self, key: str, data: Any):
        """Store data in the current session."""
        self.session_data[key] = data
        logging.debug(f"Stored session data for key: {key}")
    
    def get_session_data(self, key: str, default: Any = None) -> Any:
        """Retrieve data from the current session."""
        return self.session_data.get(key, default)
    
    def clear_session_data(self):
        """Clear all session data."""
        self.session_data.clear()
        logging.info("Session data cleared")
    
    def save_quiz_results(self, results: Dict) -> Optional[str]:
        """
        Save quiz results to a temporary file.
        
        Args:
            results: Quiz results dictionary
            
        Returns:
            File path if saved successfully, None otherwise
        """
        if not self.temp_dir:
            logging.warning("No temp directory available for saving results")
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"quiz_results_{timestamp}.json"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Prepare results for JSON serialization
            serializable_results = self._make_serializable(results)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Quiz results saved to: {filepath}")
            return filepath
            
        except Exception as e:
            logging.error(f"Failed to save quiz results: {e}")
            return None
    
    def load_quiz_results(self, filepath: str) -> Optional[Dict]:
        """
        Load quiz results from a file.
        
        Args:
            filepath: Path to the results file
            
        Returns:
            Results dictionary if loaded successfully, None otherwise
        """
        try:
            if not os.path.exists(filepath):
                logging.warning(f"Results file not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            logging.info(f"Quiz results loaded from: {filepath}")
            return results
            
        except Exception as e:
            logging.error(f"Failed to load quiz results: {e}")
            return None
    
    def _make_serializable(self, obj: Any) -> Any:
        """Convert objects to JSON-serializable format."""
        if isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return self._make_serializable(obj.__dict__)
        else:
            try:
                json.dumps(obj)
                return obj
            except (TypeError, ValueError):
                return str(obj)
    
    def get_timestamp(self) -> str:
        """Get current timestamp as ISO string."""
        return datetime.now().isoformat()
    
    def cleanup_temp_files(self, max_age_days: int = 7):
        """
        Clean up old temporary files.
        
        Args:
            max_age_days: Maximum age of files to keep in days
        """
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            return
        
        try:
            current_time = datetime.now()
            max_age_seconds = max_age_days * 24 * 3600
            
            for filename in os.listdir(self.temp_dir):
                filepath = os.path.join(self.temp_dir, filename)
                
                if os.path.isfile(filepath):
                    file_age = current_time.timestamp() - os.path.getmtime(filepath)
                    
                    if file_age > max_age_seconds:
                        os.remove(filepath)
                        logging.info(f"Cleaned up old temp file: {filename}")
                        
        except Exception as e:
            logging.warning(f"Error during temp file cleanup: {e}")
    
    def export_results_summary(self, results: Dict) -> Dict:
        """
        Create a summary of results for export.
        
        Args:
            results: Full quiz results
            
        Returns:
            Simplified results summary
        """
        summary = {
            'quiz_info': {
                'project_name': results.get('user_data', {}).get('project_name', ''),
                'client_name': results.get('user_data', {}).get('client_name', ''),
                'therapy_area': results.get('user_data', {}).get('therapy_area', ''),
                'completion_time': results.get('completion_time', ''),
                'experience_level': results.get('user_data', {}).get('experience_level', 1)
            },
            'performance': {
                'total_questions': results.get('total_questions', 0),
                'correct_answers': results.get('correct_answers', 0),
                'score_percentage': results.get('score_percentage', 0),
                'grade': results.get('grade', 'N/A'),
                'passed': results.get('passed', False)
            },
            'breakdown': {
                'categories': results.get('category_breakdown', {}),
                'difficulties': results.get('difficulty_breakdown', {})
            },
            'recommendations': results.get('recommendations', [])
        }
        
        return summary
