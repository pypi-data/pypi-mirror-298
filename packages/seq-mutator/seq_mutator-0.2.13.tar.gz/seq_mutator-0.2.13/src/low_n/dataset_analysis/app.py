import os
import pandas as pd
from typer import Typer, Option
from typing import Annotated
from Bio import SeqIO
from scipy.stats import spearmanr
from tqdm import tqdm
import pickle

from ..topmodel.topmodel import Topmodel


app = Typer(help="CLI for analysing the methods on datasets with experimental data.")


@app.command(help="Take the training set given in some csv file and the scores from another csv to train a new topmodel.")
def create_topmodel_from_training_set(
    score_col: Annotated[str, Option(help="Column in the point mutation data with the scores.")],
    esm_model: Annotated[str, Option(
        help="The ESM model to use. It should be a valid Identifier for a huggingface ESM2 model or a path to a ESM2 Hugging Face checkpoint.")] = "facebook/esm2_t6_8M_UR50D",
    tokenizer: Annotated[str, Option(
        '--tokenizer', '-t', help="The tokenizer to use. It should be a valid Identifier for a huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
    project_name: Annotated[str, Option(
        help="The name of the project.", envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option(
        '--path', '-p', help="The path to the projects. Default is 'data'. If not provided, the environment variable LOWN_PROJECTS_PATH is used.", envvar='LOWN_PROJECTS_PATH')] = 'data',
    training_mutation_col: Annotated[str, Option(
        help="Column in the training set with the mutations, labeled as 'AiB'.")] = "mutant",
    score_mutation_col: Annotated[str, Option(
        help="Column in the score data with the mutations, labeled as 'AiB'.")] = "mutant",
    strategy_prefix: Annotated[str, Option(
        help="Prefix of the training_set.csv, which contains the mutations labeled as 'AiB'.")] = "zs_",
):
    project_dir = os.path.join(path, 'projects', project_name)
    with open(os.path.join(project_dir, "target.fasta")) as fasta_file:
        wt_sequence = [str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")][0]
    scores = pd.read_csv(os.path.join(project_dir, "point_mutation_data.csv"))[
        [score_mutation_col, score_col]]
    training_set = pd.read_csv(os.path.join(project_dir, strategy_prefix +
                               "training_set.csv"))[training_mutation_col]
    activities = pd.merge(training_set, scores, "left", left_on=training_mutation_col,
                          right_on=score_mutation_col, suffixes=(False, False))
    if activities[score_col].isna().sum() > 0:
        print("Warning: " + str(activities[score_col].isna().sum()) +
              " scores are missing. Dropping those variants from the training set.")
        activities.dropna(subset=score_col, inplace=True)
    activities["sequence"] = activities.apply(lambda row: point_mutation_to_sequence(
        row[training_mutation_col], wt_sequence), axis=1)
    activities.rename(columns={score_col: "label"}, inplace=True)

    topmodel_path = os.path.join(project_dir, strategy_prefix + "topmodel.pkl")
    activities_csv = os.path.join(project_dir, strategy_prefix + "activities.csv")
    activities.to_csv(activities_csv, index=False)

    topmodel = Topmodel(esm_model, topmodel_path, tokenizer, path)
    topmodel.train(activities_csv)
    topmodel.save()


@app.command(help="Score the dataset with a specific topmodel")
def rescore_dms(
    esm_model: Annotated[str, Option(
        help="The ESM model to use. It should be a valid Identifier for a huggingface ESM2 model or a path to a ESM2 Hugging Face checkpoint.")] = "facebook/esm2_t6_8M_UR50D",
    tokenizer: Annotated[str, Option(
        '--tokenizer', '-t', help="The tokenizer to use. It should be a valid Identifier for a huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
    project_name: Annotated[str, Option(
        help="The name of the project.", envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option(
        '--path', '-p', help="The path to the projects. Default is 'data'. If not provided, the environment variable LOWN_PROJECTS_PATH is used.", envvar='LOWN_PROJECTS_PATH')] = 'data',
    mutation_col: Annotated[str, Option(
        help="Column in the score data with the mutations, labeled as 'AiB'.")] = "mutant",
    strategy_prefix: Annotated[str, Option(
        help="Prefix of the topmodel.pkl, marking which training set creation strategy was used.")] = "zs_",
    batch_size: Annotated[int, Option(
        help="If a GPU with enough VRAM is available, a larger batch size can reduce computation time. Should be a power of 2.")] = 1,
    measurement_col: Annotated[str, Option(
        help="Column in the point mutation data with the measured scores.")] = None,
    zero_shot_col: Annotated[str, Option(
        help="Column in the point mutation data with the zero shot scores.")] = None
):
    project_dir = os.path.join(path, 'projects', project_name)
    with open(os.path.join(project_dir, "target.fasta")) as fasta_file:
        wt_sequence = [str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")][0]
    topmodel_path = os.path.join(project_dir, strategy_prefix + "topmodel.pkl")
    topmodel = Topmodel(esm_model, topmodel_path, tokenizer, path, load=True)
    df = pd.read_csv(os.path.join(project_dir, "point_mutation_data.csv"))
    n_mutants = df.shape[0]
    for i in tqdm(range(0, n_mutants // batch_size)):
        batch = [point_mutation_to_sequence(
            mutation, wt_sequence) for mutation in df[mutation_col].iloc[i * batch_size:i * batch_size + batch_size]]
        scores = topmodel.predict(batch)
        df.loc[i * batch_size:i * batch_size + batch_size - 1, strategy_prefix[:-1]] = scores
    if n_mutants % batch_size > 0:
        batch = [point_mutation_to_sequence(
            mutation, wt_sequence) for mutation in df[mutation_col].iloc[batch_size * (n_mutants // batch_size):]]
        scores = topmodel.predict(batch)
        df.loc[batch_size * (n_mutants // batch_size):, strategy_prefix[:-1]] = scores
    df.to_csv(os.path.join(project_dir, "point_mutation_data.csv"), index=False)
    if measurement_col is not None and zero_shot_col is not None:
        print("Spearman correlation for the rescored mutations is " + str(spearmanr(df[measurement_col], df[strategy_prefix[:-1]], nan_policy="omit")) + ", compared to " + str(
            spearmanr(df[measurement_col], df[zero_shot_col], nan_policy="omit")) + " for the zero shot prediction.")


@app.command(help="To experiment with different topmodel settings, only compute the sequence representations once.")
def store_hidden_representations(
    model_suffix: Annotated[str, Option(help="Differentiate representations for different esm models.")],
    esm_model: Annotated[str, Option(
        help="The ESM model to use. It should be a valid Identifier for a huggingface ESM2 model or a path to a ESM2 Hugging Face checkpoint.")] = "facebook/esm2_t6_8M_UR50D",
    tokenizer: Annotated[str, Option(
        '--tokenizer', '-t', help="The tokenizer to use. It should be a valid Identifier for a huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
    project_name: Annotated[str, Option(
        help="The name of the project.", envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option(
        '--path', '-p', help="The path to the projects. Default is 'data'. If not provided, the environment variable LOWN_PROJECTS_PATH is used.", envvar='LOWN_PROJECTS_PATH')] = 'data',
    mutation_col: Annotated[str, Option(
        help="Column in the score data with the mutations, labeled as 'AiB'.")] = "mutant",
    already_seq: Annotated[str, Option(help="Format of the mutations.")] = None
):
    project_dir = os.path.join(path, 'projects', project_name)
    with open(os.path.join(project_dir, "target.fasta")) as fasta_file:
        wt_sequence = [str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")][0]
    df = pd.read_csv(os.path.join(project_dir, "point_mutation_data.csv"))[mutation_col]
    topmodel = Topmodel(esm_model, None, tokenizer, path)
    if already_seq:
        df["hidden_rep"] = df.to_frame().apply(
            lambda row: topmodel._get_hidden_states(row[mutation_col]), axis=1)
    else:
        df["hidden_rep"] = df.to_frame().apply(lambda row: topmodel._get_hidden_states(
            point_mutation_to_sequence(row[mutation_col], wt_sequence)), axis=1)
    pickle.dump(df, open(os.path.join(project_dir, "hidden_reps_" + model_suffix + ".pkl"), "wb"))


@app.command(help="Use this to add the whole sequences to the activities.csv file, in case it only has them in 'AiB' format.")
def add_sequence_mutations(
    project_name: Annotated[str, Option(
        help="The name of the project.", envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option(
        '--path', '-p', help="The path to the projects. Default is 'data'. If not provided, the environment variable LOWN_PROJECTS_PATH is used.", envvar='LOWN_PROJECTS_PATH')] = 'data',
    mutation_col: Annotated[str, Option(
        help="Column in the score data with the mutations, labeled as 'AiB'.")] = "mutant",
    score_col: Annotated[str, Option(help="Column with the scores.")] = None,
):
    project_dir = os.path.join(path, 'projects', project_name)
    with open(os.path.join(project_dir, "target.fasta")) as fasta_file:
        wt_sequence = [str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")][0]
    activities = pd.read_csv(os.path.join(project_dir, "activities.csv"))
    activities["sequence"] = activities.apply(
        lambda row: point_mutation_to_sequence(row[mutation_col], wt_sequence), axis=1)
    if score_col:
        activities.rename(columns={score_col: "label"}, inplace=True)
    activities.to_csv(os.path.join(project_dir, "activities.csv"), index=False)


@app.command(help="")
def score_with_random_training_sets(

):
    print("hi")


def point_mutation_to_sequence(mutation, wt_sequence):
    index = int(mutation[1:-1]) - 1
    new_residue = mutation[-1]
    return wt_sequence[:index] + new_residue + wt_sequence[index:]


def sequence_to_point_mutations(mt_sequence, wt_sequence):
    indices = [i for i in range(len(wt_sequence)) if mt_sequence[i] != wt_sequence[i]]
    if len(indices) == 0:
        print("They're the same sequence :(")
        return None
    elif len(indices) == 1:
        return wt_sequence[indices[0]] + str(indices[0] + 1) + mt_sequence[indices[0]]
    elif len(indices) > 1:
        print("Multiple mutations not yet implemented. Oops...")
        return None


def get_hidden_rep(hidden_rep_df: pd.DataFrame, mutation, mutation_col="mutant"):
    return hidden_rep_df.loc[hidden_rep_df[mutation_col] == mutation]["hidden_rep"]
