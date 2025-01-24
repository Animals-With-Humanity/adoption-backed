from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from app.models import Base
from app.routes import animals, applications, users, form,caretaker
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
load_dotenv()
app = FastAPI(docs_url=None)


security = HTTPBasic()
USERNAME = os.getenv("SWAGGER_USERNAME", "admin")
PASSWORD = os.getenv("SWAGGER_PASSWORD", "secret")
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_docs(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="API Docs")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; change this to specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(caretaker.router, prefix="/caretaker")
app.include_router(animals.router, prefix="/animals")
app.include_router(applications.router, prefix="/applications")
app.include_router(form.router, prefix="/form")
app.include_router(users.router, prefix="/users")
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)