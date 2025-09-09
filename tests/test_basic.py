import pytest
import pandas as pd
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import LearnerProfile, ContentRecommender, create_sample_profiles
from logger import QuizLogger
from utils import (
    generate_feedback, simulate_response_time, extract_keywords,
    calculate_similarity, validate_answer, validate_student_data,
    validate_question_data
)

class TestBasicImports:
    """Test that all modules can be imported successfully"""
    
    def test_import_app(self):
        """Test that the main app module can be imported"""
        try:
            import app
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import app module: {e}")
    
    def test_import_models(self):
        """Test that the models module can be imported"""
        try:
            import models
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import models module: {e}")
    
    def test_import_logger(self):
        """Test that the logger module can be imported"""
        try:
            import logger
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import logger module: {e}")
    
    def test_import_utils(self):
        """Test that the utils module can be imported"""
        try:
            import utils
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import utils module: {e}")

class TestLearnerProfile:
    """Test the LearnerProfile class functionality"""
    
    def setup_method(self):
        """Set up test environment before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        os.makedirs('data', exist_ok=True)
    
    def teardown_method(self):
        """Clean up after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_profile_initialization(self):
        """Test that LearnerProfile can be initialized"""
        profile_manager = LearnerProfile()
        assert profile_manager is not None
        assert hasattr(profile_manager, 'profiles')
    
    def test_profile_update(self):
        """Test profile update functionality"""
        profile_manager = LearnerProfile()
        
        # Sample quiz answers
        sample_answers = {
            'q1': {'answer': 'correct', 'correct': True, 'skipped': False, 'response_time': 25.0},
            'q2': {'answer': 'wrong', 'correct': False, 'skipped': False, 'response_time': 30.0},
            'q3': {'answer': '', 'correct': False, 'skipped': True, 'response_time': 5.0}
        }
        
        # Update profile
        result = profile_manager.update_profile('test_student', sample_answers)
        
        # Check that result is a dictionary with expected keys
        assert isinstance(result, dict)
        assert 'accuracy' in result
        assert 'pace' in result
        assert 'engagement' in result
        
        # Check that accuracy is calculated correctly (1 correct out of 3)
        assert abs(result['accuracy'] - (1/3)) < 0.01
        
        # Check that engagement accounts for skipped questions (1 skipped out of 3)
        assert abs(result['engagement'] - (2/3)) < 0.01
    
    def test_get_profile(self):
        """Test profile retrieval"""
        profile_manager = LearnerProfile()
        
        # Initially should return None for non-existent student
        profile = profile_manager.get_profile('non_existent')
        assert profile is None
        
        # After updating, should return the profile
        sample_answers = {
            'q1': {'answer': 'correct', 'correct': True, 'skipped': False, 'response_time': 25.0}
        }
        profile_manager.update_profile('test_student', sample_answers)
        
        profile = profile_manager.get_profile('test_student')
        assert profile is not None
        assert isinstance(profile, dict)

class TestContentRecommender:
    """Test the ContentRecommender class functionality"""
    
    def test_recommender_initialization(self):
        """Test that ContentRecommender can be initialized"""
        recommender = ContentRecommender()
        assert recommender is not None
    
    def test_get_recommendations(self):
        """Test recommendation generation"""
        recommender = ContentRecommender()
        
        # Sample profile and questions
        profile = {'accuracy': 0.75, 'pace': 25.0, 'engagement': 0.9}
        
        questions_df = pd.DataFrame({
            'question_id': ['q1', 'q2', 'q3', 'q4'],
            'topic': ['algebra', 'geometry', 'fractions', 'algebra'],
            'difficulty': [1, 2, 3, 2],
            'text': ['Solve x + 1 = 2', 'Find area of square', 'Add 1/2 + 1/3', 'Solve 2x = 8'],
            'hint': ['Subtract 1', 'Side squared', 'Common denominator', 'Divide by 2']
        })
        
        recommendations = recommender.get_recommendations('test_student', profile, questions_df)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3  # Should return at most 3 recommendations
        
        if recommendations:  # If any recommendations returned
            for rec in recommendations:
                assert isinstance(rec, dict)
                assert 'type' in rec
                assert 'question_id' in rec

