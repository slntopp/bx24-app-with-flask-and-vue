#!/usr/bin/env python3.8
from app import app
from dotenv import load_dotenv
load_dotenv()

import os

if __name__ == "__main__":
    app.debug = True
    app.run(port=os.environ.get('PORT', 8000))