import os
import pandas as pd
from Bio import SeqIO
from typer import Typer, Argument, Option
from typing import Annotated


app = Typer(help="Evotune CLI for the top model.")


@app.command(help="Predict the label for a given sequence or sequences.")
def predict(
    target: Annotated[str, Argument(help="The argument is either a protein sequence or a path to"
                                    "a csv or fasta file containing sequences.")],
    esm_model: Annotated[str, Option(
        '--model', '-m',
        help="The ESM model to use. It should be a valid Identifier for a"
        "huggingface ESM2 model or a path to a ESM2 Hugging Face checkpoint.")] = "facebook/esm2_t6_8M_UR50D",
    project_name: Annotated[str, Option(help="The name of the project.",
                                        envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option('--path', '-p',
                                help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
    tokenizer: Annotated[str, Option('--tokenizer', '-t',
                                     help="The tokenizer to use."
                                     "It should be a valid Identifier for a"
                                     "huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
):
    from .topmodel import Topmodel
    if os.path.isfile(target):

        is_csv = target.endswith(".csv")
        is_fasta = target.endswith(".fasta")

        if is_csv:
            df = pd.read_csv(target)
            target = df["sequence"].to_list()
        elif is_fasta:
            with open(target) as fasta_file:
                target = [str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")]
        else:
            raise ValueError("File must be a csv or fasta file.")

    topmodel = os.path.join(path, 'projects', project_name, "topmodel.pkl")

    if not os.path.exists(topmodel):
        print("The topmodel does not exist. Please train it first.")
        return

    topmodel = Topmodel(esm_model, topmodel, tokenizer, path, load=True)
    predictions = topmodel.predict(target)
    print(predictions)


@app.command(help="Train the top model.")
def train(
    esm_model: Annotated[str, Option(
        '--model', '-m',
        help="The ESM model to use. It should be a valid Identifier for a"
        "huggingface ESM2 model or a"
        "path to a ESM2 Hugging Face checkpoint.")] = "facebook/esm2_t6_8M_UR50D",
    project_name: Annotated[str, Option(help="The name of the project.",
                                        envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option('--path', '-p',
                                help="The path to the projects. Default is 'data'. If not"
                                "provided, the environment variable LOWN_PROJECTS_PATH is used.",
                                envvar='LOWN_PROJECTS_PATH')] = 'data',
    tokenizer: Annotated[str, Option('--tokenizer', '-t',
                                     help="The tokenizer to use."
                                     "It should be a valid Identifier for a"
                                     "huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
):

    from .topmodel import Topmodel
    topmodel_path = os.path.join(path, 'projects', project_name, "topmodel.pkl")
    activities_csv = os.path.join(path, 'projects', project_name, "activities.csv")

    if not os.path.exists(activities_csv):
        print("The activities csv file does not exist. Please insert it manually")
        return

    topmodel = Topmodel(esm_model, topmodel_path, tokenizer, path)
    topmodel.train(activities_csv)
    topmodel.save()


if __name__ == "__main__":
    app()




