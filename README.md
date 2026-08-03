TalentBridge
A platform where artists, craftsmen, inventors, and creative minds with excellent but unseen work can showcase their creations and connect with interested buyers, investors, and businesses.


🚀 Overview

TalentBridge is a web application built with Flask that bridges the gap between talented creators and potential patrons. Whether you're an artist with a stunning portfolio, a craftsman with unique products, or an inventor with a groundbreaking prototype, TalentBridge gives you the visibility you deserve.

Key Features:

· Showcase creative works with images, descriptions, and metadata  
· Connect creators with buyers, investors, and businesses  
· User authentication and profile management  
· Database-driven content management  
· Scalable Flask architecture  

---

🛠️ Tech Stack

Component Technology  
Backend Flask (Python)  
Database SQL (see talentbridge_database.sql)  
Frontend HTML/CSS/JS (Flask templates)  
Migration Flask-Migrate  
Environment Python 3.x  

---

📂 Project Structure

talentbridge/  
├── run.py                  # Application entry point  
├── requirements.txt        # Python dependencies  
├── flaskusagegd.txt      # Flask usage guide/notes  
├── talentbridge_database.sql # Database schema  
├── pycache/           # Python cache files  
├── instance/              # Instance-specific files  
├── migrations/            # Database migration scripts  
└── pkg/                   # Application packages/modules  

---

🚦 Getting Started

Prerequisites  

· Python 3.8+  
· pip  
· SQLite/PostgreSQL/MySQL (depending on configuration)  

Installation  

1. Clone the repository  

git clone https://github.com/Frankez75/talentbridge.git  
cd talentbridge  

2. Set up a virtual environment  

python -m venv venv  
source venv/bin/activate   # On Windows: venv\Scripts\activate  

3. Install dependencies  

pip install -r requirements.txt  

4. Set up the database  

Import the provided SQL schema or run migrations
flask db upgrade  

5. Run the application  

python run.py  

The application will be available at http://localhost:5000  

---

🔧 Configuration

Create a .env file or set environment variables for sensitive configurations:

FLASK_APP=run.py  
FLASK_ENV=development  
DATABASE_URL=sqlite:///talentbridge.db  
SECRET_KEY=your-secret-key  

---

🧪 Development Status

Last Commit: July 25, 2026  
Status: Core functionality implemented, API and email integration pending.  

The latest updates include:  

· ✅ Fixed Flask issues and core structure  
· ✅ Database schema defined  
· ✅ Migration setup completed  
· 🚧 API endpoints (in progress)  
· 🚧 Email notifications (in progress)  

---

🤝 Contributing

Contributions are welcome! Here's how you can help:  

1. Fork the repository  
2. Create a feature branch (git checkout -b feature/amazing-feature)  
3. Commit your changes (git commit -m 'Add some amazing feature')  
4. Push to the branch (git push origin feature/amazing-feature)  
5. Open a Pull Request  

---

📝 License

This project is open-source. Check the repository for specific licensing information.  

---

📬 Contact

Project Link: https://github.com/Frankez75/talentbridge  

---

🙏 Acknowledgements

· Built with Flask and the Python ecosystem  
· Inspired by the need to connect unseen talent with opportunity  

---

Made with ❤️ for creators everywhere.
