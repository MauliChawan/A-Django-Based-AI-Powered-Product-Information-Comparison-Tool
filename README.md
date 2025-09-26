🛒 A Django-Based AI-Powered Product Information Comparison Tool
📌 Overview

This project is a Django-based web application that leverages AI and Machine Learning to compare product information across multiple e-commerce platforms.
The tool collects product data (price, specifications, reviews), processes it using AI/NLP models, and presents users with a clear comparison dashboard to identify the best deals and insights.


✨ Key Highlights:

Built with Django + Django REST Framework

AI-powered NLP for feature extraction & sentiment analysis

Supports product data from multiple sources (APIs/web scraping)

Comparison engine for price, features, and reviews

Responsive UI for filtering & visualization

Deployable on AWS / Heroku / Docker

⚙️ Features

✅ Multi-source product data collection (APIs & scraping)
✅ AI-driven feature normalization (e.g., “8GB RAM” vs “8192MB RAM”)
✅ Sentiment analysis on customer reviews
✅ Real-time comparison of price, ratings, and specifications
✅ Visual comparison dashboard
✅ REST API support for integration with other apps

🏗️ Tech Stack

Backend: Django, Django REST Framework

Frontend: Django Templates / ReactJS (optional)

Database: PostgreSQL / MySQL

AI/ML: Scikit-learn, HuggingFace Transformers, spaCy

Task Management: Celery + Redis (for background scraping tasks)

Deployment: Docker, AWS EC2/RDS/S3, or Heroku

🧠 Future Enhancements

✅ Integration with Amazon/Flipkart/eBay APIs

✅ Advanced recommendation engine using ML ranking models

✅ User login & personalized comparison history

✅ Mobile app integration (React Native / Flutter frontend)

📜 License

This project is licensed under the MIT WPU Pune License.

A-Django-Based-AI-Powered-Product-Information-Comparison-Tool/

│── backend/                   # Django project (API + comparison logic)

│── frontend/                  # Templates or ReactJS frontend

│── ai_engine/                 # AI/NLP models for product comparison

│── data/                      # Datasets or scraped product data

│── docs/                      # Documentation & diagrams

│── requirements.txt      # Python dependencies

│── manage.py             # Django management script

│── README.md             # Project description
