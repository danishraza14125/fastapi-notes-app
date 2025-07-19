from fastapi import FastAPI, Depends
from app.database import engine
from app import models
from app.routes import user, auth
from app.auth import get_current_user
from app.routes import notes  # 👈 add import

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(notes.router)  # 👈 register router
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Notes App is running"}


# ✅ Place this route here for testing authentication
@app.get("/secure-data")
def get_secure_data(current_user: models.User = Depends(get_current_user)):
    return {"user": current_user.username, "message": "You are authorized"}