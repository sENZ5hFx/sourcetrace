# Contributing to sourcetrace

This is a private NeuroCatalyst™ project. Contributions are by invitation only.

## Setup
```bash
git clone https://github.com/sENZ5hFx/sourcetrace
cd sourcetrace
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Testing
```bash
pytest tests/ -v
```

## Code Standards
- Python 3.11+, type-annotated throughout
- Pydantic v2 for all I/O schemas
- No external DB dependencies in core (swap-ready)
- Every endpoint must have a corresponding test

## Branch model
- `main` — production
- Feature branches: `feat/description`
- Bug fixes: `fix/description`

---
*© 2026 Haley Ann Bird. All rights reserved.*
