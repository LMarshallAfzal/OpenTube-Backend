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
