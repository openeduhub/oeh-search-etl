import os
import sys
from dotenv import load_dotenv
load_dotenv()

class Env:
    def get(key: str, allowNull = False) -> str:
        value = os.getenv(key)
        if value == None and not allowNull:
            sys.exit('No configuration for key ' + key + ' was found in your .env file. Please refer to the .env.example file for a sample value')
        return value
