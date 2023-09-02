import sys
sys.path.insert(0, '.')
from esvr import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
