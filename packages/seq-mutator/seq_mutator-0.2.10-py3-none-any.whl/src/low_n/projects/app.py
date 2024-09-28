import os
from typer import Typer, Argument, Option
from typing import Annotated
from enum import Enum

from .utils import insert_target, insert_activities

app = Typer(help="LowN CLI to manage projects.")


class InsertionStrategy(str, Enum):
    link = "link"
    move = "move"
    copy = "copy"


@app.command(help="List all the projects in the given path.")
def list(
    path: Annotated[str, Option(help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data'
):

    if not os.path.exists(path):
        print("The path to the projects does not exist.")
        return

    project_path = os.path.join(path, 'projects')

    if not os.path.exists(project_path):
        os.makedirs(project_path)

    for project in os.listdir(project_path):
        print(project)


@app.command(help="Create a new project.")
def create(
    name: Annotated[str, Argument(help="The name of the project.")],
    activities: Annotated[str,
                          Option(help="The path to the activities csv file.")] = None,
    target: Annotated[str,
                      Option(help="The path to the target fasta file.")] = None,
    path: Annotated[str, Option(help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
    insert: Annotated[InsertionStrategy,
                      Option(help="Specifies how the specified file should be inserted"
                                  "into the project directory")] = InsertionStrategy.copy,
):
    if not os.path.exists(path):
        print("The path to the projects does not exist: ", os.path.abspath(path))
        return

    path = os.path.join(path, 'projects')

    if not os.path.exists(path):
        os.makedirs(path)

    project_path = os.path.join(path, name)
    if os.path.exists(project_path):
        print("The project already exists: ", os.path.abspath(project_path))
        return

    os.makedirs(project_path)
    print("Project created under: ", os.path.abspath(project_path))

    if activities:
        insert_activities(project_path, activities, insert)

    if target:
        insert_target(project_path, target, insert)


@app.command(help="Delete a project.")
def delete(
    name: Annotated[str, Argument(help="The name of the project.")],
    path: Annotated[str, Option(help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
):
    if not os.path.exists(path):
        print("The path to the projects does not exist.")
        return

    path = os.path.join(path, 'projects')

    project_path = os.path.join(path, name)
    if not os.path.exists(project_path):
        print("The project does not exist.")
        return

    # rm -rf
    os.system(f'rm -rf {project_path}')

    print(f'Project {name} deleted.')


if __name__ == "__main__":
    app()

