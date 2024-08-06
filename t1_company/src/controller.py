from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, Response

from t1_company.src.shema import User
from t1_company.src.service import login, get_current_user, get_practice

router = APIRouter()


@router.get("/", tags=["Main page"])
def get_main_page() -> RedirectResponse:
    return RedirectResponse("/login", status_code=302)


@router.post("/login", tags=["Login"])
def get_login_page(response: Response, user_data: User) -> RedirectResponse:
    return login(response=response, user_data=user_data)


@router.post("/logout", tags=["Login"])
async def logout_user(response: Response, user_data: User = Depends(get_current_user)) -> dict[str, str]:
    response.delete_cookie(key="user_access_token")
    return {'message': 'Пользователь успешно вышел из системы.'}


@router.get("/appsec", tags=["AppSec"])
async def get_main_appsec(key: str = 'practice_main', user_data: User = Depends(get_current_user)) -> dict[str, str]:
    return get_practice(key=key)
