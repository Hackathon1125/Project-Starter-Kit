"""
Custom styling for the Pharmaceutical Quiz Module Streamlit interface.
Provides professional pharmaceutical industry-appropriate styling.
"""

import streamlit as st


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
    <style>
    /* Main app styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2e75b6 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Question container styling */
    .question-container {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Feedback styling */
    .feedback-correct {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        color: #155724;
        margin: 1rem 0;
    }
    
    .feedback-incorrect {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 1rem;
        color: #721c24;
        margin: 1rem 0;
    }
    
    /* Results styling */
    .results-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .score-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    
    .score-passed {
        color: #28a745;
    }
    
    .score-failed {
        color: #dc3545;
    }
    
    /* Card styling */
    .metric-card {
        background-color: white;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1f4e79 0%, #2e75b6 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #1f4e79;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        background-color: #f8f9fa;
    }
    
    /* Experience level definitions */
    .experience-definitions {
        background-color: #e3f2fd;
        border-left: 4px solid #1f4e79;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    /* Navigation menu custom styling */
    .nav-link-selected {
        background-color: #1f4e79 !important;
        color: white !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            padding: 0.5rem;
        }
        
        .question-container {
            padding: 1rem;
        }
        
        .score-display {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def create_header(title: str, subtitle: str = ""):
    """Create a styled header section."""
    header_html = f"""
    <div class="main-header fade-in">
        <h1>{title}</h1>
        {f'<p style="margin: 0; opacity: 0.9;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def create_metric_card(title: str, value: str, delta: str = None):
    """Create a styled metric card."""
    delta_html = f'<p style="color: #6c757d; margin: 0; font-size: 0.9rem;">{delta}</p>' if delta else ''
    
    card_html = f"""
    <div class="metric-card fade-in">
        <h3 style="margin: 0; color: #1f4e79;">{title}</h3>
        <h2 style="margin: 0.5rem 0; color: #2e75b6;">{value}</h2>
        {delta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def create_feedback_box(is_correct: bool, content: str):
    """Create a styled feedback box."""
    css_class = "feedback-correct" if is_correct else "feedback-incorrect"
    icon = "✅" if is_correct else "❌"
    
    feedback_html = f"""
    <div class="{css_class} fade-in">
        <h4 style="margin: 0 0 0.5rem 0;">{icon} {'Correct!' if is_correct else 'Incorrect'}</h4>
        <div>{content}</div>
    </div>
    """
    st.markdown(feedback_html, unsafe_allow_html=True)


def create_experience_definitions():
    """Create styled experience level definitions."""
    definitions_html = """
    <div class="experience-definitions fade-in">
        <h4 style="color: #1f4e79; margin-bottom: 1rem;">Experience Level Definitions:</h4>
        <ul style="margin: 0; padding-left: 1.5rem;">
            <li><strong>Level 1:</strong> Completely new to project & therapy area</li>
            <li><strong>Level 2:</strong> Limited knowledge - familiar with basic therapy area concepts</li>
            <li><strong>Level 3:</strong> Some knowledge but need development for project specifics</li>
            <li><strong>Level 4:</strong> Moderate understanding with limited client/project exposure</li>
            <li><strong>Level 5:</strong> Good working knowledge with some client familiarity</li>
            <li><strong>Level 6:</strong> Advanced knowledge - subject matter expert level</li>
            <li><strong>Level 7:</strong> Expert level - internal SME with extensive client/project experience</li>
        </ul>
    </div>
    """
    st.markdown(definitions_html, unsafe_allow_html=True)
