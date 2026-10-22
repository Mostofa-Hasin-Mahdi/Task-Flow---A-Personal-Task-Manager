from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

# Placeholder for future dependency injections (repositories, services)
__all__ = ["get_db", "Depends", "Session"]
