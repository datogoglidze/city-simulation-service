from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["hellos"])


@router.get("/")
def say_hello() -> str:
    return "Hello World!"
