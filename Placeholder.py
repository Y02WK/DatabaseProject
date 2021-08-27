from app import app
import os

# Citation for following Listener code:
# Date: 07/31/21
# Copied from
# Source URL: https://github.com/gkochera/CS340-demo-flask-app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9221))
    app.run(port)