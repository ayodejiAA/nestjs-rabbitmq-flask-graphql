from flask import Flask
from flask_graphql import GraphQLView

from .schema import schema
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "NestJS - RabbitMQ - Flask-Graphql Example"

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # for having the GraphiQL interface
        )
    )

    return app
