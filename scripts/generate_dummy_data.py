#!/usr/bin/env python3
"""
Script to generate dummy data for the personalized learning platform.
This script creates sample students and questions if the data files don't exist.
"""

import pandas as pd
import os
import random
from datetime import datetime, timedelta

def generate_students_data(num_students: int = 10) -> pd.DataFrame:
    """Generate sample student data"""
    
    # Sample names from different backgrounds
    names = [
        "Rahul", "Aisha", "Sam", "Maya", "Alex", "Priya", "Jordan", "Emma", 
        "Carlos", "Zoe", "Liam", "Sofia", "Ethan", "Aria", "Noah", "Luna",
        "Oliver", "Stella", "Lucas", "Isla", "Mason", "Grace", "Logan", "Hazel"
    ]
    
    grades = [9, 10, 11, 12]
    formats = ["text", "video", "interactive"]
    
    students_data = []
    
    for i in range(num_students):
        student_id = f"s{i+1}"
        name = random.choice(names)
        # Remove chosen name to avoid duplicates
        if name in names:
            names.remove(name)
        
        grade = random.choice(grades)
        preferred_format = random.choice(formats)
        
        students_data.append({
            'student_id': student_id,
            'name': name,
            'grade': grade,
            'preferred_format': preferred_format
        })
    
    return pd.DataFrame(students_data)

