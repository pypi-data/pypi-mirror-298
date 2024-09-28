from typer import Typer, Option, Argument
from typing import Annotated
import os

from ..jackhmmr.database import Database


app = Typer(help="add, list and build databases used for lowN protein engineering")


@app.command(help="list all the databases")
def list(
    path: Annotated[str, Option('--path', '-p',
                                help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
):
    databases_path = os.path.join(path, "databases")

    if not os.path.exists(databases_path):
        os.makedirs(databases_path)

    for database in os.listdir(databases_path):
        print(database)


@app.command(help="add a new database fasta file")
def add(
    name: Annotated[str, Argument(help="The name of the database.")],
    db: Annotated[str, Argument(help="The path to the database fasta file.")],
    path: Annotated[str, Option('--path', '-p',
                                help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
):
    databases_path = os.path.join(path, "databases")

    if not os.path.exists(databases_path):
        os.makedirs(databases_path)

    db_name = name
    db_folder_path = os.path.join(databases_path, db_name)

    if os.path.exists(db_folder_path):
        print("The database already exists: ", db_folder_path)
        return

    os.mkdir(db_folder_path)
    db_path = os.path.join(db_folder_path, 'db.fasta')
    os.rename(db, db_path)
    print("Database added under: ", db_path)


@app.command(help="build a database")
def build(
    db: Annotated[str, Argument(help="The path to the database fasta file.")],
    path: Annotated[str, Option('--path', '-p',
                                help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
):
    fasta_path = os.path.join(path, "databases", db, 'db.fasta')
    db_path = os.path.join(path, "databases", db, 'db.sqlite')

    if not os.path.exists(fasta_path):
        print("The database does not exist: ", fasta_path)
        return

    print("Building sequences batabase")
    db = Database(db_path)
    db.insert_fasta(fasta_path)
    print("Created Database")
    print("Database has {} entries".format(db.entry_count()))
    del db




