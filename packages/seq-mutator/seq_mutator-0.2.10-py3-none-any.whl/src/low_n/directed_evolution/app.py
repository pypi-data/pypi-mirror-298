import os
import pandas as pd
import numpy as np
from Bio import SeqIO
import copy
from typer import Typer, Option
from typing import Annotated
from tqdm import tqdm


app = Typer(help="CLI for directed evolution.")

@app.command(help="Generate a number of directed evolution trajectories.")
def run(
    esm_model: Annotated[str, Option('--model', '-m', help="The ESM model to use. It should be a valid Identifier for a huggingface ESM2 model or a path to a ESM2 Hugging Face checkpoint.")] = "facebook/esm2_t6_8M_UR50D",
    project_name: Annotated[str, Option(help="The name of the project.", envvar='LOWN_CURRENT_PROJECT')] = 'default',
    path: Annotated[str, Option('--path', '-p', help="The path to the projects. Default is 'data'. If not provided, the environment variable LOWN_PROJECTS_PATH is used.", envvar='LOWN_PROJECTS_PATH')] = 'data',
    tokenizer: Annotated[str, Option('--tokenizer', '-t', help="The tokenizer to use. It should be a valid Identifier for a huggingface ESM2 model.")] = "facebook/esm2_t6_8M_UR50D",
    n_iterations: Annotated[int, Option(help="How many steps should be performed for each trajectory?")]=20,
    batch_size: Annotated[int, Option(help="How many trajectories should be started in parallel? Make sure there is enough VRAM available to evaluate the chosen ESM model with the given batch size!")]=1,
    trust_radius: Annotated[int, Option(help="At how many positions are the mutants allowed to differ from the wildtype?")]=7,
    temperature: Annotated[float, Option(help="")]=0.1,
    batch_name: Annotated[str, Option(help="Relevant for name of the resulting file.")]="b0_",
):

    from ..topmodel.topmodel import Topmodel

    amino_acids = {'P': 0,'G': 1,'A': 2,'V': 3,'L': 4,'I': 5,'M': 6,'F': 7,'Y': 8,'W': 9,'C': 10,'S': 11,'T': 12,'N': 13,'Q': 14,'D': 15,'E': 16,'K':17,'R': 18,'H': 19}

    project_dir = os.path.join(path, 'projects', project_name)
    with open(os.path.join(project_dir, "target.fasta")) as fasta_file:
        wt_sequence = [str(record.seq) for record in SeqIO.parse(fasta_file, "fasta")][0]

    topmodel = Topmodel(esm_model, os.path.join(project_dir, "topmodel.pkl"), tokenizer, path, load=True)

    n_initial_mutations = np.random.poisson(2)+1

    current_proposal = []
    mutated_positions = []
    for i in range(batch_size):
        mutated_positions.append(set())
        current_proposal.append(introduce_mutations(wt_sequence, wt_sequence, mutated_positions[i], n_initial_mutations, trust_radius, amino_acids))
    current_score = topmodel.predict(current_proposal)

    results = []
    for i in range(batch_size):
        results.append([[current_proposal[i],current_score[i],"yes"]])
    rng = np.random.default_rng()
    for i in tqdm(range(0,n_iterations)):
        new_candidate = []
        new_mutated_positions = copy.deepcopy(mutated_positions)
        for j in range(0,batch_size):
            new_candidate.append(introduce_mutations(current_proposal[j], wt_sequence, new_mutated_positions[j], rng.poisson(rng.random()*1.5)+1, trust_radius, amino_acids)) # Draw from pois(mu) with mu drawn uniformly from [1,2.5]
        new_score = topmodel.predict(new_candidate)
        for j in range(0,batch_size):
            acceptance_prob = min(1,np.exp((new_score[j]-current_score[j])/temperature))
            if rng.random()>acceptance_prob:
                results[j].append([new_candidate[j],new_score[j],"no"])
            else:
                results[j].append([new_candidate[j],new_score[j],"yes"])
                current_proposal[j] = new_candidate[j]
                current_score[j] = new_score[j]
                mutated_positions[j] = new_mutated_positions[j]

    trajectory_dir = os.path.join(project_dir, "trajectories")
    if not os.path.exists(trajectory_dir):
        os.mkdir(trajectory_dir)
    df = pd.DataFrame()
    for i in range(batch_size):
        df[["sequence_"+str(i),"score_"+str(i),"accepted_"+str(i)]] = pd.DataFrame(results[i])
    df.to_csv(os.path.join(trajectory_dir, "directed_evolution_"+batch_name+".csv"), index=False)


def introduce_mutations(sequence, wt_sequence, mutated_positions, num_mutations, trust_radius, amino_acids):
    rng = np.random.default_rng()
    num_mutations = min(num_mutations, trust_radius)
    if trust_radius>=len(mutated_positions)+num_mutations:
        positions = rng.choice(range(1,len(sequence)), num_mutations, replace=False)
        mutated_positions.update(positions)
    elif trust_radius==len(mutated_positions):
        positions = rng.choice(list(mutated_positions), num_mutations, replace=False)
    else:
        n_new_positions = trust_radius-len(mutated_positions)
        positions = rng.choice(range(1,len(sequence)), n_new_positions, replace=False)
        mutated_positions.update(positions)
        np.append(positions, rng.choice(list(mutated_positions), num_mutations-n_new_positions, replace=False))

    for i in set(positions):
        amino_set = list(amino_acids.keys())
        amino_set.remove(sequence[i])
        substitution = rng.choice(amino_set)
        sequence = sequence[:i] + substitution + sequence[i+1:]
        if substitution==wt_sequence[i]:
            mutated_positions.remove(i)
    return sequence
