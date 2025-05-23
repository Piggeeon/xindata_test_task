from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
PATH_TO_FREELANCERS_DATA=os.getenv("PATH_TO_FREELANCERS_DATA")