class TestQuizLogger:
    """Test the QuizLogger class functionality"""
    
    def setup_method(self):
        """Set up test environment before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        os.makedirs('data', exist_ok=True)
    
    def teardown_method(self):
        """Clean up after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_logger_initialization(self):
        """Test that QuizLogger can be initialized"""
        logger = QuizLogger()
        assert logger is not None
        assert hasattr(logger, 'log_file')
    
    def test_log_attempt(self):
        """Test logging a quiz attempt"""
        logger = QuizLogger()
        
        # Sample data
        questions_df = pd.DataFrame({
            'question_id': ['q1', 'q2'],
            'topic': ['algebra', 'geometry'],
            'difficulty': [1, 2],
            'text': ['Solve x + 1 = 2', 'Find area'],
            'hint': ['Subtract 1', 'Formula needed']
        })
        
        answers = {
            'q1': {'answer': 'x=1', 'correct': True, 'skipped': False, 'response_time': 25.0},
            'q2': {'answer': '', 'correct': False, 'skipped': True, 'response_time': 5.0}
        }
        
        # Log attempt
        result = logger.log_attempt('test_student', questions_df, answers)
        
        assert result is True  # Should return True on success
        
        # Check that log file was created and contains data
        logs = logger.get_all_logs()
        assert not logs.empty
        assert 'test_student' in logs['student_id'].values

class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_generate_feedback(self):
        """Test feedback generation"""
        profile = {'accuracy': 0.75, 'pace': 25.0, 'engagement': 0.9}
        student_info = {'name': 'Test Student', 'preferred_format': 'text'}
        
        feedback = generate_feedback(0.75, profile, student_info)
        
        assert isinstance(feedback, str)
        assert len(feedback) > 0
        assert 'Test Student' in feedback
    
    def test_simulate_response_time(self):
        """Test response time simulation"""
        time1 = simulate_response_time(1)  # Easy question
        time2 = simulate_response_time(3)  # Hard question
        
        assert isinstance(time1, float)
        assert isinstance(time2, float)
        assert time1 > 0
        assert time2 > 0
        # Harder questions should generally take longer
        # Note: This is probabilistic, so we can't guarantee it always
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        text = "Solve the algebraic equation for x"
        keywords = extract_keywords(text)
        
        assert isinstance(keywords, list)
        assert 'solve' in keywords
        assert 'algebraic' in keywords
        assert 'equation' in keywords
        # Stop words should be removed
        assert 'the' not in keywords
        assert 'for' not in keywords
    
    def test_calculate_similarity(self):
        """Test text similarity calculation"""
        text1 = "solve algebraic equations"
        text2 = "algebra problem solving"
        text3 = "geometry shapes and angles"
        
        # Similar texts should have higher similarity
        sim1 = calculate_similarity(text1, text2)
        sim2 = calculate_similarity(text1, text3)
        
        assert isinstance(sim1, float)
        assert isinstance(sim2, float)
        assert 0 <= sim1 <= 1
        assert 0 <= sim2 <= 1
        assert sim1 > sim2  # algebra texts should be more similar than algebra vs geometry
    
    def test_validate_answer(self):
        """Test answer validation"""
        # Test exact match
        assert validate_answer("42", "42", "text")
        assert not validate_answer("42", "43", "text")
        
        # Test case insensitivity
        assert validate_answer("HELLO", "hello", "text")
        
        # Test numeric validation
        assert validate_answer("3.14", "3.14", "numeric")
        assert validate_answer("3.140", "3.14", "numeric")  # Should handle precision
    
    def test_validate_student_data(self):
        """Test student data validation"""
        # Valid data
        valid_df = pd.DataFrame({
            'student_id': ['s1', 's2'],
            'name': ['Alice', 'Bob'],
            'grade': [9, 10],
            'preferred_format': ['text', 'video']
        })
        
        errors = validate_student_data(valid_df)
        assert len(errors) == 0
        
        # Invalid data - missing column
        invalid_df = pd.DataFrame({
            'student_id': ['s1', 's2'],
            'name': ['Alice', 'Bob']
            # Missing grade and preferred_format
        })
        
        errors = validate_student_data(invalid_df)
        assert len(errors) > 0
    
    def test_validate_question_data(self):
        """Test question data validation"""
        # Valid data
        valid_df = pd.DataFrame({
            'question_id': ['q1', 'q2'],
            'topic': ['algebra', 'geometry'],
            'difficulty': [1, 2],
            'text': ['Solve x=1', 'Find area'],
            'hint': ['Subtract', 'Use formula']
        })
        
        errors = validate_question_data(valid_df)
        assert len(errors) == 0
        
        # Invalid data - difficulty out of range
        invalid_df = pd.DataFrame({
            'question_id': ['q1', 'q2'],
            'topic': ['algebra', 'geometry'],
            'difficulty': [1, 10],  # 10 is out of range
            'text': ['Solve x=1', 'Find area'],
            'hint': ['Subtract', 'Use formula']
        })
        
        errors = validate_question_data(invalid_df)
        assert len(errors) > 0

