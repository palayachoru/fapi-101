from typing import Annotated
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from passlib.context import CryptContext
from jose import jwt, JWTError
from jose.exceptions import JWTError

from models import User, UserRequest, PasswordChangeRequest
from database import get_db



# generated using 'openssl rand -hex 32'
SECRET = "88fa54e5f7ecf1697fe93d89341192570ba196b992efaf0908ff5369fe6d0ac5"
ALGORITHM = "HS256"

# set the hashing algorithm to bcrypt
bcrypt_hasher = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Defining dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
auth_passwd_form = Annotated[OAuth2PasswordRequestForm, Depends()]
auth_user_depedency = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))]



### HELPER FUNCTIONS ###
def authenticate_user(username:str, passwd:str, db:Session):
  # retrieve user
  luser = db.query(User).filter(User.username == username).first()
  if not luser:
    return False

  # Authenticate the user
  if not bcrypt_hasher.verify(passwd, luser.hashed_passwd):
    return False

  return luser

def encode_jwt(user: User, expires_at: timedelta):
  """Create a JSON Web Token"""
  payload = {
    "sub": user.username,
    "id": user.id,
    "is_admin": user.is_admin,
    "exp": datetime.now(timezone.utc) + expires_at
  }
  return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def get_user(token: auth_user_depedency):
  try:
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    username:str = payload.get('sub')
    usr_id:int = payload.get('id')
    is_admin:bool = payload.get('is_admin')

    if not username or not usr_id:
      raise HTTPException(status_code=404, detail="Invalid User")
  except JWTError:
    raise HTTPException(status_code=404, detail="Invalid User")

  return {"username": username, "id": usr_id, "is_admin": is_admin}

user_dependency = Annotated[dict, Depends(get_user)]

router = APIRouter(
  prefix = "/auth",           # all end points start with /auth
  tags = ["Authentication"]   # these routes are grouped in Swagger UI
)


@router.post("/signup")
def user_signup(db: db_dependency, user: UserRequest):
  new_user = User(
    email = user.email,
    username = user.username,
    name = user.name,
    hashed_passwd = bcrypt_hasher.hash(user.passwd),
    is_active = True,
    is_admin = user.is_admin
  )

  db.add(new_user)
  db.commit()


@router.post("/login")
def user_login(db: db_dependency, form: auth_passwd_form):
  user = authenticate_user(form.username, form.password, db)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

  token = encode_jwt(user, timedelta(minutes=20))

  # using the OAuth2 password flow convention
  return {"access_token": token, "token_type": "bearer"}


@router.get("/users")
def user_list(db: db_dependency, user: user_dependency):
  if not user or not user.get('is_admin'):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

  return db.query(User).all()


@router.post("/change-password")
def change_password(db: db_dependency, cgpasswd: PasswordChangeRequest, user: dict=Depends(get_user)):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User")

  # verify if the entered curr password matches the password hash
  user_model = db.query(User).filter(User.id == user.get('id')).first()
  if not bcrypt_hasher.verify(cgpasswd.curr_password, user_model.hashed_passwd):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password mismatched")

  # update the password with new password
  user_model.hashed_passwd = bcrypt_hasher.hash(cgpasswd.new_password)

  db.add(user_model)
  db.commit()
