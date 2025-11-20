# Comparsy
# A Django-Based AI-Powered Information Comparison Tool

An intelligent **product analysis and comparison platform** built with **Django** and powered by **AI**.  
The tool enables users to search, analyze, and compare products using **multimodal AI (text + link + image)**, delivering smart insights for better decision-making.  

---

## ✨ Features

- 🔎 **Product Search & Comparison** – Compare multiple products side by side.  
- 🤖 **AI-Powered Insights** – Summarizes product features, pros, and cons.  
- 📊 **Dynamic Product Cards** – Clean UI for product comparison.  
- 🌙 **Dark/Light Mode** – Modern, responsive design.  
- 📡 **Product Information API** – Fetches and integrates real-time product details.  
- 🧠 **Gemini/LLM Integration** – Multimodal AI analysis (text + image inputs).  
- 🔐 **User Accounts** – Signup/login with history of comparisons.  

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** Django (Python) 
- **Database:** SQLite / PostgreSQL  
- **AI Integration:** Gemini API / OpenAI API (configurable)
- **Version Control:** Git + GitHub  

---
## 🏗️ Architecture

- **Frontend:** Django Templates, Bootstrap (optional), minimal JS.  
- **Backend:** Django Views, REST API endpoints, AI integration (Gemini/OpenAI).  
- **Database:** SQLite/PostgreSQL.  
- **AI Layer:** Multimodal processing (text + image).  
- **Optional:** Cache frequently accessed product data for performance.
---

## ⚙️ How It Works

1. User searches for products or uploads product images.  
2. Backend fetches product details using **API integration**.  
3. AI analyzes features, prices, pros & cons, and ratings.  
4. Products are displayed side-by-side with **insights and recommendations**.  
5. Users can save comparisons for future reference.
---
## 💡 Key Advantages

- Saves time by consolidating product information.  
- Provides **AI-driven insights** that human research might miss.  
- Multimodal support: text + images.  
- Easy-to-use web interface with **dynamic comparison cards**.  
- Can scale to include more product categories and APIs.
---
## 👥 Target Users

- Online shoppers who want **quick comparisons**.  
- Tech-savvy users who value **AI-powered recommendations**.  
- Developers looking for a **Django + AI integration example**.  
- Startups or businesses needing a **product comparison tool** for their platform.
---
## 🚀 Future Enhancements

- Add **price-tracking and alerts** for products.  
- Integrate **more e-commerce platforms** (Amazon, Flipkart, eBay).  
- Build a **mobile app version**.  
- Add **voice commands** for search and comparison.  
- Include **user reviews and sentiment analysis** in the AI recommendations.
---

## 🙏 Acknowledgements

Django

Gemini API

OpenAI

Bootstrap
 (if used for styling)

 ---
## 📜 License

This project is licensed under the MIT WPU PUNE License – see the LICENSE
 file for details.

---
## 👨‍💻 Author

 Mauli Chavhan
 | [LinkedIn](https://www.linkedin.com/in/mauli-chavhan)
 
 ---
 
## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork this repo and submit a pull request.

---
## 👥 Contributors

A big thanks to everyone who contributed to this project!  

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/MauliChawan.png" width="70" style="border-radius:50%"/><br>
      <b>Mauli Chavhan</b><br>
      Project Lead / Backend Developer<br>
      <a href="https://github.com/MauliChawan">GitHub</a><br>
      <a href="https://www.linkedin.com/in/mauli-chavhan">Linkedin</a>
    </td>
    <td align="center">
      <img src="https://github.com/MishraAmit20.png" width="70" style="border-radius:50%"/><br>
      <b>Amit Mishra</b><br>
      Frontend / UI Designer<br>
      <a href="https://github.com/MishraAmit20">GitHub</a><br>
      <a href="https://www.linkedin.com/in/mauli-chavhan">Linkedin</a>
    </td>
    <td align="center">
      <img src="https://github.com/sankalpsingh404.png" width="70" style="border-radius:50%"/><br>
      <b>Sankalp Singh</b><br>
      AI Integration / Research<br>
      <a href="https://github.com/sankalpsingh404">GitHub</a><br>
      <a href="https://www.linkedin.com/in/mauli-chavhan">Linkedin</a>
    </td>
  </tr>
</table>


  

 ---
## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/MauliChawan/Comparsy.git
cd comparsy
```
### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
pip install -r requirements.txt
```
### 3️⃣ Run Database Migrations
```bash
python manage.py migrate
```
### 4️⃣ Start the Development Server
```bash
python manage.py runserver
```
## ⚙️ Configuration
Add your AI API keys in .env file:
```env 
GEMINI_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
Update settings.py for your database and API configuration.
```


