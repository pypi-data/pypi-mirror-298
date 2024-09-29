from ftplib import FTP
import os
from typing import List, Optional
from io import BufferedWriter

import rich.progress as prog
from rich.progress import Progress

def quit_connection(message: Optional[str], ftp: FTP):
    if message is not None:
        print(message)
    # quit() can throw an exception if ftp server responds with error
    try:
        ftp.quit()
    except Exception as e:
        # This is more like a log message, just something to know that the ftp QUIT command failed.
        # This is not a critical error, so we can just close the connection with ftp.close().
        print("ftp QUIT command failed, trying to close the connection with ftp.close()", e)
        ftp.close()

def ena_download(sra_accession: str, output_dir: str) -> List[str]:
    # small argument validations for the sra_accession parameter
    if (not sra_accession.isalnum()):
        print("Invalid SRA accession number. Please provide a valid SRA accession number.")
        return

    ftp = FTP('ftp.sra.ebi.ac.uk')
    ftp.login()

    prefix = sra_accession[:6]
    last_digit_of_accession = sra_accession[len(sra_accession)-1]

    # handles different format of directory for shorter accession numbers
    if (len(sra_accession) < 10):
        directory = f'/vol1/fastq/{prefix}/{sra_accession}'
    else:
        directory = f'/vol1/fastq/{prefix}/00{last_digit_of_accession}/{sra_accession}'

    try:
        ftp.cwd(directory)
    except Exception:
        quit_connection("Failed to access the directory for the provided accession number.\n"
                 "Please ensure that the accession number is correct and the corresponding\n"
                 "FASTQ files are available on ENA.", ftp)
        return

    file_names = ftp.nlst()
    if (file_names == []):
        quit_connection("No files found for the given SRA accession number.", ftp)
        return
    
    if (output_dir != None):
        if not os.path.exists(output_dir):
            quit_connection("Directory does not exist.", ftp)
            return

    output_files = []

    with create_progress_bar() as progress:
        for file_name in file_names:
            size = ftp.size(f"{file_name}")
            task = progress.add_task(f"Downloading {file_name}", total=size)
            
            # build local file path
            if (output_dir != None):
                local_file_path = os.path.join(output_dir, file_name)
            else:
                local_file_path = file_name

            output_files.append(local_file_path)
            
            # skip download if the entire file already exists
            if os.path.isfile(local_file_path) and os.path.getsize(local_file_path) == size:
                progress.update(task, advance=size)
                continue

            with open(local_file_path, 'wb') as f:
                callback = lambda data : write_file(f, data, progress, task)
                ftp.retrbinary(f"RETR {file_name}", callback)
            
    quit_connection(None, ftp)
    return output_files


def write_file(file: BufferedWriter, data: bytes, progress: Progress, task: prog.TaskID):
    '''
    Writes data to a file buffer and updates the task for a progress bar
    '''
    file.write(data)
    progress.update(task, advance=len(data))


def create_progress_bar() -> Progress:
    '''
    Creates a progress bar configured for ena downloading.
    '''
    return Progress(prog.SpinnerColumn(),
                    prog.TextColumn("[progress.description]{task.description}"),
                    prog.BarColumn(),
                    prog.DownloadColumn(),
                    prog.TaskProgressColumn(),
                    prog.TimeElapsedColumn())
