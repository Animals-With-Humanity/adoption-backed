from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routes import animals, applications, users, form
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(docs_url="/")
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
app.include_router(animals.router, prefix="/animals")
app.include_router(applications.router, prefix="/applications")
app.include_router(users.router, prefix="/users")
app.include_router(form.router, prefix="/form")
if __name__ == '__main__':
    
    import uvicorn
    uvicorn.run(app)