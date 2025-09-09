import re
import time
import random
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

def generate_feedback(accuracy: float, profile: Dict[str, float], 
                     student_info: Dict[str, Any]) -> str:
    """Generate personalized feedback based on performance"""
    
    feedback_templates = {
        'excellent': [
            "🌟 Outstanding work, {name}! You're mastering the material with {accuracy:.1%} accuracy. Keep challenging yourself!",
            "🎯 Excellent performance! Your {accuracy:.1%} accuracy shows strong understanding. Ready for more advanced topics?",
            "🔥 You're on fire! {accuracy:.1%} accuracy is impressive. Consider exploring enrichment materials."
        ],
        'good': [
            "👍 Good job, {name}! You achieved {accuracy:.1%} accuracy. Focus on the areas you missed to improve further.",
            "📈 Nice progress! {accuracy:.1%} shows you're learning well. Practice similar problems to strengthen your skills.",
            "💪 Well done! Your {accuracy:.1%} accuracy is solid. A bit more practice will make you even stronger."
        ],
        'needs_improvement': [
            "🤔 You scored {accuracy:.1%}, {name}. Don't worry - learning takes time! Focus on understanding the basics first.",
            "📚 {accuracy:.1%} shows you're working hard. Try reviewing the fundamentals and practicing step-by-step solutions.",
            "🌱 Everyone learns at their own pace. Your {accuracy:.1%} is a starting point. Break down complex problems into smaller steps."
        ],
        'struggling': [
            "💡 {accuracy:.1%} accuracy tells us you need more support, {name}. Consider asking for help with the basics.",
            "🤝 Learning can be challenging! Your {accuracy:.1%} suggests reviewing foundational concepts would help.",
            "🎯 Don't give up! {accuracy:.1%} means we need to find the right approach for you. Try different learning strategies."
        ]
    }
    
    # Determine performance category
    if accuracy >= 0.85:
        category = 'excellent'
    elif accuracy >= 0.7:
        category = 'good'
    elif accuracy >= 0.5:
        category = 'needs_improvement'
    else:
        category = 'struggling'
    
    # Select random template from category
    template = random.choice(feedback_templates[category])
    
    # Format with student information
    feedback = template.format(
        name=student_info.get('name', 'Student'),
        accuracy=accuracy
    )
    
    # Add specific recommendations based on profile
    engagement = profile.get('engagement', 0)
    pace = profile.get('pace', 0)
    
    additional_tips = []
    
    if engagement < 0.7:
        additional_tips.append("💭 Try not to skip questions - even a guess can help your learning!")
    
    if pace > 30:
        additional_tips.append("⏰ Take your time to read questions carefully, but don't overthink simple problems.")
    elif pace < 10:
        additional_tips.append("🚀 You're working quickly! Make sure to double-check your answers.")
    
    # Add learning style recommendations
    preferred_format = student_info.get('preferred_format', 'text')
    if preferred_format == 'video':
        additional_tips.append("🎥 Since you prefer videos, try Khan Academy or educational YouTube channels!")
    elif preferred_format == 'text':
        additional_tips.append("📖 You learn well from text - try worked examples and step-by-step guides!")
    
    if additional_tips:
        feedback += "\n\n" + " ".join(additional_tips)
    
    return feedback

def simulate_response_time(difficulty: int, base_time: float = 20.0) -> float:
    """Simulate realistic response time based on question difficulty"""
    
    # Base time increases with difficulty
    difficulty_multiplier = {1: 0.8, 2: 1.0, 3: 1.5, 4: 2.0, 5: 2.5}
    multiplier = difficulty_multiplier.get(difficulty, 1.0)
    
    # Add some randomness
    variation = random.uniform(0.7, 1.3)
    
    # Calculate simulated time
    simulated_time = base_time * multiplier * variation
    
    # Add occasional "thinking pauses"
    if random.random() < 0.2:  # 20% chance of longer thinking time
        simulated_time *= random.uniform(1.5, 2.5)
    
    return round(simulated_time, 1)

