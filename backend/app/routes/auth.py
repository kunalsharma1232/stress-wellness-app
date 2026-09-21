from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database.mongodb import users_collection
from app.models.user import UserRegister, UserLogin, TokenResponse, UserPublic
from app.services.auth_service import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def get_current_user(token: str | None = Depends(oauth2_scheme)) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        user_id = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    from bson import ObjectId
    user = await users_collection().find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def _to_public(user: dict) -> UserPublic:
    return UserPublic(id=str(user["_id"]), full_name=user["name"], email=user["email"], age=user["age"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing = await users_collection().find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    user_doc = {
        "name": payload.full_name,
        "email": payload.email,
        "password_hash": hash_password(payload.password),
        "age": payload.age,
        "created_at": datetime.now(timezone.utc),
    }
    result = await users_collection().insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    token = create_access_token(str(result.inserted_id))
    return TokenResponse(access_token=token, user=_to_public(user_doc))


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    user = await users_collection().find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(str(user["_id"]))
    return TokenResponse(access_token=token, user=_to_public(user))


@router.get("/me", response_model=UserPublic)
async def me(current_user: dict = Depends(get_current_user)):
    return _to_public(current_user)
