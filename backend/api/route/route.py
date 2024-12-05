from fastapi import APIRouter

router = APIRouter()

@router.get("/testroute")
def testroute():
    return {"message": "Hello World"}

