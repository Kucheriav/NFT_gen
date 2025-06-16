from flask import Flask, redirect, url_for, session
from database import Base, engine
from api.nft import bp as nft_bp
from api.auth import bp as auth_bp
from dotenv import load_dotenv
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.secret_key =  os.getenv('APP_SECRET_KEY')
#Base.metadata.create_all(bind=engine)
app.register_blueprint(nft_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def index():
    # if "user_id" in session:
    #     return redirect(url_for("nft.dashboard"))
    # return redirect(url_for("auth.login"))
    return redirect(url_for("nft.dashboard"))

if __name__ == "__main__":
    app.run(debug=True)