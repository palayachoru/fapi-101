from fastapi import APIRouter

from models import User, UserRequest

router = APIRouter()


@router.get("/auth")
def get_user():
  return {'user': 'authenticted'}
