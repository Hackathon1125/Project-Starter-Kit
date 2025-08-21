# Pharmaceutical Therapy Area Knowledge Quiz Module

A comprehensive Python-based quiz application designed for pharmaceutical consulting companies to assess consultant knowledge before project onboarding. This tool generates AI-powered questions tailored to specific therapy areas, client scenarios, and experience levels.

## Features

### Phase 1 (MVP) - Completed
- ✅ **Comprehensive Input Form**: Collects project details, client information, therapy areas, and experience levels
- ✅ **AI-Powered Question Generation**: Uses OpenAI GPT-4 or Anthropic Claude to create relevant questions
- ✅ **Experience-Based Difficulty**: Adjusts question difficulty based on self-assessed experience (1-7 scale)
- ✅ **Multiple Question Types**: Multiple choice, multiple select, and true/false questions
- ✅ **Interactive Quiz Interface**: Professional Tkinter-based UI with progress tracking
- ✅ **Immediate Feedback**: Shows correct answers and detailed explanations after each question
- ✅ **Document Upload Support**: Processes PDF, Word, PowerPoint, and Excel files for context
- ✅ **Comprehensive Results**: Detailed performance analytics with category and difficulty breakdowns
- ✅ **Professional Styling**: Clean, pharmaceutical industry-appropriate interface

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**:
   ```bash
   cd C:\Users\SebastianCwalina\CascadeProjects\pharmaceutical_quiz
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key or Anthropic API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   # OR
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```
   - You need at least one API key for question generation

4. **Run the application**:
   ```bash
   python main.py
   ```

## Usage Guide

### Starting a Quiz

1. **Launch the application** by running `python main.py`

2. **Fill in the required information**:
   - Project Name
   - Client Name
   - Primary Therapy Area
   - Indication
   - Project Type (from dropdown)
   - Client Scenario (from dropdown)

3. **Set your experience level** (1-7 scale):
   - Level 1: Completely new to project & therapy area
   - Level 7: Expert level - internal SME with extensive experience

4. **Optional enhancements**:
   - Add additional therapy area
   - Include client product information (brand/generic names)
   - Upload background documents (PDF, Word, PowerPoint, Excel)

5. **Start the quiz** - The system will generate 15 questions tailored to your inputs

### Taking the Quiz

- **Answer questions** using radio buttons, checkboxes, or true/false options
- **Submit each answer** to receive immediate feedback
- **Navigate** between questions using Previous/Next buttons
- **View explanations** for correct and incorrect answers
- **Track progress** with the built-in progress bar

### Viewing Results

- **Overall performance**: Score percentage, letter grade, pass/fail status
- **Category breakdown**: Performance by knowledge area
- **Difficulty analysis**: Performance by question difficulty level
- **Personalized recommendations**: Specific areas for improvement
- **Detailed question review**: Question-by-question analysis
- **Save results**: Export results to JSON file

## Question Generation

The system uses advanced AI to generate relevant questions based on:

- **Therapy Area**: Specific medical/therapeutic domain
- **Experience Level**: Difficulty distribution (fundamental/intermediate/advanced)
- **Project Type**: Methodology-specific questions
- **Client Context**: Scenario-based questions
- **Document Context**: Questions derived from uploaded materials

### Difficulty Distribution by Experience Level

| Level | Fundamental | Intermediate | Advanced |
|-------|-------------|--------------|----------|
| 1     | 80%         | 15%          | 5%       |
| 2     | 70%         | 20%          | 10%      |
| 3     | 60%         | 25%          | 15%      |
| 4     | 50%         | 30%          | 20%      |
| 5     | 40%         | 35%          | 25%      |
| 6     | 30%         | 40%          | 30%      |
| 7     | 20%         | 50%          | 30%      |

## Supported File Types

- **PDF**: Clinical documents, proposals, research papers
- **Word (.docx)**: Meeting notes, client resources, protocols
- **PowerPoint (.pptx)**: Presentations, kick-off decks, deliverables
- **Excel (.xlsx)**: Data summaries, market research, analytics

## Project Structure

```
pharmaceutical_quiz/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment configuration template
├── README.md                 # This file
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration settings
├── ui/
│   ├── __init__.py
│   ├── input_forms.py        # Input form interface
│   ├── quiz_interface.py     # Quiz display and navigation
│   └── results_display.py    # Results and analytics display
├── quiz_engine/
│   ├── __init__.py
│   └── quiz_logic.py         # Core quiz logic and scoring
└── utils/
    ├── __init__.py
    ├── ai_integration.py     # AI API connections
    ├── document_processor.py # File parsing utilities
    └── data_handler.py       # Session and data management
```

## Configuration

### API Settings
- Supports both OpenAI and Anthropic APIs
- Automatic fallback between providers
- Configurable question count (default: 15)
- Adjustable pass threshold (default: 70%)

### UI Customization
- Professional pharmaceutical industry color scheme
- Responsive layout with scrollable content
- Progress tracking and navigation
- Consistent styling across all components

## Troubleshooting

### Common Issues

1. **"API key not found" error**:
   - Ensure you've created a `.env` file from `.env.example`
   - Add a valid OpenAI or Anthropic API key
   - Restart the application

2. **"Failed to generate questions" error**:
   - Check your internet connection
   - Verify API key is valid and has sufficient credits
   - Try with different input parameters

3. **Document processing errors**:
   - Ensure files are not corrupted
   - Check file size (max 50MB per file)
   - Verify file format is supported

4. **UI display issues**:
   - Ensure all required packages are installed
   - Try running with administrator privileges
   - Check Python version compatibility

### Getting Help

For technical issues or questions:
1. Check the console output for detailed error messages
2. Verify all dependencies are properly installed
3. Ensure API keys are correctly configured
4. Review the troubleshooting section above

## Future Enhancements (Planned)

### Phase 2
- Advanced question types (scenario-based, ranking, fill-in-blank)
- Enhanced document processing with key information extraction
- Configurable question count and time estimation
- Improved results dashboard with trend analysis

### Phase 3
- Context-aware question generation from documents
- Dynamic difficulty adjustment during quiz
- Learning resources integration
- Performance tracking across multiple attempts

### Phase 4
- User authentication and progress history
- PDF report generation
- Administrative content management
- API endpoints for external integration

## Technical Requirements

- **Python**: 3.8+
- **GUI Framework**: Tkinter (included with Python)
- **AI APIs**: OpenAI GPT-4 or Anthropic Claude
- **Document Processing**: PyPDF2, python-docx, python-pptx, pandas
- **Operating System**: Windows, macOS, Linux

## License

This project is designed for internal use by pharmaceutical consulting companies. Please ensure compliance with your organization's software usage policies and API terms of service.

## Support

This application is designed to integrate with existing pharmaceutical consulting workflows and can be customized for specific organizational needs.
