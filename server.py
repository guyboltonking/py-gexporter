from flask import Flask
from pathlib import Path

app = Flask(__name__)

def create_json_index(root: Path):
    pass
    
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(use_reloader=False, port=22222)
