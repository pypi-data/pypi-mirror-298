from typer import Typer, Option
from typing import Annotated
import os
from enum import Enum


app = Typer(help="Evotune CLI")


class EvaluationStrategy(str, Enum):
    steps = "steps"
    epoch = "epoch"


@app.command(help="Train an ESM model on a dataset of sequences.")
def train(
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
                    Option(help="The evaluation strategy to use")] = EvaluationStrategy.steps,
    tokenizer: Annotated[str, Option(help="The tokenizer to use."
                                     "It should be a valid Identifier for a"
                                     "huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
    save_total_limit: Annotated[int, Option(
        help="The maximum number of checkpoints to keep.")] = 10,
    path: Annotated[str, Option('--path', '-p',
                                help="The path to the projects. Default is 'data'. If not "
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
    max_evalue: float = 10.0,
    run: str = 'test',
    lora=False,
):

    from .train import train as evotune_train

    project_dir = os.path.join(path, 'projects', project_name)
    target_fasta = os.path.join(project_dir, "target.fasta")
    sequences_csv_path = os.path.join(project_dir, "sequences.csv")
    runs_dir = os.path.join(project_dir, 'runs')
    output_dir = os.path.join(runs_dir, run)

    if not os.path.exists(sequences_csv_path):
        print("The sequences csv file does not exist. Please insert it manually or run"
              "the parse command in the search CLI. File: ", sequences_csv_path)
        return

    if not os.path.exists(target_fasta):
        print("The target fasta file does not exist. Please insert it manually.")
        return

    if not os.path.exists(runs_dir):
        os.makedirs(runs_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("starting run: ", run)

    evotune_train(sequences_csv_path, esm_model, max_length, epochs,
                  batch_size, target_fasta, output_dir, take, eval,
                  tokenizer, save_total_limit, path, max_evalue, lora=lora)


if __name__ == "__main__":
    app()



