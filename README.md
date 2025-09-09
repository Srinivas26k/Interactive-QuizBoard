# 🎓 Personalized Learning Platform

A lightweight Streamlit web app that demonstrates personalized learning through quiz-taking, real-time logging, learner profiling, ML-powered content recommendations, and teacher analytics dashboard.

![Personalized Learning Platform](https://img.shields.io/badge/python-3.11-blue)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **📝 Interactive Quizzes**: Adaptive 5-question quizzes with real-time tracking
- **👤 Learner Profiling**: Automatic calculation of accuracy, pace, and engagement metrics
- **🤖 Smart Recommendations**: ML-powered content suggestions using scikit-learn
- **📊 Teacher Dashboard**: Comprehensive analytics with student performance insights
- **💾 Data Persistence**: CSV-based logging with in-memory backup
- **🎯 Personalized Feedback**: Template-based feedback with skill-specific hints

## 📸 Screenshots

![Home Page](screenshots/home.png)
![Quiz Page](screenshots/quiz.png)
![Results Page](screenshots/results.png)
![Teacher Dashboard](screenshots/dashboard.png)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd personalized-learning-platform
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501` to use the application.

## 🛠️ Project Structure

```
personalized-learning-platform/
├── app.py                 # Main Streamlit application
├── models.py              # ML models for learner profiling and recommendations
├── logger.py              # Quiz logging and data persistence
├── utils.py               # Utility functions for feedback and data processing
├── pyproject.toml         # Project dependencies (uv)
├── requirements.txt       # Project dependencies (pip)
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── data/
│   ├── sample_students.csv # Sample student data
│   └── sample_questions.csv # Sample question data
└── README.md
```

## 🎯 Usage

1. **Student Mode**:
   - Select your student profile from the dropdown
   - Take a personalized quiz with 5 questions
   - Receive real-time feedback and performance metrics
   - Get personalized content recommendations based on your performance

2. **Teacher Dashboard**:
   - View class-wide analytics and performance metrics
   - Monitor individual student progress
   - Identify struggling students
   - Export data for further analysis

## 🔧 Configuration

The application can be configured through the `.streamlit/config.toml` file:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## 📊 Data Model

### Student Profile
- `student_id`: Unique identifier
- `name`: Student name
- `grade`: Grade level
- `preferred_format`: Learning preference (text, video, interactive)

### Question Data
- `question_id`: Unique identifier
- `topic`: Subject area (fractions, algebra, geometry)
- `difficulty`: Difficulty level (1-5 stars)
- `text`: Question text
- `hint`: Contextual hint

### Performance Metrics
- `accuracy`: Percentage of correct answers
- `pace`: Average response time per question
- `engagement`: Percentage of questions attempted (vs skipped)

## 🤖 Machine Learning

The platform uses:
- **K-Means Clustering** for grouping similar questions
- **Decision Trees** for content recommendation logic
- **Profile-based filtering** for personalized content delivery

## 📈 Analytics

Teacher dashboard provides:
- Class performance summary
- Individual student tracking
- Accuracy distribution charts
- Struggling student identification
- Data export functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [scikit-learn](https://scikit-learn.org/) for ML algorithms
- [Plotly](https://plotly.com/) for interactive charts
- [Pandas](https://pandas.pydata.org/) for data manipulation

## 📞 Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/yourusername/personalized-learning-platform](https://github.com/yourusername/personalized-learning-platform)