from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from t1_company.src.controller import router as main_router
from t1_company.src.exceptions import PracticeException, UserException


def run_api() -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(main_router)

    @app.exception_handler(PracticeException)
    async def practice_exception_handler(request: Request, exc: PracticeException):
        return JSONResponse(
            status_code=404,
            content={"message": exc.text}
        )

    @app.exception_handler(UserException)
    async def user_exception_handler(request: Request, exc: UserException):
        return JSONResponse(
            status_code=401,
            content={"message": exc.text}
        )

    return app
