import subprocess


def search(max_iterations, target_fasta, db_fasta, results, num_threads):

    # create jackhmmer command
    cmd = ['jackhmmer', '-N', str(max_iterations), '--cpu', str(int(num_threads)),
           '--tblout', results, target_fasta, db_fasta]

    # run jackhmmer
    result = subprocess.run(cmd, check=True, capture_output=False, text=True)

    # unpack
    stdout = result.stdout
    stderr = result.stderr

    # decode if possible
    if stdout is not None:
        stdout = stdout.decode('utf-8')

    if stderr is not None:
        stderr = stderr.decode('utf-8')

    # return output
    return stdout, stderr