def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from text for content matching"""
    
    # Convert to lowercase and remove punctuation
    clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    # Split into words
    words = clean_text.split()
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'what', 'when', 'where', 'why', 'how', 'this', 'that', 'these', 'those'
    }
    
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using keyword overlap"""
    
    keywords1 = set(extract_keywords(text1))
    keywords2 = set(extract_keywords(text2))
    
    if not keywords1 and not keywords2:
        return 0.0
    
    if not keywords1 or not keywords2:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = keywords1.intersection(keywords2)
    union = keywords1.union(keywords2)
    
    similarity = len(intersection) / len(union) if union else 0.0
    
    return similarity

def find_similar_content(target_text: str, content_list: List[Dict], 
                        text_field: str = 'text', threshold: float = 0.3) -> List[Dict]:
    """Find content similar to target text"""
    
    similar_content = []
    
    for content in content_list:
        content_text = content.get(text_field, '')
        similarity = calculate_similarity(target_text, content_text)
        
        if similarity >= threshold:
            content_copy = content.copy()
            content_copy['similarity_score'] = similarity
            similar_content.append(content_copy)
    
    # Sort by similarity score (descending)
    similar_content.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return similar_content

def categorize_difficulty(accuracy: float, response_time: float) -> str:
    """Categorize appropriate difficulty level for a student"""
    
    # Consider both accuracy and response time
    if accuracy >= 0.85 and response_time < 25:
        return 'challenge'
    elif accuracy >= 0.7 and response_time < 35:
        return 'moderate'
    elif accuracy >= 0.5:
        return 'practice'
    else:
        return 'remedial'

def format_time_duration(seconds: float) -> str:
    """Format time duration in a human-readable way"""
    
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"

def validate_answer(user_answer: str, expected_answer: str, 
                   question_type: str = 'text') -> bool:
    """Validate user answer against expected answer"""
    
    if not user_answer or not expected_answer:
        return False
    
    # Clean both answers
    user_clean = user_answer.strip().lower()
    expected_clean = expected_answer.strip().lower()
    
    if question_type == 'numeric':
        try:
            # Try to convert to numbers and compare
            user_num = float(user_clean)
            expected_num = float(expected_clean)
            return abs(user_num - expected_num) < 0.01  # Allow small floating point errors
        except ValueError:
            pass
    
    elif question_type == 'fraction':
        # Handle fraction comparison
        try:
            user_fraction = eval_fraction(user_clean)
            expected_fraction = eval_fraction(expected_clean)
            return abs(user_fraction - expected_fraction) < 0.01
        except:
            pass
    
    # Default to text comparison
    return user_clean == expected_clean

def eval_fraction(fraction_str: str) -> float:
    """Safely evaluate a fraction string"""
    
    # Handle fractions like "1/2", "3/4", etc.
    if '/' in fraction_str:
        parts = fraction_str.split('/')
        if len(parts) == 2:
            try:
                numerator = float(parts[0].strip())
                denominator = float(parts[1].strip())
                if denominator != 0:
                    return numerator / denominator
            except ValueError:
                pass
    
    # Try to evaluate as regular number
    try:
        return float(fraction_str)
    except ValueError:
        raise ValueError(f"Cannot evaluate fraction: {fraction_str}")

def generate_hint(question_text: str, difficulty: int) -> str:
    """Generate contextual hints for questions"""
    
    # Extract key terms from question
    keywords = extract_keywords(question_text)
    
    # General hints based on common math topics
    hint_patterns = {
        'fraction': [
            "Find a common denominator when adding or subtracting fractions",
            "Remember: to add fractions, the denominators must be the same",
            "Convert mixed numbers to improper fractions first"
        ],
        'algebra': [
            "Isolate the variable by doing the same operation to both sides",
            "Work backwards from the answer you want",
            "Remember the order of operations (PEMDAS)"
        ],
        'geometry': [
            "Draw a diagram to visualize the problem",
            "Remember the formulas for area and perimeter",
            "Label all known measurements on your diagram"
        ],
        'arithmetic': [
            "Double-check your calculation step by step",
            "Use estimation to verify your answer makes sense",
            "Remember the multiplication tables"
        ]
    }
    
    # Determine topic based on keywords
    topic = 'arithmetic'  # default
    for key in hint_patterns:
        if any(keyword in key for keyword in keywords):
            topic = key
            break
    
    # Select appropriate hint
    hints = hint_patterns.get(topic, hint_patterns['arithmetic'])
    
    # Choose hint based on difficulty
    if difficulty <= 2:
        return random.choice(hints)
    else:
        return f"{random.choice(hints)} This is a {difficulty}-star difficulty question, so take your time."

