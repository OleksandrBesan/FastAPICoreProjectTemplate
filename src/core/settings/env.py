from functools import wraps
from dotenv import load_dotenv
import os 
ENR_FILE  = ".env" 
ENV_PATH = os.path.join(os.path.dirname(__file__), "../../../", ENR_FILE)