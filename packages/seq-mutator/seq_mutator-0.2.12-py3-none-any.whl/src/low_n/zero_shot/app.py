import os
import pandas as pd
<<<<<<< HEAD
from typer import Typer, Argument, Option
=======
import numpy as np
from typer import Typer, Option
>>>>>>> dev
from typing import Annotated
from Bio import SeqIO

from .zero_shot_model import ZeroShotModel


app = Typer(help="CLI for zero shot prediction.")


@app.command(help="Generate the file with mutations on which the zero shot prediction is to be run.")
def init(
    project_name: Annotated[str, Option(help="The name of the project.", envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option('--path', '-p', help="The path to the projects. Default is 'data'. If not provided, the environment variable LOWN_PROJECTS_PATH is used.", envvar='LOWN_PROJECTS_PATH')] = 'data',
):
    project_dir = os.path.join(path, 'projects', project_name)
    if os.path.exists(os.path.join(project_dir, "point_mutation_data.csv")):
        print("dms file already exists.")
        return

    amino_acids = {'P': 0,'G': 1,'A': 2,'V': 3,'L': 4,'I': 5,'M': 6,'F': 7,'Y': 8,'W': 9,'C': 10,'S': 11,'T': 12,'N': 13,'Q': 14,'D': 15,'E': 16,'K':17,'R': 18,'H': 19}

    with open(os.path.join(project_dir, "target.fasta")) as fasta_file:
        wt_sequence = [str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")][0]

    output = pd.DataFrame(columns=['mutant'])

    for i in range(1,len(wt_sequence)):
        wt_residue = wt_sequence[i]
        for residue in amino_acids.keys():
            if residue==wt_residue:
                continue
            output.loc[len(output.index)]=wt_residue+str(i+1)+residue

    output.to_csv(os.path.join(project_dir, "point_mutation_data.csv"), index=False)


@app.command(help="Run zero shot prediction on the point_mutation_data.csv file. Uses the mutant-marginals scoring method, since it yielded the best results.")
def predict(
    esm_model: Annotated[str, Option('--model', '-m', help="The ESM model to use. It should be a valid Identifier for a huggingface ESM2 model or a path to a ESM2 Hugging Face checkpoint.")] = "facebook/esm2_t6_8M_UR50D",
    project_name: Annotated[str, Option(help="The name of the project.", envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option('--path', '-p', help="The path to the projects. Default is 'data'. If not provided, the environment variable LOWN_PROJECTS_PATH is used.", envvar='LOWN_PROJECTS_PATH')] = 'data',
    tokenizer: Annotated[str, Option('--tokenizer', '-t', help="The tokenizer to use. It should be a valid Identifier for a huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
    mutation_col: Annotated[str, Option('--mutation-col', help="Column with the mutations, labeled as 'AiB'")] = "mutant",
):
    project_dir = os.path.join(path, 'projects', project_name)
    df = pd.read_csv(os.path.join(project_dir, "point_mutation_data.csv"))
    with open(os.path.join(project_dir, "target.fasta")) as fasta_file:
        wt_sequence = [str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")][0]
    
    mutation_positions = list(df.apply(lambda row: int(row[mutation_col][1:-1]),1).unique())

    model = ZeroShotModel(esm_model, tokenizer, path)
    scores = model.predict_point_mutations(wt_sequence, mutation_positions)

    df[esm_model] = df.apply(
        lambda row: scores[mutation_positions.index(int(row[mutation_col][1:-1]))][row[mutation_col][-1]],
        axis=1
    )

    df.to_csv(os.path.join(project_dir, "point_mutation_data.csv"), index=False)


<<<<<<< HEAD
@app.command(help="Give out the n mutations with the highest zero shot score.")
=======
@app.command(help="Gives n mutations, half drawn from the top 10% prediced zero-shot variants and half from the bottom 90%.")
>>>>>>> dev
def trainingset(
    score_column: Annotated[str, Option(help="What column in point_mutation_data.csv should be used as the scores.")],
    project_name: Annotated[str, Option(help="The name of the project.", envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option('--path', '-p', help="The path to the projects. Default is 'data'. If not provided, the environment variable LOWN_PROJECTS_PATH is used.", envvar='LOWN_PROJECTS_PATH')] = 'data',
    n_variants: Annotated[int, Option(help="How many variants should be tested?")]=24,
    mutation_col: Annotated[str, Option('--mutation-col', help="Column with the mutations, labeled as 'AiB'")] = "mutant",
):
    project_dir = os.path.join(path, 'projects', project_name)
    df = pd.read_csv(os.path.join(project_dir, "point_mutation_data.csv"))
    assert score_column in df.columns, "Score column doesn't exist."

<<<<<<< HEAD
    df.nlargest(n_variants, score_column)[mutation_col].to_csv(os.path.join(project_dir, "zs_training_set.csv"), index=False)
=======
    rng = np.random.default_rng()
    percentile = np.percentile(df[score_column], 90)
    training_set = pd.concat([
        df[[mutation_col, score_column]].loc[rng.choice(df[df[score_column]>=percentile].index, int(np.ceil(n_variants/2)), replace=False)], 
        df[[mutation_col, score_column]].loc[rng.choice(df[df[score_column]<=percentile].index, int(np.floor(n_variants/2)), replace=False)]])
    training_set.to_csv(os.path.join(project_dir, "zs_training_set.csv"), index=False)
>>>>>>> dev
