__author__ = 'rowley'
from manager import app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

else:
    print(__name__)