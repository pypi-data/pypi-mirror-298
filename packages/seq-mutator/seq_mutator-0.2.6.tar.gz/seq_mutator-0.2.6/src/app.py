from .low_n.app import app as low_n_app
from typer import Typer
import os
from .shuffle.app import app as shuffle_app


def main():

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    current_dir = os.getcwd()
    env_path = os.path.join(current_dir, '.env')

    if os.path.exists(env_path):
        print(f'loading environment variables from {env_path}')
        with open(env_path) as f:
            for line in f:
                key, value = line.strip().split('=')
                os.environ[key] = value

    current_project = os.getenv('LOWN_CURRENT_PROJECT', 'default')
    os.environ['LOWN_CURRENT_PROJECT'] = current_project

    projects_path = os.getenv('LOWN_PROJECTS_PATH', 'data')
    projects_path = os.path.abspath(projects_path)
    os.environ['LOWN_PROJECTS_PATH'] = projects_path

    app = Typer(help="unimuenster protein engineering toolbox")

    app.add_typer(low_n_app, name="low_n")
    app.add_typer(shuffle_app, name="shuffle")

    app()
