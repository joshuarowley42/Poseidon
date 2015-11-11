from manager import app
from manager import my_farm

@app.route("/", methods=["GET"])
def home():
    response = ''
    for printer in my_farm.printers:
        response += str(printer.status)
    return response