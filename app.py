from flask import Flask, redirect, url_for, session
from database import Base, engine
from api.nft import bp as nft_bp
from api.auth import bp as auth_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"
Base.metadata.create_all(bind=engine)
app.register_blueprint(nft_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("nft.dashboard"))
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)