"""
Configuration settings for the Pharmaceutical Quiz Module.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Quiz Configuration
DEFAULT_QUESTION_COUNT = 15
MIN_QUESTION_COUNT = 10
MAX_QUESTION_COUNT = 40
PASS_THRESHOLD = 0.70  # 70% to pass

# Experience Level Definitions
EXPERIENCE_LEVELS = {
    1: "Completely new to project & therapy area",
    2: "Limited knowledge - familiar with basic therapy area concepts",
    3: "Some knowledge but need development for project specifics",
    4: "Moderate understanding with limited client/project exposure",
    5: "Good working knowledge with some client familiarity",
    6: "Advanced knowledge - subject matter expert level",
    7: "Expert level - internal SME with extensive client/project experience"
}

# Difficulty Distribution by Experience Level
DIFFICULTY_DISTRIBUTION = {
    1: {"fundamental": 80, "intermediate": 15, "advanced": 5},
    2: {"fundamental": 70, "intermediate": 20, "advanced": 10},
    3: {"fundamental": 60, "intermediate": 25, "advanced": 15},
    4: {"fundamental": 50, "intermediate": 30, "advanced": 20},
    5: {"fundamental": 40, "intermediate": 35, "advanced": 25},
    6: {"fundamental": 30, "intermediate": 40, "advanced": 30},
    7: {"fundamental": 20, "intermediate": 50, "advanced": 30}
}

# Project Types
PROJECT_TYPES = [
    "ATU",
    "ATU PCA", 
    "HCP PT",
    "PET",
    "Qual",
    "RT",
    "Digital Tracker",
    "Demand Estimation",
    "Segmentation"
]

# Client Scenarios
CLIENT_SCENARIOS = [
    "Scenario 1: New Client, Baseline Wave (Wave 1)",
    "Scenario 2: Existing Client, Follow-up Wave (Wave 2+)",
    "Scenario 3: Existing Client, New Project Baseline (Wave 1)"
]

# Question Types
QUESTION_TYPES = [
    "multiple_choice",
    "multiple_select",
    "true_false"
]

# File Upload Settings
SUPPORTED_FILE_TYPES = [
    ("PDF files", "*.pdf"),
    ("Word documents", "*.docx"),
    ("PowerPoint files", "*.pptx"),
    ("Excel files", "*.xlsx"),
    ("All supported", "*.pdf;*.docx;*.pptx;*.xlsx")
]

MAX_FILE_SIZE_MB = 50

# UI Configuration
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
PADDING = 20

# Colors (following professional pharmaceutical industry standards)
COLORS = {
    'primary': '#1f4e79',      # Professional blue
    'secondary': '#2e75b6',    # Lighter blue
    'success': '#28a745',      # Green for correct answers
    'error': '#dc3545',        # Red for incorrect answers
    'warning': '#ffc107',      # Yellow for warnings
    'light_gray': '#f8f9fa',   # Light background
    'dark_gray': '#6c757d'     # Text gray
}

# AI Prompt Templates
AI_SYSTEM_PROMPT = """You are an expert pharmaceutical consultant quiz generator. 
Create relevant, accurate questions for pharmaceutical market research consultants 
based on the provided therapy area, client information, and experience level.

Focus on:
- Therapy area knowledge and competitive landscape
- Regulatory and market access considerations
- Client-specific scenarios when applicable
- Industry best practices and methodologies

Ensure questions are:
- Professionally relevant for pharmaceutical consulting
- Appropriate for the specified experience level
- Clear and unambiguous
- Based on current industry standards and practices
"""

# Error Messages
ERROR_MESSAGES = {
    'api_key_missing': "API key not found. Please set your OpenAI or Anthropic API key in the .env file.",
    'api_request_failed': "Failed to generate questions. Please check your internet connection and API key.",
    'file_too_large': f"File size exceeds {MAX_FILE_SIZE_MB}MB limit.",
    'unsupported_file': "Unsupported file type. Please select PDF, Word, PowerPoint, or Excel files.",
    'invalid_input': "Please fill in all required fields.",
    'no_questions': "No questions were generated. Please try again with different parameters."
}