def calculate_learning_velocity(historical_accuracy: List[float]) -> str:
    """Calculate learning velocity based on historical performance"""
    
    if len(historical_accuracy) < 2:
        return "Insufficient data"
    
    # Calculate trend using simple linear regression
    x = list(range(len(historical_accuracy)))
    y = historical_accuracy
    
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(x[i] ** 2 for i in range(n))
    
    # Calculate slope
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    
    if slope > 0.05:
        return "Fast improvement"
    elif slope > 0.02:
        return "Steady improvement"
    elif slope > -0.02:
        return "Stable performance"
    else:
        return "Needs attention"

def create_study_plan(profile: Dict[str, float], weak_topics: List[str]) -> Dict[str, Any]:
    """Create a personalized study plan"""
    
    accuracy = profile.get('accuracy', 0)
    engagement = profile.get('engagement', 0)
    pace = profile.get('pace', 0)
    
    plan = {
        'duration_weeks': 4,
        'sessions_per_week': 3,
        'session_duration_minutes': 30,
        'focus_areas': weak_topics[:3],  # Top 3 weak topics
        'recommendations': []
    }
    
    # Adjust plan based on performance
    if accuracy < 0.5:
        plan['session_duration_minutes'] = 45
        plan['sessions_per_week'] = 4
        plan['recommendations'].append("Focus on fundamental concepts")
        plan['recommendations'].append("Use visual aids and manipulatives")
    
    elif accuracy < 0.7:
        plan['recommendations'].append("Practice mixed problem sets")
        plan['recommendations'].append("Review mistakes and understand errors")
    
    else:
        plan['session_duration_minutes'] = 25
        plan['recommendations'].append("Challenge yourself with advanced problems")
        plan['recommendations'].append("Explore real-world applications")
    
    if engagement < 0.7:
        plan['recommendations'].append("Try interactive learning tools")
        plan['recommendations'].append("Set small, achievable goals")
    
    if pace > 35:
        plan['recommendations'].append("Practice timed exercises to improve speed")
    elif pace < 15:
        plan['recommendations'].append("Slow down and double-check your work")
    
    return plan

# Utility functions for data validation
def validate_student_data(student_df: pd.DataFrame) -> List[str]:
    """Validate student data format"""
    errors = []
    required_columns = ['student_id', 'name', 'grade', 'preferred_format']
    
    for col in required_columns:
        if col not in student_df.columns:
            errors.append(f"Missing required column: {col}")
    
    if not errors:
        if student_df['student_id'].duplicated().any():
            errors.append("Duplicate student IDs found")
        
        valid_formats = ['text', 'video', 'interactive']
        invalid_formats = student_df[~student_df['preferred_format'].isin(valid_formats)]
        if not invalid_formats.empty:
            errors.append(f"Invalid preferred formats found: {invalid_formats['preferred_format'].unique()}")
    
    return errors

def validate_question_data(questions_df: pd.DataFrame) -> List[str]:
    """Validate question data format"""
    errors = []
    required_columns = ['question_id', 'topic', 'difficulty', 'text', 'hint']
    
    for col in required_columns:
        if col not in questions_df.columns:
            errors.append(f"Missing required column: {col}")
    
    if not errors:
        if questions_df['question_id'].duplicated().any():
            errors.append("Duplicate question IDs found")
        
        if questions_df['difficulty'].min() < 1 or questions_df['difficulty'].max() > 5:
            errors.append("Difficulty values should be between 1 and 5")
    
    return errors

if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...")
    
    # Test feedback generation
    sample_profile = {'accuracy': 0.75, 'pace': 25.5, 'engagement': 0.9}
    sample_student = {'name': 'Alice', 'preferred_format': 'video'}
    
    feedback = generate_feedback(0.75, sample_profile, sample_student)
    print(f"Sample feedback: {feedback}")
    
    # Test similarity calculation
    similarity = calculate_similarity("solve algebraic equations", "algebra problems with variables")
    print(f"Text similarity: {similarity}")
    
    print("Utility functions test completed!")
