# library imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# module imports
from .routes import blog_content,users, auth, password_reset

# initialize an app
app = FastAPI()

# Handle CORS protection
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# register all the router endpoint
app.include_router(blog_content.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password_reset.router)
