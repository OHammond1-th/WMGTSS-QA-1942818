import flask as fk
import flask_login as fk_lg
from .models import User
from . import wmgtss_qa


def create_website():

    from .auth import auth
    from .views import views

    app = fk.Flask(__name__)
    app.config["SECRET_KEY"] = "fesgfsges"

    app.register_blueprint(auth, url_prefix="/Auth")
    app.register_blueprint(views, url_prefix="/")

    wmgtss_qa.db.set_db(wmgtss_qa.DB_singleton("WMGTSS_QA", "web_client", "default"))

    login_manager = fk_lg.LoginManager(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    return app


def test_website():
    wmgtss_qa.db.set_db(wmgtss_qa.DB_singleton("WMGTSS_QA_TEST", "wmg_admin", "warwickuni22"))
    return create_website()
