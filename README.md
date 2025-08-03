# OpenTube Backend API

## Project Structure

```
/backend
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app setup
│   ├── core/                # Config, security, utils
│   │   ├── config.py        # Settings (env vars)
│   │   └── security.py      # JWT utilities
│   ├── models/              # Database models
│   │   └── user.py          # User model (SQLModel)
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Login/signup
│   │   └── video.py         # Existing video proxy
│   ├── services/            # Business logic
│   │   ├── auth.py          # User auth logic
│   │   └── youtube.py       # yt-dlp wrapper
│   └── db/                  # Database setup
│       ├── session.py       # SQLAlchemy session
│       └── init_db.py       # Database initialisation
├── requirements.txt
└── .env                     # Environment variables
```

## Prerequisites
 - Python 3.9+
 - pip
 - sqlite3

## Installation
```bash
# Clone the repository
git clone https://github.com/lmarshallafzal/OpenTube-Backend.git
cd OpenTube-Backend

# Install dependencies (using pip)
pip install -r requirements.txt
```

## Database Setup
```bash
# Create sqlite database
python -m db.init_db

# Check the database and all the tables were initialised
sqlite3 database.db
.tables
```

## First-Time Setup
```bash
echo "JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" > .env
```

## Running the Server
```bash
# Start the Uvicorn server (development)
uvicorn main:app --reload

# Production-style (adjust workes as needeed)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Test the API
 - Docs: http://localhost:8000/docs
 - Redoc: http://localhost:8000/redoc


