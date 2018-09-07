import os

from app import create_app


def init_app():
    if os.environ.get('env') is None:
        env = 'dev' # default environment
    else:
        env = os.environ.get('env')

    return create_app(env.upper())


application = init_app()
