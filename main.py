import os

import uvicorn
from server import app
from dotenv import load_dotenv

load_dotenv()
PORT = int(os.environ.get("PORT"))

def main():
    uvicorn.run(app, host='0.0.0.0', port=PORT, log_level='info')


if __name__ == "__main__":
    main()
