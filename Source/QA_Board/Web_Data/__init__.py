import flask as fk
import flask_login as fk_lg
from . import models
from . import wmgtss_qa


def create_website():
    """
    Generates a Flask webserver to access the WMGTSS QA Board web page
    :return:
    """

    # gather our bluprints to use
    from .auth import auth
    from .views import views

    # initialise the web app with a secret key
    app = fk.Flask(__name__)
    app.config["SECRET_KEY"] = "fesgfsges"

    # init our blueprints with route prefixes
    app.register_blueprint(auth, url_prefix="/Auth")
    app.register_blueprint(views, url_prefix="/")

    # init the login manager with the login page
    login_manager = fk_lg.LoginManager(app)
    login_manager.login_view = "auth.login"

    # tell the login manager what class the users will be stored in
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.get_by_id(user_id)

    return app


def test_website():
    """
    Generates a Flask webserver using the test version of the WMGTSS database
    :return:
    """
    models.db.set_db(wmgtss_qa.DB_singleton("WMGTSS_QA_TEST", "wmg_admin", "warwickuni22"))
    return create_website()
