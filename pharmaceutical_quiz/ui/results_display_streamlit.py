"""
Streamlit results display for the Pharmaceutical Quiz Module.
Interactive analytics and comprehensive performance reporting.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict
from ui.styling import create_metric_card
from utils.pdf_generator import PDFReportGenerator


def render_results_display(quiz_logic):
    """Render comprehensive quiz results with interactive analytics."""
    results = quiz_logic.get_results()
    
    # Header section
    st.header("📊 Quiz Results")
    
    # Overall performance section
    render_performance_overview(results)
    
    # Interactive charts section
    render_analytics_charts(results)
    
    # Detailed breakdown section
    render_detailed_breakdown(results)
    
    # Recommendations section
    render_recommendations(results)
    
    # Action buttons section
    render_action_buttons(results, quiz_logic)


def render_performance_overview(results: Dict):
    """Render the overall performance overview."""
    score = results['score_percentage']
    passed = results['passed']
    grade = results['grade']
    
    # Score display with styling
    score_color = "#28a745" if passed else "#dc3545"
    status_text = "PASSED" if passed else "NEEDS IMPROVEMENT"
    
    st.markdown(f"""
    <div class="results-header fade-in">
        <div class="score-display" style="color: white;">
            {score}%
        </div>
        <h2 style="margin: 0; color: white;">Grade: {grade}</h2>
        <h3 style="margin: 0.5rem 0 0 0; color: white;">{status_text}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Questions Answered",
            f"{results['answered_questions']}/{results['total_questions']}",
            delta=f"{results['answered_questions']} completed"
        )
    
    with col2:
        st.metric(
            "Correct Answers",
            results['correct_answers'],
            delta=f"{score:.1f}% accuracy"
        )
    
    with col3:
        experience_level = results['user_data'].get('experience_level', 1)
        st.metric(
            "Experience Level",
            f"Level {experience_level}",
            delta="Self-assessed"
        )
    
    with col4:
        pass_status = "✅ Passed" if passed else "❌ Failed"
        st.metric(
            "Status",
            pass_status,
            delta="70% required"
        )


def render_analytics_charts(results: Dict):
    """Render interactive analytics charts using Plotly."""
    st.subheader("📈 Performance Analytics")
    
    # Create tabs for different chart views
    tab1, tab2, tab3 = st.tabs(["Category Breakdown", "Difficulty Analysis", "Question Details"])
    
    with tab1:
        render_category_chart(results)
    
    with tab2:
        render_difficulty_chart(results)
    
    with tab3:
        render_question_details_chart(results)


