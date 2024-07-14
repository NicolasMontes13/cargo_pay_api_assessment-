from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.environ.get("HOST") 
PORT = os.environ.get("PORT")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
DATABASE = os.environ.get("DATABASE")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")