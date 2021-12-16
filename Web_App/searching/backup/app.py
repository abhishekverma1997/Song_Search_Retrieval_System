from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
    return "ISR project : Searching"
        
if __name__ == "__main__":
    app.run(host='172.31.11.236', port=5000)
