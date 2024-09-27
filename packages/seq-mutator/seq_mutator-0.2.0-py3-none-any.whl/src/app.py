import os
from typer import Typer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from .shuffle.app import app as shuffle_app
from .low_n.app import app as low_n_app


app = Typer(help="unimuenster protein engineering toolbox")

app.add_typer(low_n_app, name="low-n")
app.add_typer(shuffle_app, name="shuffle")

if __name__ == "__main__":
    app()


