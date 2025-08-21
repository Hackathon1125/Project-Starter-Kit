"""
Pharmaceutical Therapy Area Knowledge Quiz - Streamlit App Entry Point
This is the main entry point for Streamlit Cloud deployment.
"""

import sys
import os

# Add the pharmaceutical_quiz directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
pharmaceutical_quiz_dir = os.path.join(current_dir, 'pharmaceutical_quiz')
sys.path.insert(0, pharmaceutical_quiz_dir)

# Import and run the main Streamlit app
from streamlit_main import main

if __name__ == "__main__":
    main()
