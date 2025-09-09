# Personalized Learning Platform

## Overview

This is a lightweight Streamlit web application that demonstrates personalized learning through interactive quizzes, real-time performance tracking, and ML-powered content recommendations. The platform provides a complete learning ecosystem with student quiz-taking functionality, automatic learner profiling based on accuracy/pace/engagement metrics, intelligent content recommendations using scikit-learn, and a comprehensive teacher analytics dashboard. The system uses CSV-based data persistence with in-memory backup for reliable data storage without requiring external databases.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Streamlit Web Application**: Single-page application with multiple views (Quiz, Teacher Dashboard, Student Profile)
- **Session State Management**: Uses Streamlit's session state to track quiz progress, student data, and application state
- **Interactive Components**: Real-time quiz interface with question navigation, answer validation, and progress tracking
- **Data Visualization**: Plotly integration for creating interactive charts and graphs in the teacher dashboard

### Backend Architecture
- **Modular Design**: Separated into distinct modules (models.py, logger.py, utils.py) for maintainability
- **LearnerProfile Class**: Manages student profiles and performance metrics using JSON storage
- **ContentRecommender Class**: Implements ML-powered content recommendations using sklearn clustering and decision trees
- **QuizLogger Class**: Handles all quiz attempt logging and performance data persistence

### Data Storage Solutions
- **CSV-based Persistence**: Primary data storage using CSV files for student data, questions, and logs
- **JSON Profile Storage**: Student profiles and performance metrics stored in JSON format
- **In-memory Backup**: Session-based data retention to prevent data loss during user sessions
- **File System Organization**: Structured data directory with separate files for students, questions, logs, and profiles

### Machine Learning Components
- **Scikit-learn Integration**: Uses KMeans clustering for student grouping and DecisionTreeClassifier for content recommendations
- **Optional Sentence Transformers**: Implements text embeddings using all-MiniLM-L6-v2 model with fallback to keyword matching
- **Performance Profiling**: Automated calculation of accuracy, response time, and engagement metrics
- **Adaptive Recommendations**: ML model training based on historical student performance data

### Application Flow
- **Quiz System**: 5-question adaptive quizzes with real-time response tracking and scoring
- **Profile Generation**: Automatic learner profile creation based on quiz performance metrics
- **Recommendation Engine**: Content suggestions based on student performance patterns and ML analysis
- **Analytics Dashboard**: Teacher view with comprehensive student performance insights and trend analysis

## External Dependencies

### Core Dependencies
- **Streamlit (>=1.25)**: Web application framework for the user interface
- **Pandas**: Data manipulation and CSV file handling
- **Scikit-learn**: Machine learning algorithms for clustering and classification
- **Plotly**: Interactive data visualization for charts and graphs
- **NumPy**: Numerical computing support for ML operations

### Optional Dependencies
- **Sentence-transformers**: Text embedding model (all-MiniLM-L6-v2) for advanced content matching
- **Typing Extensions**: Enhanced type hints for better code documentation

### Development Dependencies
- **Pytest**: Testing framework for unit and integration tests

### Data Sources
- **Sample CSV Files**: Pre-generated student and question datasets
- **Local File System**: All data persistence handled through local files, no external databases required
- **No External APIs**: Completely self-contained system with no third-party service dependencies

### Deployment Considerations
- **CPU-only Operation**: All ML models designed to run on CPU without GPU requirements
- **No API Keys Required**: Zero external service dependencies for cost-free operation
- **Replit Compatible**: Structured for easy deployment on Replit platform