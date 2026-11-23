import routes


def register_blueprint(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.search)
    app.register_blueprint(routes.temple)
    app.register_blueprint(routes.course)
    app.register_blueprint(routes.padawan)
    app.register_blueprint(routes.master)
    app.register_blueprint(routes.saber)
    app.register_blueprint(routes.species)