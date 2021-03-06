import flask
import flask_login
app = flask.Flask(__name__)
app.secret_key = 'some secret'


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@app.before_request
def before_request():
#    app.logger.info("hello")
    # app.logger.info(flask_login.current_user)
    # app.logger.info(flask_login.current_user.is_authenticated)
    # app.logger.info(type(flask_login.current_user.is_authenticated))
    flask.g.userid = None
    if flask_login.current_user.is_authenticated:
        app.logger.info(flask_login.current_user.id)
        flask.g.userid = flask_login.current_user.id
    #     pass
        


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    password = request.form.get('password')
    # TODO: In this simple example we stored the password as plain text
    # TODO: update the example to use hashes password
    if password != users[email]['password']:
        return

    user = User()
    user.id = email

    return user


@app.route("/")
def main():
    return flask.render_template('main.html',
        title = "Flask Login Example",
    )

@app.route('/login', methods=['GET'])
def login_get():
    return flask.render_template('login.html',
        title = "Login",
    )


@app.route('/login', methods=['POST'])
def login():
    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return flask.render_template('protected.html',
        title = "Bad Login",
    ), 401

@app.route('/protected')
@flask_login.login_required
def protected():
    return flask.render_template('protected.html',
        title = "Protected",
        user = flask_login.current_user.id,
    )


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.render_template('logged_out.html',
        title = "Logged out",
    )

@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.render_template('unauthorized.html',
        title = "Unauthorized",
    ), 401
    