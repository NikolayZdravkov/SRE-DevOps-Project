import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config is not None:
        app.config.update(test_config)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Student  # noqa: F401

    from app.routes import api
    app.register_blueprint(api)

    app.logger.info("Flask app started")

    return app
