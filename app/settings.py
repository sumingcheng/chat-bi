import os
from dotenv import load_dotenv


def load_environment():
    env = os.getenv('ENVIRONMENT', 'development')

    if env == 'development':
        load_dotenv(dotenv_path='.env.development')
    elif env == 'production':
        load_dotenv(dotenv_path='.env.production')
    else:
        load_dotenv()

    return env
