import flask as fk
import flask_login as fk_lg


def create_website():

    from .views import views

    app = fk.Flask(__name__)
    app.config["SECRET_KEY"] = "fesgfsges"

    app.register_blueprint(views, url_prefix="/")

    return app