def generate_questions_data(num_questions: int = 30) -> pd.DataFrame:
    """Generate sample question data"""
    
    topics = ["fractions", "algebra", "geometry", "arithmetic", "statistics", "trigonometry"]
    
    # Question templates for different topics and difficulties
    question_templates = {
        "fractions": {
            1: [
                ("What is {n1}/{d1} + {n2}/{d1}?", "When denominators are the same, add numerators"),
                ("What is {n1}/{d1} - {n2}/{d1}?", "When denominators are the same, subtract numerators"),
                ("Convert {whole} to an improper fraction with denominator {d1}", "Multiply whole number by denominator, then add numerator")
            ],
            2: [
                ("Add {n1}/{d1} + {n2}/{d2}", "Find common denominator first"),
                ("Subtract {n1}/{d1} - {n2}/{d2}", "Convert to common denominator"),
                ("Convert {decimal} to a fraction", "Think about place values")
            ],
            3: [
                ("Multiply {n1}/{d1} × {n2}/{d2}", "Multiply numerators and denominators"),
                ("Divide {n1}/{d1} ÷ {n2}/{d2}", "Multiply by the reciprocal"),
                ("Simplify {n1}/{d1} + {n2}/{d2} - {n3}/{d3}", "Find common denominator for all fractions")
            ]
        },
        "algebra": {
            1: [
                ("Solve x + {a} = {b}", "Subtract {a} from both sides"),
                ("Solve {a}x = {b}", "Divide both sides by {a}"),
                ("Simplify {a}x + {b}x", "Combine like terms")
            ],
            2: [
                ("Solve {a}x + {b} = {c}", "Subtract {b}, then divide by {a}"),
                ("Expand ({a}x + {b})({c}x + {d})", "Use FOIL method"),
                ("Factor x² + {sum}x + {product}", "Find two numbers that multiply to {product} and add to {sum}")
            ],
            3: [
                ("Solve x² + {b}x + {c} = 0", "Try factoring or use quadratic formula"),
                ("Simplify (x + {a})² - {b}", "Expand the square first"),
                ("Solve the system: x + y = {sum}, x - y = {diff}", "Use substitution or elimination")
            ]
        },
        "geometry": {
            1: [
                ("Find the area of a rectangle with length {l} and width {w}", "Area = length × width"),
                ("Find the perimeter of a square with side {s}", "Perimeter = 4 × side length"),
                ("What is the area of a triangle with base {b} and height {h}?", "Area = (1/2) × base × height")
            ],
            2: [
                ("Find the circumference of a circle with radius {r}", "Use C = 2πr"),
                ("Find the area of a circle with diameter {d}", "First find radius, then use A = πr²"),
                ("Find the volume of a rectangular prism {l}×{w}×{h}", "Volume = length × width × height")
            ],
            3: [
                ("Find the surface area of a cylinder with radius {r} and height {h}", "SA = 2πr² + 2πrh"),
                ("Find the volume of a cone with radius {r} and height {h}", "V = (1/3)πr²h"),
                ("In a right triangle, if one leg is {a} and hypotenuse is {c}, find the other leg", "Use Pythagorean theorem: a² + b² = c²")
            ]
        },
        "arithmetic": {
            1: [
                ("What is {a} + {b}?", "Add the numbers step by step"),
                ("What is {a} - {b}?", "Subtract carefully"),
                ("What is {a} × {b}?", "Use multiplication tables or break down the problem")
            ],
            2: [
                ("Calculate {a} × {b}", "Break it down: {a} × {b} = {breakdown}"),
                ("What is {dividend} ÷ {divisor}?", "Think about what number times {divisor} equals {dividend}"),
                ("What is {percent}% of {number}?", "{percent}% = {percent}/100")
            ],
            3: [
                ("Calculate {base}² + {other}", "Square {base} first, then add {other}"),
                ("Find the square root of {square}", "What number times itself equals {square}?"),
                ("What is {a}³?", "{a} × {a} × {a}")
            ]
        }
    }
    
    questions_data = []
    
    for i in range(num_questions):
        question_id = f"q{i+1}"
        topic = random.choice(topics)
        difficulty = random.randint(1, 3)
        
        # Get appropriate template for topic and difficulty
        if topic in question_templates and difficulty in question_templates[topic]:
            template, hint = random.choice(question_templates[topic][difficulty])
            
            # Generate random values for template
            values = {}
            for param in ['a', 'b', 'c', 'd', 'n1', 'n2', 'n3', 'd1', 'd2', 'd3', 
                         'l', 'w', 'h', 'r', 's', 'sum', 'diff', 'product', 'base', 
                         'other', 'square', 'percent', 'number', 'whole', 'decimal',
                         'dividend', 'divisor', 'breakdown']:
                if f'{{{param}}}' in template:
                    if param in ['percent']:
                        values[param] = random.choice([10, 20, 25, 50, 75])
                    elif param in ['number']:
                        values[param] = random.randint(20, 200)
                    elif param in ['square']:
                        base_num = random.randint(2, 12)
                        values[param] = base_num ** 2
                    elif param in ['decimal']:
                        values[param] = random.choice([0.25, 0.5, 0.75, 0.125, 0.375])
                    elif param in ['dividend']:
                        divisor = random.randint(2, 15)
                        quotient = random.randint(2, 20)
                        values['dividend'] = divisor * quotient
                        values['divisor'] = divisor
                    elif param.startswith('d'):  # denominators
                        values[param] = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
                    elif param.startswith('n'):  # numerators
                        values[param] = random.randint(1, 10)
                    else:
                        values[param] = random.randint(1, 20)
            
            # Special handling for some parameters
            if 'sum' in values and 'diff' in values:
                # Ensure we can solve the system
                x = (values['sum'] + values['diff']) / 2
                y = (values['sum'] - values['diff']) / 2
                if x != int(x) or y != int(y):
                    values['sum'] = random.choice([10, 12, 14, 16, 18])
                    values['diff'] = random.choice([2, 4, 6])
            
            if 'product' in values and 'sum' in values:
                # Ensure factorizable quadratic
                factors = [(1, values['product']), (2, values['product']//2) if values['product'] % 2 == 0 else (1, values['product'])]
                if factors:
                    f1, f2 = random.choice(factors)
                    values['sum'] = f1 + f2
            
            try:
                text = template.format(**values)
                hint_formatted = hint.format(**values)
            except KeyError:
                # Fallback if template formatting fails
                text = f"Solve this {topic} problem (difficulty {difficulty})"
                hint_formatted = f"Apply {topic} concepts step by step"
        
        else:
            # Fallback for topics not in templates
            text = f"Solve this {topic} problem (difficulty {difficulty})"
            hint_formatted = f"Apply {topic} concepts step by step"
        
        questions_data.append({
            'question_id': question_id,
            'topic': topic,
            'difficulty': difficulty,
            'text': text,
            'hint': hint_formatted
        })
    
    return pd.DataFrame(questions_data)

def generate_sample_logs(students_df: pd.DataFrame, questions_df: pd.DataFrame, 
                        num_sessions: int = 20) -> pd.DataFrame:
    """Generate sample quiz log data"""
    
    logs_data = []
    
    for session in range(num_sessions):
        # Select random student
        student = students_df.sample(n=1).iloc[0]
        student_id = student['student_id']
        
        # Select 5 random questions for the quiz
        quiz_questions = questions_df.sample(n=5)
        
        # Simulate session timestamp
        session_time = datetime.now() - timedelta(days=random.randint(1, 30))
        session_id = f"{student_id}_{session_time.strftime('%Y%m%d_%H%M%S')}"
        
        # Simulate student performance based on grade level
        base_accuracy = 0.4 + (student['grade'] - 9) * 0.15  # Higher grades perform better
        base_accuracy += random.uniform(-0.2, 0.2)  # Add some randomness
        base_accuracy = max(0.1, min(0.95, base_accuracy))  # Clamp between 0.1 and 0.95
        
        correct_count = 0
        skipped_count = 0
        response_times = []
        
        for _, question in quiz_questions.iterrows():
            # Simulate answer correctness based on difficulty and student ability
            difficulty_penalty = (question['difficulty'] - 1) * 0.15
            prob_correct = max(0.1, base_accuracy - difficulty_penalty)
            
            # Simulate skipping (lower ability students skip more)
            prob_skip = max(0.05, 0.3 - base_accuracy)
            
            is_skipped = random.random() < prob_skip
            is_correct = not is_skipped and random.random() < prob_correct
            
            # Simulate response time
            base_time = 20 + question['difficulty'] * 10
            response_time = base_time * random.uniform(0.5, 2.0)
            if is_skipped:
                response_time *= 0.3  # Quick skip
            
            if is_correct:
                correct_count += 1
            if is_skipped:
                skipped_count += 1
            
            response_times.append(response_time)
            
            # Create log entry
            logs_data.append({
                'student_id': student_id,
                'timestamp': session_time.isoformat(),
                'question_id': question['question_id'],
                'answer': 'correct_answer' if is_correct else ('skipped' if is_skipped else 'wrong_answer'),
                'correct': is_correct,
                'skipped': is_skipped,
                'response_time': round(response_time, 1),
                'accuracy': correct_count / len(quiz_questions),
                'engagement': 1 - (skipped_count / len(quiz_questions)),
                'avg_response_time': sum(response_times) / len(response_times),
                'session_id': session_id
            })
    
    return pd.DataFrame(logs_data)

def main():
    """Main function to generate all dummy data"""
    
    print("🔧 Generating dummy data for Personalized Learning Platform...")
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate students data
    print("👥 Generating student data...")
    students_df = generate_students_data(num_students=10)
    students_df.to_csv('data/sample_students.csv', index=False)
    print(f"✅ Created {len(students_df)} student records")
    
    # Generate questions data
    print("❓ Generating question data...")
    questions_df = generate_questions_data(num_questions=25)
    questions_df.to_csv('data/sample_questions.csv', index=False)
    print(f"✅ Created {len(questions_df)} questions")
    
    # Generate sample logs
    print("📊 Generating sample quiz logs...")
    logs_df = generate_sample_logs(students_df, questions_df, num_sessions=15)
    logs_df.to_csv('data/logs.csv', index=False)
    print(f"✅ Created {len(logs_df)} log entries from {logs_df['session_id'].nunique()} quiz sessions")
    
    # Create empty learner profiles file
    print("👤 Creating learner profiles structure...")
    profiles = {}
    with open('data/learner_profiles.json', 'w') as f:
        import json
        json.dump(profiles, f, indent=2)
    print("✅ Created learner profiles file")
    
    print("\n🎉 Dummy data generation completed successfully!")
    print("\nGenerated files:")
    print("- data/sample_students.csv")
    print("- data/sample_questions.csv") 
    print("- data/logs.csv")
    print("- data/learner_profiles.json")
    
    print("\n📋 Data Summary:")
    print(f"- Students: {len(students_df)}")
    print(f"- Questions: {len(questions_df)}")
    print(f"- Quiz Sessions: {logs_df['session_id'].nunique()}")
    print(f"- Total Log Entries: {len(logs_df)}")
    
    # Display sample data
    print("\n📝 Sample Student Data:")
    print(students_df.head().to_string(index=False))
    
    print("\n📝 Sample Question Data:")
    print(questions_df[['question_id', 'topic', 'difficulty', 'text']].head().to_string(index=False))
    
    print(f"\n📊 Topics Distribution:")
    topic_counts = questions_df['topic'].value_counts()
    for topic, count in topic_counts.items():
        print(f"- {topic}: {count}")
    
    print(f"\n📊 Difficulty Distribution:")
    difficulty_counts = questions_df['difficulty'].value_counts().sort_index()
    for diff, count in difficulty_counts.items():
        print(f"- Level {diff}: {count}")

if __name__ == "__main__":
    main()
