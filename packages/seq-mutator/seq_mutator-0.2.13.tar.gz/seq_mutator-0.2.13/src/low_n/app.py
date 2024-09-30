# from .dataset_analysis.app import app as da_app
from .database.app import app as database_app
from .zero_shot.app import app as zs_app
from .directed_evolution.app import app as de_app
from .projects.app import app as projects_app
from .topmodel.app import app as topmodel_app
from .jackhmmr.app import search_and_parse
from .evotuning.app import train, EvaluationStrategy

from typer import Typer, Option, Argument
from typing import Annotated


app = Typer(help="LowN Protein Engineering CLI.")

app.add_typer(topmodel_app, name="topmodel")
app.add_typer(projects_app, name="projects")
app.add_typer(de_app, name="directed_evolution")
app.add_typer(zs_app, name="zero_shot")
app.add_typer(database_app, name="databases")


@app.command(help="First build the database, then perform a jackhmmer search "
             "and parse the results.")
def search(
    db: Annotated[str, Argument(help="The name of the database to use")],
    project_name: Annotated[str,
                            Argument(help="The name of the project.",
                                     envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option('--path', '-p',
                                help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
    n: Annotated[int, Option('--num-iters', '-n', help="Maximum jackhmmr Iterations.")] = 5,
    max_evalue: Annotated[float, Option(
        '--max-evalue', '-e', help="Maximum evalue to filter the hits.")] = 10.,
    num_threads: Annotated[int, Option(
        '--num-threads', '-t', help="Number of threads to use.")] = 4,
):
    search_and_parse(db, project_name, path, n, max_evalue, num_threads)


@app.command(help="Train an ESM model (Finetune) on a dataset of sequences.")
def evotune(
    esm_model: Annotated[str, Option('--model', '-m',
                                     help="The ESM model to use. It should be a valid"
                                     "Identifier for a huggingface ESM2 model or a path to a ESM2"
                                     " Hugging Face checkpoint.")] = "facebook/esm2_t6_8M_UR50D",
    project_name: Annotated[str,
                            Option(help="The name of the project.",
                                   envvar='LOWN_CURRENT_PROJECT')] = 'default',
    max_length: Annotated[int, Option(help="The maximum length of the sequences.")] = 1024,
    batch_size: Annotated[int, Option('--batch-size', '-b', help="The batch size to use.")] = 2,
    epochs: Annotated[int, Option(
        '--epochs', '-e', help="The maximum number of epochs to train for.")] = 1,
    take: Annotated[float, Option(
        '--take', '-t', help="The fraction of the dataset to use.")] = 1.0,
    eval: Annotated[EvaluationStrategy,
                    Option(help="The evaluation strategy to use")] = EvaluationStrategy.epoch,
    tokenizer: Annotated[str, Option(help="The tokenizer to use."
                                     "It should be a valid Identifier for a"
                                     "huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
    save_total_limit: Annotated[int, Option(
        help="The maximum number of checkpoints to keep.")] = 10,
    path: Annotated[str, Option('--path', '-p',
                                help="The path to the projects. Default is 'data'. If not "
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
    max_evalue: Annotated[float, Option('--max-evalue', '-me',
                                        help="The maximum e-value to filter the hits.")] = 10.,
    lora: Annotated[bool, Option(help="Whether to use LORA or not.")] = False,
    run: Annotated[str, Option(help="The ru to use")] = 'test',
):

    train(esm_model, project_name, max_length, batch_size, epochs, take, eval,
          tokenizer, save_total_limit, path, max_length, run=run, lora=lora)


if __name__ == "__main__":
    app()
