"""
run.py

Wrapper script for launching Docket app.

Tyler Huntington, 2018
"""
import os
from project import app

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
