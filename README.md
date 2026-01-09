# 🚀 AI Proposal Generator

An intelligent proposal generation tool powered by AI that automates the creation of professional project proposals using Groq LLM, semantic search, and vector databases.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Django](https://img.shields.io/badge/django-5.1-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Features

- **AI-Powered Generation**: Uses Groq's Mixtral-8x7b LLM for intelligent proposal creation
- **Semantic Search**: Finds similar past proposals using Sentence Transformers embeddings
- **Vector Database**: FAISS for fast similarity search across proposals
- **Context-Aware**: Leverages past proposals to generate better, more relevant content
- **Clean UI**: Modern, responsive interface with light color scheme
- **Full CRUD**: Create, read, update, and delete proposals
- **Export Ready**: Copy proposals to clipboard for easy sharing

## 🏗️ Architecture
```
User Input → Django Backend → Groq LLM (Generation)
                ↓
         PostgreSQL (Storage)
                ↓
    Sentence Transformer (Embeddings)
                ↓
         FAISS (Vector Search)
                ↓
    Context from Similar Proposals → Enhanced Generation
```

## 🛠️ Tech Stack

- **Backend**: Django 5.1
- **Database**: PostgreSQL 16
- **AI/ML**: 
  - Groq API (Mixtral-8x7b-32768)
  - Sentence Transformers (all-MiniLM-L6-v2)
  - FAISS (Vector similarity search)
- **Frontend**: HTML, CSS, JavaScript
- **Other**: Python-dotenv, psycopg2

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Areel123/AI-Proposal-Generator.git
cd AI-Proposal-Generator
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL
```bash
# Create database
sudo -u postgres psql
CREATE DATABASE proposal_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE proposal_db TO postgres;
\q
```

### 5. Configure environment variables

Create a `.env` file in the project root:
```env
SECRET_KEY=your-django-secret-key-here
DB_NAME=proposal_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
GROQ_API_KEY=your_groq_api_key_here
```

### 6. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 8. Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📖 Usage

1. **Generate Proposal**: Fill in project details (title, description, requirements, budget, timeline)
2. **AI Processing**: The system searches for similar past proposals and generates a tailored proposal
3. **Review & Copy**: View the generated proposal and copy it to clipboard
4. **History**: Access all past proposals, view, or delete them

## 🎨 Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Generated Proposal
![Proposal View](screenshots/proposal.png)

### History
![History](screenshots/history.png)

## 🧪 How It Works

1. **Input Processing**: User provides project details
2. **Embedding Generation**: Sentence Transformer converts text to 384-dimensional vectors
3. **Semantic Search**: FAISS finds the most similar past proposals
4. **Context Building**: Retrieved proposals provide context to the LLM
5. **AI Generation**: Groq LLM generates a tailored proposal
6. **Storage**: Proposal and embedding saved to PostgreSQL
7. **Index Update**: FAISS index updated for future searches

## 📊 Project Structure
```
proposal_generator/
├── proposal_project/       # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── proposals/              # Main app
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── ai_service.py      # AI/ML logic
│   ├── admin.py           # Admin configuration
│   └── urls.py            # URL routing
├── templates/              # HTML templates
│   └── proposals/
│       ├── base.html
│       ├── home.html
│       ├── view_proposal.html
│       └── history.html
├── static/                 # Static files
├── .env                    # Environment variables (not in repo)
├── .gitignore
├── requirements.txt
└── manage.py
```

## 🔧 Configuration

### Groq API

Get your free API key from [console.groq.com](https://console.groq.com)

### PostgreSQL

Default configuration uses:
- Database: `proposal_db`
- User: `postgres`
- Port: `5432`

Modify in `.env` file as needed.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@Areel123](https://github.com/Areel123)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Groq for providing fast LLM inference
- Sentence Transformers for embedding models
- FAISS for efficient similarity search
- Django community for the amazing framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

⭐ Star this repo if you find it helpful!
