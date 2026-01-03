# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed
- Supabase account (free tier available)

## 1. Clone and Setup
```bash
# Clone repository
git clone https://github.com/your-username/ai-career-intelligence.git
cd ai-career-intelligence

# Setup backend
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
```

## 2. Database Setup
1. Create a [Supabase](https://supabase.com) account
2. Create a new project
3. Go to SQL Editor and run the contents of `database_setup.sql`
4. Get your project URL and anon key from Settings > API

## 3. Environment Configuration
```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit with your Supabase credentials
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_anon_key
# SECRET_KEY=your_random_secret_key
```

## 4. Run Application
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

## 5. Access Application
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 🎯 First Test
1. Register a new account
2. Upload a PDF resume
3. Get AI-powered job recommendations

## 🔧 Troubleshooting
- **Module not found**: Run `pip install -r requirements.txt` again
- **Database errors**: Check your Supabase credentials in `.env`
- **Port conflicts**: Change port with `--port 8001`

## 📞 Need Help?
- Check the [full README](README.md)
- Open an [issue](https://github.com/your-username/ai-career-intelligence/issues)
- Review [documentation](docs/)