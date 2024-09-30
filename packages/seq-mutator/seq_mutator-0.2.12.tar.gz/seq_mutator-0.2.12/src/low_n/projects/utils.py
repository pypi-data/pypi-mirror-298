import os
import pandas as pd
import shutil


def insert_file(path: str, file: str, type: str = 'link'):
    # check if the folder of path exists
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        print("The folder does not exist: ", os.path.abspath(folder))
        return

    if not os.path.exists(file):
        print("The file does not exist ", os.path.abspath(file))
        return

    target_path = os.path.abspath(path)
    file = os.path.abspath(file)

    # check if file already exists
    if os.path.exists(target_path):
        a = input('The file already exists. Do you want to overwrite it? [y/n]: ')
        if a != 'y':
            return
        os.remove(target_path)

    if type == 'link':
        os.symlink(file, target_path)
    elif type == 'move':
        shutil.move(file, target_path)
    elif type == 'copy':
        shutil.copy(file, target_path)
    else:
        print("Invalid type of insertion.")
        return


def insert_target(path, target_fasta, type):
    # check that file is a fasta file
    if not target_fasta.endswith('.fasta'):
        print("The target fasta file must be a fasta file.")
        return

    path = os.path.join(path, 'target.fasta')
    insert_file(path, target_fasta, type)

    print(f'Target fasta file inserted into {path}.')


def insert_activities(path, activities, type):
    # check that file is a csv
    if not activities.endswith('.csv'):
        print("The activities file must be a csv file.")
        return

    # check that csv contains the right columns
    try:
        df = pd.read_csv(activities)
        assert 'label' in df.columns
        assert 'sequence' in df.columns
    except Exception:
        print("The activities file must contain the columns 'label', 'protein' and 'sequence'.")
        return

    path = os.path.join(path, 'activities.csv')
    insert_file(path, activities, type)

    print(f'Activities file inserted into {path}.')


def insert_db(path, db_file, type):
    # check that file is a fasta file
    if not db_file.endswith('.fasta'):
        print("The database fasta file must be a fasta file.")
        return

    path = os.path.join(path, 'db.fasta')
    insert_file(path, db_file, type)

    print(f'Database fasta file inserted into {path}.')


