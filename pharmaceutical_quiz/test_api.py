import anthropic
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test API connection
api_key = os.getenv('ANTHROPIC_API_KEY')
print(f"API Key loaded: {api_key[:20]}...")

client = anthropic.Anthropic(api_key=api_key)

# Test simple question generation
prompt = """Generate exactly 1 quiz question about diabetes in JSON format. 
Return ONLY a JSON array with this exact structure:
[{
    "question": "What is the primary characteristic of Type 1 diabetes?",
    "type": "multiple_choice", 
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Brief explanation here",
    "category": "Endocrinology",
    "difficulty": "fundamental"
}]

Return ONLY the JSON array, no other text."""

try:
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.content[0].text
    print("Raw response:")
    print(content)
    print("\n" + "="*50 + "\n")
    
    # Try to parse JSON
    questions = json.loads(content)
    print("Parsed successfully:")
    print(json.dumps(questions, indent=2))
    
except Exception as e:
    print(f"Error: {e}")
