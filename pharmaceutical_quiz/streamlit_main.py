"""
Pharmaceutical Therapy Area Knowledge Quiz Module - Streamlit Version
Main entry point for the modern web-based quiz application.
"""

import streamlit as st
import sys
import os
# Removed streamlit_option_menu dependency - using native Streamlit components
import time

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.input_forms_streamlit import render_input_form
from ui.quiz_interface_streamlit import render_quiz_interface
from ui.results_display_streamlit import render_results_display
from ui.styling import apply_custom_css
from quiz_engine.quiz_logic import QuizLogic
from utils.data_handler import DataHandler


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Input'
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    if 'quiz_logic' not in st.session_state:
        st.session_state.quiz_logic = None
    
    if 'data_handler' not in st.session_state:
        st.session_state.data_handler = DataHandler()
    
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False


def main():
    """Main application function."""
    # Configure page
    st.set_page_config(
        page_title="Pharmaceutical Therapy Area Knowledge Quiz",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom styling
    apply_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.title("💊 Pharmaceutical Therapy Area Knowledge Quiz")
    st.markdown("*Assess consultant knowledge before project onboarding*")
    st.divider()
    
    # Render sidebar
    render_sidebar()
    
    # Determine default index based on current page
    page_to_index = {"Input": 0, "Quiz": 1, "Results": 2}
    current_index = page_to_index.get(st.session_state.current_page, 0)
    
    # Main navigation using native Streamlit tabs
    tab1, tab2, tab3 = st.tabs(["📝 Input", "❓ Quiz", "📊 Results"])
    
    # Determine which tab to show based on session state
    if st.session_state.current_page == "Input":
        selected = "Input"
        with tab1:
            render_input_page()
    elif st.session_state.current_page == "Quiz":
        selected = "Quiz"
        with tab2:
            render_quiz_page()
    elif st.session_state.current_page == "Results":
        selected = "Results"
        with tab3:
            render_results_page()
    else:
        selected = "Input"
        with tab1:
            render_input_page()
    
    # Handle tab switching
    if 'last_tab_state' not in st.session_state:
        st.session_state.last_tab_state = selected
    
    # Tab content is already rendered above in the with statements


def render_input_page():
    """Render the input form page."""
    if st.session_state.quiz_started:
        st.warning("⚠️ Quiz is already in progress. Use the Quiz tab to continue or restart below.")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("Continue Quiz", type="primary"):
                st.session_state.current_page = 'Quiz'
                st.rerun()
        with col2:
            if st.button("Restart Quiz", type="secondary"):
                reset_quiz()
                st.rerun()
        st.divider()
    
    # Render input form
    user_data = render_input_form()
    
    if user_data:
        # Store user data and start quiz
        st.session_state.user_data = user_data
        start_quiz()


def render_quiz_page():
    """Render the quiz interface page."""
    if not st.session_state.quiz_started:
        st.error("❌ No quiz in progress. Please complete the input form first.")
        if st.button("Go to Input Form", type="primary"):
            st.session_state.current_page = 'Input'
            st.rerun()
        return
    
    if st.session_state.quiz_completed:
        st.success("🎉 Quiz completed! View your results in the Results tab.")
        if st.button("View Results", type="primary"):
            st.session_state.current_page = 'Results'
            st.rerun()
        return
    
    # Render quiz interface
    render_quiz_interface(st.session_state.quiz_logic)


def render_results_page():
    """Render the results display page."""
    if not st.session_state.quiz_completed:
        st.error("❌ No quiz results available. Please complete a quiz first.")
        if st.button("Go to Input Form", type="primary"):
            st.session_state.current_page = 'Input'
            st.rerun()
        return
    
    # Render results display
    render_results_display(st.session_state.quiz_logic)


def start_quiz():
    """Initialize and start the quiz."""
    try:
        with st.spinner("🧠 Generating personalized quiz questions..."):
            # Initialize quiz logic
            st.session_state.quiz_logic = QuizLogic(
                st.session_state.user_data, 
                st.session_state.data_handler
            )
            
            # Generate questions
            question_count = st.session_state.user_data.get('question_count', 15)
            success = st.session_state.quiz_logic.generate_questions(question_count)
            
            if success:
                # Start the quiz after successful generation
                st.session_state.quiz_logic.start_quiz()
                st.session_state.quiz_started = True
                st.session_state.quiz_completed = False
                st.success("✅ Quiz questions generated successfully!")
                time.sleep(1)
                st.session_state.current_page = 'Quiz'
                st.rerun()
            else:
                st.error("❌ Failed to generate quiz questions. Please check your configuration and try again.")
                
    except Exception as e:
        st.error(f"❌ Error starting quiz: {str(e)}")


def reset_quiz():
    """Reset the quiz to initial state."""
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False
    st.session_state.quiz_logic = None
    st.session_state.user_data = {}
    st.session_state.current_page = 'Input'


# Sidebar information
def render_sidebar():
    """Render sidebar with helpful information."""
    with st.sidebar:
        st.header("📋 Quiz Information")
        
        if st.session_state.get('quiz_started', False) and st.session_state.get('quiz_logic'):
            progress = st.session_state.quiz_logic.get_question_progress()
            st.metric("Progress", f"{progress['current']}/{progress['total']}")
            st.progress(progress['percentage'] / 100)
        
        st.divider()
        
        st.subheader("🎯 Experience Levels")
        st.markdown("""
        **1**: Completely new to project & therapy area  
        **2**: Limited knowledge - basic concepts  
        **3**: Some knowledge, need development  
        **4**: Moderate understanding  
        **5**: Good working knowledge  
        **6**: Advanced knowledge - SME level  
        **7**: Expert level - internal SME  
        """)
        
        st.divider()
        
        if st.button("🔄 Reset Application", type="secondary"):
            reset_quiz()
            st.rerun()


if __name__ == "__main__":
    # Run main application
    main()