class TestDataGeneration:
    """Test data generation functionality"""
    
    def setup_method(self):
        """Set up test environment before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        os.makedirs('data', exist_ok=True)
    
    def teardown_method(self):
        """Clean up after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_sample_data_files_exist(self):
        """Test that sample data files can be created"""
        # Create sample CSV files
        students_data = {
            'student_id': ['s1', 's2'],
            'name': ['Alice', 'Bob'],
            'grade': [9, 10],
            'preferred_format': ['text', 'video']
        }
        students_df = pd.DataFrame(students_data)
        students_df.to_csv('data/sample_students.csv', index=False)
        
        questions_data = {
            'question_id': ['q1', 'q2'],
            'topic': ['algebra', 'geometry'],
            'difficulty': [1, 2],
            'text': ['Solve x + 1 = 2', 'Find area of square'],
            'hint': ['Subtract 1', 'Side squared']
        }
        questions_df = pd.DataFrame(questions_data)
        questions_df.to_csv('data/sample_questions.csv', index=False)
        
        # Verify files exist and can be read
        assert os.path.exists('data/sample_students.csv')
        assert os.path.exists('data/sample_questions.csv')
        
        # Test reading the files
        read_students = pd.read_csv('data/sample_students.csv')
        read_questions = pd.read_csv('data/sample_questions.csv')
        
        assert len(read_students) == 2
        assert len(read_questions) == 2
        assert 'student_id' in read_students.columns
        assert 'question_id' in read_questions.columns
    
    def test_create_sample_profiles(self):
        """Test sample profile creation"""
        profiles = create_sample_profiles()
        
        assert isinstance(profiles, dict)
        assert len(profiles) > 0
        
        # Check profile structure
        for student_id, profile in profiles.items():
            assert isinstance(profile, dict)
            assert 'accuracy' in profile
            assert 'pace' in profile
            assert 'engagement' in profile
            assert 'quiz_count' in profile
            assert 'last_updated' in profile
        
        # Verify file was created
        assert os.path.exists('data/learner_profiles.json')

class TestIntegration:
    """Integration tests for the complete system"""
    
    def setup_method(self):
        """Set up test environment before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        os.makedirs('data', exist_ok=True)
        
        # Create minimal test data
        students_data = {
            'student_id': ['s1'],
            'name': ['Test Student'],
            'grade': [10],
            'preferred_format': ['text']
        }
        self.students_df = pd.DataFrame(students_data)
        self.students_df.to_csv('data/sample_students.csv', index=False)
        
        questions_data = {
            'question_id': ['q1', 'q2', 'q3'],
            'topic': ['algebra', 'geometry', 'fractions'],
            'difficulty': [1, 2, 1],
            'text': ['Solve x + 1 = 2', 'Find area of square', 'Add 1/2 + 1/4'],
            'hint': ['Subtract 1', 'Side squared', 'Common denominator']
        }
        self.questions_df = pd.DataFrame(questions_data)
        self.questions_df.to_csv('data/sample_questions.csv', index=False)
    
    def teardown_method(self):
        """Clean up after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_complete_quiz_workflow(self):
        """Test the complete quiz workflow"""
        # Initialize components
        logger = QuizLogger()
        profile_manager = LearnerProfile()
        recommender = ContentRecommender()
        
        # Simulate a quiz session
        student_id = 's1'
        sample_answers = {
            'q1': {'answer': '1', 'correct': True, 'skipped': False, 'response_time': 25.0},
            'q2': {'answer': 'wrong', 'correct': False, 'skipped': False, 'response_time': 35.0},
            'q3': {'answer': '', 'correct': False, 'skipped': True, 'response_time': 5.0}
        }
        
        # Log the attempt
        log_success = logger.log_attempt(student_id, self.questions_df, sample_answers)
        assert log_success
        
        # Update profile
        updated_profile = profile_manager.update_profile(student_id, sample_answers)
        assert isinstance(updated_profile, dict)
        assert 'accuracy' in updated_profile
        
        # Get recommendations
        recommendations = recommender.get_recommendations(student_id, updated_profile, self.questions_df)
        assert isinstance(recommendations, list)
        
        # Verify data persistence
        logs = logger.get_all_logs()
        assert not logs.empty
        assert student_id in logs['student_id'].values
        
        profile = profile_manager.get_profile(student_id)
        assert profile is not None

def test_main_modules_are_importable():
    """High-level test that main modules can be imported without errors"""
    modules_to_test = ['app', 'models', 'logger', 'utils']
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
        except ImportError as e:
            pytest.fail(f"Failed to import {module_name}: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
