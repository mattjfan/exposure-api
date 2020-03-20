from application import application
from dotenv import load_dotenv

load_dotenv()
app = application
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)