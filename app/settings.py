"""Module to store shared config stuff."""
import os

import dotenv

dotenv.load_dotenv()


DB_URL = os.getenv('DB_URL')
if not DB_URL:
    raise Exception('Missing DB_URL env variable')

PASSWORD_SALT = 'test_salt'