from fastapi import FastAPI
import uvicorn
from src import auth_router, user_router, main_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(main_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

