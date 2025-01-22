import dotenv

from .bot import cli

if __name__ == '__main__':
    env = dotenv.load_dotenv(".env")
    if env:
        cli()
    else:
        print("No dotenv file found")