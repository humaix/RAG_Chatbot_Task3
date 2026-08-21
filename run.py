from flask import Flask
from app.web.routes import web
def create_app():
    app = Flask(
        __name__,
        template_folder="app/web/templates"
    )
    app.register_blueprint(web)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)