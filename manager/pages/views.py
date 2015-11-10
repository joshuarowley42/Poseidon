from manager import app
from manager import farm

@app.route("/", methods=["GET"])
def home():
    response = ''
    for printer in farm.printers:
        response += printer.status
    return response