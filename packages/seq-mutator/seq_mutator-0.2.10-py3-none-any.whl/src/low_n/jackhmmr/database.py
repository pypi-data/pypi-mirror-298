from Bio import SeqIO
import sqlite3
import os
from tqdm import tqdm


class Database:
    def __init__(self, db_file):

        if not os.path.exists(db_file):
            self.conn = sqlite3.connect(db_file)
            self.create_table()
            return

        self.conn = sqlite3.connect(db_file)

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE hits
                     (id text, sequence text)''')
        self.conn.commit()

    def insert_fasta(self, fasta_path):
        c = self.conn.cursor()
        db = SeqIO.parse(fasta_path, "fasta")
        for record in tqdm(db):
            c.execute("INSERT INTO hits VALUES (?, ?)", (record.id, str(record.seq)))
        self.conn.commit()

    def get_sequences(self, ids):
        c = self.conn.cursor()
        query = "SELECT * FROM hits WHERE id IN ({})".format(", ".join(["?"] * len(ids)))
        return c.execute(query, ids).fetchall()

    def __del__(self):
        self.conn.close()

    def __str__(self):
        c = self.conn.cursor()
        # fetch first 3 entries and last 3 entries
        first = c.execute("SELECT * FROM hits LIMIT 3").fetchall()

        if self.entry_count() < 6:
            return f'{first}'

        last = c.execute("SELECT * FROM hits ORDER BY rowid DESC LIMIT 3").fetchall()
        return f'{first}\n...\n{last}'

    def entry_count(self):
        c = self.conn.cursor()
        return c.execute("SELECT COUNT(*) FROM hits").fetchone()[0]


