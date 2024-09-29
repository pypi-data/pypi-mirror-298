import subprocess
import os
from typing import List

import rich.progress as prog
from rich.progress import Progress

def get_zcat_command() -> str:
    '''
    Checks if zcat or gzcat exist on the machine, returns whichever is functional!
    '''
    try:
        subprocess.check_output("zcat --help", shell=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.check_output("gzcat --help", shell=True)
        except subprocess.CalledProcessError:
            raise Exception("Error working with fastq.gz file! zcat or gzcat not found on this machine!")
        else:
            return "gzcat"
    else:
        return "zcat"
    

def check_jellyfish():
    '''
    Checks if jellyfish is installed. Raises an exception if not.
    '''
    try:
        subprocess.check_output("jellyfish --help", shell=True)
    except subprocess.CalledProcessError:
        raise Exception("Jellyfish not found! Please install Jellyfish to count kmers!")


def try_command(command: str, err_msg: str):
    '''
    Runs and command and if there's an error, raises an exception with the provided error message.
    '''
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"{err_msg}{e}")


def fastq_to_kmer_counts(file_paths: List[str],
                         k: int,
                         output_dir: str = "",
                         threads: int = 10, 
                         hash_size: int = 100_000_000) -> str:
    '''
    Takes a path to a 'fastq' or zipped `fastq.gz' file and uses Jellyfish
    to count the provided number of kmers of length 'k'.

    Returns the local path to the output counts file.
    '''
    check_jellyfish()

    # Use the accession number as the base name
    base_path = f"{output_dir}/{os.path.basename(file_paths[0].replace('_1', ''))}"

    # Modify the file extension to .jf for the output
    jf_file = base_path.replace('.fastq', f'_{k}.jf').replace('.gz', '')

    # The base command for kmer counting
    count_command = f"jellyfish count -m {k} -s {hash_size} -C -t {threads} -o {jf_file}"

    # modifies the base command depending on if the files are zipped or not
    if file_paths[0].endswith('.fastq.gz'):
        zcat_command = get_zcat_command()
        count_command = f"{zcat_command} {' '.join(file_paths)} | {count_command} /dev/fd/0"
    else:
        count_command = f"{count_command} {' '.join(file_paths)}"

    # Run count and dump jellyfish commands
    with create_progress_bar() as progress:
        task = progress.add_task(f"Counting {k}-mers...", total=None)

        try_command(count_command, err_msg="Error running Jellyfish count: ")

        counts_file = jf_file.replace(".jf", ".counts")
        dump_command = f"jellyfish dump -c {jf_file} > {counts_file}"

        try_command(dump_command, err_msg="Error running Jellyfish dump: ")
        progress.update(task, total=1, advance=1)
    
    return counts_file

def create_progress_bar() -> Progress:
    '''
    Returns a progress bar configured for k-mer counting progress.
    '''
    return Progress(prog.SpinnerColumn(),
                    prog.TextColumn("[progress.description]{task.description}"),
                    prog.BarColumn(),
                    prog.TimeElapsedColumn())