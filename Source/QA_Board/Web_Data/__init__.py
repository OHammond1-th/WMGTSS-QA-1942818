import flask as fk
import flask_login as fk_lg
from .models import User


def create_website():

    from .views import views

    app = fk.Flask(__name__)
    app.config["SECRET_KEY"] = "fesgfsges"

    app.register_blueprint(views, url_prefix="/")

    login_manager = fk_lg.LoginManager(app)
    login_manager.blueprint_login_views("views.login")

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    return app