def render_category_chart(results: Dict):
    """Render category performance chart."""
    category_data = results.get('category_breakdown', {})
    
    if not category_data:
        st.info("No category data available")
        return
    
    # Prepare data for chart
    categories = list(category_data.keys())
    percentages = [data['percentage'] for data in category_data.values()]
    correct_counts = [data['correct'] for data in category_data.values()]
    total_counts = [data['total'] for data in category_data.values()]
    
    # Create bar chart
    fig = px.bar(
        x=categories,
        y=percentages,
        title="Performance by Knowledge Category",
        labels={'x': 'Knowledge Category', 'y': 'Score Percentage'},
        color=percentages,
        color_continuous_scale='RdYlGn',
        text=[f"{correct}/{total}" for correct, total in zip(correct_counts, total_counts)]
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        showlegend=False,
        height=400,
        coloraxis_colorbar_title="Score %"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_difficulty_chart(results: Dict):
    """Render difficulty performance chart."""
    difficulty_data = results.get('difficulty_breakdown', {})
    
    if not difficulty_data:
        st.info("No difficulty data available")
        return
    
    # Prepare data for donut chart
    difficulties = list(difficulty_data.keys())
    percentages = [data['percentage'] for data in difficulty_data.values()]
    
    # Create donut chart
    fig = go.Figure(data=[go.Pie(
        labels=difficulties,
        values=percentages,
        hole=0.4,
        textinfo='label+percent',
        textposition='outside',
        marker_colors=['#ff9999', '#66b3ff', '#99ff99']
    )])
    
    fig.update_layout(
        title="Performance by Question Difficulty",
        height=400,
        annotations=[dict(text='Difficulty<br>Breakdown', x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_question_details_chart(results: Dict):
    """Render detailed question-by-question performance."""
    question_results = results.get('question_results', [])
    
    if not question_results:
        st.info("No question details available")
        return
    
    # Prepare data
    question_numbers = []
    correctness = []
    categories = []
    difficulties = []
    
    for i, result in enumerate(question_results, 1):
        if result:
            question_numbers.append(f"Q{i}")
            correctness.append(1 if result['is_correct'] else 0)
            categories.append(result['question'].get('category', 'General'))
            difficulties.append(result['question'].get('difficulty', 'intermediate'))
    
    # Create scatter plot
    fig = px.scatter(
        x=question_numbers,
        y=correctness,
        color=categories,
        symbol=difficulties,
        title="Question-by-Question Performance",
        labels={'x': 'Question Number', 'y': 'Correct (1) / Incorrect (0)'},
        height=400
    )
    
    fig.update_traces(marker_size=12)
    fig.update_layout(yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Incorrect', 'Correct']))
    
    st.plotly_chart(fig, use_container_width=True)


def render_detailed_breakdown(results: Dict):
    """Render detailed performance breakdown."""
    st.subheader("📋 Detailed Analysis")
    
    # Expandable sections for detailed review
    with st.expander("📊 Category Performance Details", expanded=False):
        category_data = results.get('category_breakdown', {})
        for category, stats in category_data.items():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**{category}**")
                progress_value = stats['percentage'] / 100
                st.progress(progress_value)
            with col2:
                st.metric("Score", f"{stats['percentage']:.1f}%", f"{stats['correct']}/{stats['total']}")
    
    with st.expander("⚡ Difficulty Analysis", expanded=False):
        difficulty_data = results.get('difficulty_breakdown', {})
        for difficulty, stats in difficulty_data.items():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**{difficulty.title()} Questions**")
                progress_value = stats['percentage'] / 100
                st.progress(progress_value)
            with col2:
                st.metric("Score", f"{stats['percentage']:.1f}%", f"{stats['correct']}/{stats['total']}")
    
    with st.expander("🔍 Question-by-Question Review", expanded=False):
        render_question_review(results)


def render_question_review(results: Dict):
    """Render detailed question-by-question review."""
    question_results = results.get('question_results', [])
    
    for i, result in enumerate(question_results, 1):
        if result is None:
            st.write(f"**Question {i}:** Not answered")
            continue
        
        question = result['question']
        is_correct = result['is_correct']
        user_answer = result['user_answer']
        correct_answer = result['correct_answer']
        
        # Question header with status
        status_icon = "✅" if is_correct else "❌"
        status_color = "#28a745" if is_correct else "#dc3545"
        
        st.markdown(f"""
        <div style="border-left: 4px solid {status_color}; padding-left: 1rem; margin: 1rem 0;">
            <h5 style="color: {status_color}; margin: 0;">
                {status_icon} Question {i} - {question.get('category', 'General')}
            </h5>
        </div>
        """, unsafe_allow_html=True)
        
        # Question details
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Q:** {question['question']}")
            st.write(f"**Your Answer:** {user_answer}")
            st.write(f"**Correct Answer:** {correct_answer}")
        
        with col2:
            st.caption(f"Difficulty: {question.get('difficulty', 'N/A').title()}")
        
        # Explanation
        if question.get('explanation'):
            with st.expander("View Explanation"):
                st.write(question['explanation'])
        
        st.divider()


def render_recommendations(results: Dict):
    """Render personalized recommendations."""
    recommendations = results.get('recommendations', [])
    
    if not recommendations:
        return
    
    st.subheader("💡 Personalized Recommendations")
    
    for i, recommendation in enumerate(recommendations, 1):
        st.markdown(f"""
        <div class="metric-card">
            <h5 style="color: #1f4e79; margin: 0 0 0.5rem 0;">
                {i}. Recommendation
            </h5>
            <p style="margin: 0;">{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)


def render_action_buttons(results: Dict, quiz_logic):
    """Render action buttons for results page."""
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Retake Quiz", type="secondary", use_container_width=True):
            if st.session_state.get('retake_confirmed', False):
                reset_quiz_state()
                st.rerun()
            else:
                st.session_state.retake_confirmed = True
                st.warning("Click again to confirm retaking the quiz")
    
    with col2:
        if st.button("📄 Generate PDF Report", type="primary", use_container_width=True):
            generate_pdf_report(results)
    
    with col3:
        if st.button("📊 Export Data", type="secondary", use_container_width=True):
            export_results_data(results)
    
    with col4:
        if st.button("🏠 New Quiz", type="secondary", use_container_width=True):
            reset_quiz_state()
            st.rerun()


def generate_pdf_report(results: Dict):
    """Generate and download PDF report."""
    try:
        with st.spinner("📄 Generating PDF report..."):
            pdf_generator = PDFReportGenerator()
            pdf_data = pdf_generator.generate_report(results)
            
            if pdf_data:
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_data,
                    file_name=f"quiz_results_{results['user_data']['project_name'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    type="primary"
                )
                st.success("✅ PDF report generated successfully!")
            else:
                st.error("❌ Failed to generate PDF report")
                
    except Exception as e:
        st.error(f"❌ Error generating PDF: {str(e)}")


def export_results_data(results: Dict):
    """Export results data as JSON."""
    try:
        import json
        
        # Prepare data for export
        export_data = {
            'quiz_summary': {
                'project_name': results['user_data']['project_name'],
                'client_name': results['user_data']['client_name'],
                'therapy_area': results['user_data']['therapy_area'],
                'score_percentage': results['score_percentage'],
                'grade': results['grade'],
                'passed': results['passed'],
                'completion_time': results['completion_time']
            },
            'performance_breakdown': {
                'categories': results.get('category_breakdown', {}),
                'difficulties': results.get('difficulty_breakdown', {})
            },
            'recommendations': results.get('recommendations', [])
        }
        
        json_data = json.dumps(export_data, indent=2)
        
        st.download_button(
            label="⬇️ Download JSON Data",
            data=json_data,
            file_name=f"quiz_data_{results['user_data']['project_name'].replace(' ', '_')}.json",
            mime="application/json",
            type="secondary"
        )
        
    except Exception as e:
        st.error(f"❌ Error exporting data: {str(e)}")


def reset_quiz_state():
    """Reset all quiz-related session state."""
    keys_to_reset = [
        'quiz_started', 'quiz_completed', 'quiz_logic', 'user_data',
        'current_question_answered', 'show_feedback', 'current_feedback',
        'retake_confirmed', 'skip_confirmed'
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state.current_page = 'Input'


def create_performance_radar_chart(results: Dict):
    """Create a radar chart for competency areas."""
    category_data = results.get('category_breakdown', {})
    
    if len(category_data) < 3:
        return None
    
    categories = list(category_data.keys())
    scores = [data['percentage'] for data in category_data.values()]
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Performance',
        line_color='#1f4e79'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Competency Radar Chart",
        height=400
    )
    
    return fig


def render_competency_radar(results: Dict):
    """Render competency radar chart if applicable."""
    radar_chart = create_performance_radar_chart(results)
    
    if radar_chart:
        st.subheader("🎯 Competency Overview")
        st.plotly_chart(radar_chart, use_container_width=True)
    else:
        st.info("Radar chart requires at least 3 performance categories")
