from application import application
from dotenv import load_dotenv

load_dotenv()
app = application
if __name__ == "__main__":
    app.debug = True
    app.run()