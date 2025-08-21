"""
Streamlit input forms for the Pharmaceutical Quiz Module.
Modern web-based input collection and validation.
"""

import streamlit as st
from typing import Dict, Optional
from config.settings import PROJECT_TYPES, CLIENT_SCENARIOS, EXPERIENCE_LEVELS
from ui.styling import create_experience_definitions


def render_input_form() -> Optional[Dict]:
    """
    Render the main input form and return user data if submitted.
    
    Returns:
        Dictionary with user data if form is submitted and valid, None otherwise
    """
    st.header("📋 Project & Client Information")
    st.markdown("Please provide the following information to customize your quiz:")
    
    with st.form("quiz_input_form"):
        # Required Information Section
        st.subheader("Required Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input(
                "Project Name *",
                placeholder="Enter project name",
                help="The name of the current project or study"
            )
            
            therapy_area = st.text_input(
                "Primary Therapy Area *",
                placeholder="e.g., Oncology, Cardiology, Neurology",
                help="The main therapeutic area for this project"
            )
            
            project_type = st.selectbox(
                "Project Type *",
                options=[""] + PROJECT_TYPES,
                help="Select the type of market research project"
            )
        
        with col2:
            client_name = st.text_input(
                "Client Name *",
                placeholder="Enter client/company name",
                help="The pharmaceutical company or client for this project"
            )
            
            indication = st.text_input(
                "Indication *",
                placeholder="e.g., Breast Cancer, Heart Failure",
                help="The specific medical condition or indication"
            )
            
            client_scenario = st.selectbox(
                "Client Scenario *",
                options=[""] + CLIENT_SCENARIOS,
                help="Select the appropriate client engagement scenario"
            )
        
        st.divider()
        
        # Experience Level Assessment
        st.subheader("Experience Level Assessment")
        
        experience_level = st.slider(
            "Self-assessed Experience Level *",
            min_value=1,
            max_value=7,
            value=1,
            help="Rate your experience with this therapy area and project type"
        )
        
        # Show experience definitions
        create_experience_definitions()
        
        st.divider()
        
        # Quiz Configuration
        st.subheader("Quiz Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            question_count = st.number_input(
                "Number of Questions",
                min_value=10,
                max_value=40,
                value=15,
                help="Choose how many questions you'd like in your quiz"
            )
        
        with col2:
            # Time estimation
            estimated_time = calculate_time_estimate(question_count, experience_level)
            st.metric("Estimated Time", f"{estimated_time} minutes")
        
        st.divider()
        
        # Optional Information Section
        st.subheader("Optional Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            additional_therapy = st.text_input(
                "Additional Therapy Area",
                placeholder="Enter if applicable",
                help="Secondary therapy area relevant to the project"
            )
            
            brand_name = st.text_input(
                "Client Brand Name(s)",
                placeholder="e.g., Keytruda, Herceptin",
                help="Brand names of relevant client products"
            )
        
        with col2:
            generic_name = st.text_input(
                "Generic Name(s)",
                placeholder="e.g., pembrolizumab, trastuzumab",
                help="Generic/scientific names of relevant products"
            )
        
        st.divider()
        
        # Document Upload Section
        st.subheader("Background Documents (Optional)")
        st.markdown("Upload relevant documents to enhance question context:")
        
        uploaded_files = st.file_uploader(
            "Select files",
            type=['pdf', 'docx', 'pptx', 'xlsx'],
            accept_multiple_files=True,
            help="Upload PDFs, Word docs, PowerPoint files, or Excel sheets"
        )
        
        if uploaded_files:
            st.success(f"📁 {len(uploaded_files)} file(s) selected:")
            for file in uploaded_files:
                st.write(f"• {file.name} ({file.size / 1024:.1f} KB)")
        
        st.divider()
        
        # Submit button
        submitted = st.form_submit_button(
            "🚀 Generate Quiz",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            # Validate required fields
            validation_errors = validate_form_data(
                project_name, client_name, therapy_area, indication, 
                project_type, client_scenario
            )
            
            if validation_errors:
                for error in validation_errors:
                    st.error(error)
                return None
            
            # Prepare user data
            user_data = {
                'project_name': project_name.strip(),
                'client_name': client_name.strip(),
                'therapy_area': therapy_area.strip(),
                'additional_therapy': additional_therapy.strip(),
                'indication': indication.strip(),
                'brand_name': brand_name.strip(),
                'generic_name': generic_name.strip(),
                'project_type': project_type,
                'client_scenario': client_scenario,
                'experience_level': experience_level,
                'question_count': question_count,
                'uploaded_files': uploaded_files if uploaded_files else []
            }
            
            return user_data
    
    return None


def validate_form_data(project_name: str, client_name: str, therapy_area: str, 
                      indication: str, project_type: str, client_scenario: str) -> list:
    """Validate form data and return list of errors."""
    errors = []
    
    if not project_name.strip():
        errors.append("❌ Project Name is required")
    
    if not client_name.strip():
        errors.append("❌ Client Name is required")
    
    if not therapy_area.strip():
        errors.append("❌ Primary Therapy Area is required")
    
    if not indication.strip():
        errors.append("❌ Indication is required")
    
    if not project_type:
        errors.append("❌ Project Type is required")
    
    if not client_scenario:
        errors.append("❌ Client Scenario is required")
    
    return errors


def calculate_time_estimate(question_count: int, experience_level: int) -> int:
    """Calculate estimated quiz completion time."""
    # Base time per question (in minutes)
    base_time_per_question = {
        1: 2.5,  # Beginners need more time
        2: 2.2,
        3: 2.0,
        4: 1.8,
        5: 1.5,
        6: 1.3,
        7: 1.0   # Experts can answer faster
    }
    
    time_per_question = base_time_per_question.get(experience_level, 2.0)
    total_time = question_count * time_per_question
    
    # Add buffer time for reading instructions and reviewing
    buffer_time = 3
    
    return int(total_time + buffer_time)


def render_quiz_preview(user_data: Dict):
    """Render a preview of the quiz configuration."""
    st.subheader("📊 Quiz Preview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Questions", user_data['question_count'])
    
    with col2:
        estimated_time = calculate_time_estimate(
            user_data['question_count'], 
            user_data['experience_level']
        )
        st.metric("Est. Time", f"{estimated_time} min")
    
    with col3:
        st.metric("Experience Level", f"Level {user_data['experience_level']}")
    
    # Configuration summary
    st.markdown("**Configuration Summary:**")
    st.write(f"• **Project**: {user_data['project_name']}")
    st.write(f"• **Client**: {user_data['client_name']}")
    st.write(f"• **Therapy Area**: {user_data['therapy_area']}")
    st.write(f"• **Project Type**: {user_data['project_type']}")
    
    if user_data.get('uploaded_files'):
        st.write(f"• **Documents**: {len(user_data['uploaded_files'])} file(s) uploaded")
