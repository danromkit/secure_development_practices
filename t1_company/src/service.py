from fastapi import status, Depends
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from t1_company.src.exception import PracticeException, UserException
from t1_company.src.shema import User
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from config import settings

users_db = {
    settings.auth.login: {
        "login": settings.auth.login,
        "password": settings.auth.password,
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, key=settings.auth.secret_key, algorithm=settings.auth.algorithm)
    return encode_jwt


def get_user(db, login: str) -> User:
    if login in db:
        user_dict = db[login]
        return User(**user_dict)


def authenticate_user(login: str, password: str) -> User:
    user: User = get_user(users_db, login)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        raise UserException('Неправильный логин или пароль.')
    return user


def login(response: Response, user_data: User):
    try:
        check: User = authenticate_user(login=user_data.login, password=user_data.password)
    except UserException as err:
        raise UserException(err.text)
    access_token: str = create_access_token({"sub": str(check.login)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return RedirectResponse("/appsec?key=practice_main", status_code=status.HTTP_302_FOUND, headers=response.headers)


def get_token(request: Request) -> str | None:
    token: str | None = request.cookies.get('user_access_token')
    if not token:
        raise UserException('Необходимо авторизоваться.')
    return token


def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload: dict[str, str] = jwt.decode(token, key=settings.auth.secret_key, algorithms=[settings.auth.algorithm])
    except JWTError:
        raise UserException('Токен не валидный.')
    expire_time: datetime = datetime.fromtimestamp(int(payload.get('exp')), tz=timezone.utc)
    if expire_time < datetime.now(timezone.utc):
        raise UserException('Срок действия токена истек.')
    user: User = get_user(users_db, payload.get('sub'))
    if not user:
        raise UserException('Указан неправильный пользователь.')
    return user


def get_practice(key: str) -> dict[str, str]:
    for practice in settings.practices:
        if practice.get('practice_name') == key:
            return practice
    else:
        raise PracticeException("Указана неверная практика разработки.")
