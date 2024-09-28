import os

from .parse_results import JackHMMERParser
from .search import search as jackhmmer_search


def parse(
    db_sqlite_path: str,
    project_name: str,
    path: str,
    max_evalue: float
):
    hmmer_file = os.path.join(path, 'projects', project_name, "hmmer.out")
    output_csv = os.path.join(path, 'projects', project_name, "sequences.csv")

    if not os.path.exists(hmmer_file):
        print("The jackhmmer output file does not exist.")
        return

    print("Parsing jackhmmer output file")

    parser = JackHMMERParser(hmmer_file, db_sqlite_path)
    parser.create_csv(output_csv, max_evalue)


def search(
    db_fasta_path: str,
    project_name: str,
    path: str,
    n: int,
    num_threads: int
):
    target_fasta = os.path.join(path, 'projects', project_name, "target.fasta")
    results = os.path.join(path, 'projects', project_name, "hmmer.out")

    target_fasta = os.path.abspath(target_fasta)
    results = os.path.abspath(results)

    if not os.path.exists(target_fasta):
        print("The target fasta file does not exist. Please insert it manually if not"
              "done so at creation of the project.")
        return

    print("Running jackhmmer search")

    jackhmmer_search(n, target_fasta, db_fasta_path, results, num_threads)


def search_and_parse(
    db: str,
    project_name: str,
    path: str,
    n: int,
    max_evalue: float,
    num_threads: int,
):

    db_path = os.path.join(path, 'databases', db)
    if not os.path.exists(db_path):
        print("The database does not exist. Choose one of:")
        print(os.listdir(os.path.join(path, 'databases')))
        return
    db_fasta_path = os.path.join(db_path, 'db.fasta')

    if not os.path.exists(db_fasta_path):
        print("The database fasta file does not exist. Please add it first.")
        return

    sqlite_path = os.path.join(db_path, 'db.sqlite')

    if not os.path.exists(sqlite_path):
        print("The database is not built. Please build it first.")
        return

    search(db_fasta_path, project_name, path, n, num_threads)
    parse(sqlite_path, project_name, path, max_evalue)


if __name__ == "__main__":
    app()
