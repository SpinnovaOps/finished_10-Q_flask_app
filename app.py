from flask import Flask
from app import routes
from app.processing.processing_routes import processing_bp
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY  # Required for sessions

# Register existing routes
routes.init_app(app)

# Register the processing Blueprint
app.register_blueprint(processing_bp)

if __name__ == "__main__":
    app.run(debug=True)