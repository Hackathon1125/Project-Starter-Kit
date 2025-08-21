"""
Streamlit quiz interface for the Pharmaceutical Quiz Module.
Modern web-based question display and answer collection.
"""

import streamlit as st
from typing import Dict, Any
import time
from streamlit_lottie import st_lottie
import requests
from ui.styling import create_feedback_box


def load_lottie_url(url: str):
    """Load Lottie animation from URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


def render_quiz_interface(quiz_logic):
    """Render the main quiz interface."""
    # Initialize quiz session state
    if 'current_question_answered' not in st.session_state:
        st.session_state.current_question_answered = False
    
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    
    # Get current question
    current_question = quiz_logic.get_current_question()
    if not current_question:
        st.error("No questions available")
        return
    
    # Progress section
    progress = quiz_logic.get_question_progress()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress['percentage'] / 100)
    with col2:
        st.metric("Progress", f"{progress['current']}/{progress['total']}")
    
    st.divider()
    
    # Question display
    st.subheader(f"Question {progress['current']}")
    
    # Question container
    with st.container():
        st.markdown(f"""
        <div class="question-container">
            <h4 style="color: #1f4e79; margin-bottom: 1rem;">
                {current_question['question']}
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Question metadata
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"📂 Category: {current_question.get('category', 'General')}")
        with col2:
            st.caption(f"⚡ Difficulty: {current_question.get('difficulty', 'Intermediate').title()}")
    
    st.divider()
    
    # Answer section
    st.subheader("Select Your Answer")
    
    user_answer = None
    question_type = current_question['type']
    options = current_question['options']
    
    # Render appropriate answer widget
    if question_type == 'multiple_choice':
        user_answer = st.radio(
            "Choose one option:",
            options,
            index=None,
            key=f"question_{progress['current']}_mc"
        )
    
    elif question_type == 'multiple_select':
        st.markdown("**Select all that apply:**")
        selected_options = []
        for option in options:
            if st.checkbox(option, key=f"question_{progress['current']}_ms_{option}"):
                selected_options.append(option)
        user_answer = selected_options if selected_options else None
    
    elif question_type == 'true_false':
        user_answer = st.radio(
            "Choose one:",
            ["True", "False"],
            index=None,
            key=f"question_{progress['current']}_tf"
        )
    
    st.divider()
    
    # Submit answer section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if quiz_logic.can_go_back():
            if st.button("← Previous", key="prev_btn"):
                quiz_logic.go_to_previous_question()
                st.session_state.show_feedback = False
                st.rerun()
    
    with col2:
        # Submit button
        submit_disabled = user_answer is None or st.session_state.current_question_answered
        
        if st.button(
            "Submit Answer", 
            type="primary", 
            disabled=submit_disabled,
            use_container_width=True,
            key="submit_btn"
        ):
            submit_answer(quiz_logic, user_answer)
    
    with col3:
        next_text = "Next →" if quiz_logic.can_go_forward() else "Finish Quiz"
        if st.button(next_text, key="next_btn"):
            handle_next_question(quiz_logic)
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback and 'current_feedback' in st.session_state:
        st.divider()
        display_feedback(st.session_state.current_feedback)


def submit_answer(quiz_logic, user_answer):
    """Submit the user's answer and show feedback."""
    try:
        feedback = quiz_logic.submit_answer(user_answer)
        st.session_state.current_feedback = feedback
        st.session_state.current_question_answered = True
        st.session_state.show_feedback = True
        st.rerun()
        
    except Exception as e:
        st.error(f"Error submitting answer: {str(e)}")


def handle_next_question(quiz_logic):
    """Handle navigation to next question or quiz completion."""
    # Check if current question is answered
    current_result = quiz_logic.question_results[quiz_logic.current_question_index]
    
    if current_result is None:
        if not st.session_state.get('skip_confirmed', False):
            st.warning("⚠️ You haven't answered this question yet.")
            if st.button("Skip Question", key="skip_confirm"):
                st.session_state.skip_confirmed = True
                st.rerun()
            return
    
    # Reset question state
    st.session_state.current_question_answered = False
    st.session_state.show_feedback = False
    st.session_state.skip_confirmed = False
    
    # Navigate to next question or complete quiz
    if quiz_logic.go_to_next_question():
        if quiz_logic.quiz_completed:
            st.session_state.quiz_completed = True
            st.session_state.current_page = 'Results'
        st.rerun()


def display_feedback(feedback: Dict):
    """Display feedback for the submitted answer."""
    is_correct = feedback['is_correct']
    
    # Feedback content
    content_parts = []
    
    if not is_correct:
        content_parts.append(f"**Correct Answer:** {feedback['correct_answer']}")
    
    if feedback.get('explanation'):
        content_parts.append(f"**Explanation:** {feedback['explanation']}")
    
    content = "<br>".join(content_parts)
    
    # Display styled feedback box
    create_feedback_box(is_correct, content)


def render_loading_animation():
    """Render loading animation while generating questions."""
    # Try to load Lottie animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"  # Brain/thinking animation
    lottie_json = load_lottie_url(lottie_url)
    
    if lottie_json:
        st_lottie(lottie_json, height=200, key="loading")
    else:
        # Fallback to simple spinner
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem;">🧠</div>
            <p>Generating personalized quiz questions...</p>
        </div>
        """, unsafe_allow_html=True)


def render_quiz_summary(quiz_logic):
    """Render a summary of the current quiz state."""
    if not quiz_logic:
        return
    
    summary = quiz_logic.get_quiz_summary()
    
    st.sidebar.subheader("📊 Current Quiz")
    st.sidebar.write(f"**Project:** {summary['user_data'].get('project_name', 'N/A')}")
    st.sidebar.write(f"**Therapy Area:** {summary['therapy_area']}")
    st.sidebar.write(f"**Questions:** {summary['question_count']}")
    st.sidebar.write(f"**Experience Level:** {summary['experience_level']}")
    
    if summary['has_documents']:
        st.sidebar.write("📄 **Documents:** Uploaded")
    
    # Progress tracking
    if quiz_logic.quiz_started:
        progress = quiz_logic.get_question_progress()
        answered = sum(1 for result in quiz_logic.question_results if result is not None)
        
        st.sidebar.divider()
        st.sidebar.write(f"**Current Question:** {progress['current']}")
        st.sidebar.write(f"**Answered:** {answered}/{progress['total']}")
        
        # Progress bar
        st.sidebar.progress(progress['percentage'] / 100)
