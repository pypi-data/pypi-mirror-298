"""
Save the matched amino acid sequences in FASTa format.
"""

import sys
import gzip
from rich.progress import track
from Bio import SeqIO
from src.pymibig.console import console
from src.pymibig.constants import AA

def save_aa(target: str, access_codes: str, basedir: str,
                   completeness: str, minimal: bool) -> None:
    '''
    Save the desired amino acis sequences in a FASTa file.

    Arguments:
    target -- target taxon name
    access_codes -- codes list to retrieve from database
    basedir -- main module path
    completeness -- Cluster completeness from mibig
    mininal -- annotation status from mibig
    '''
    desired_seqs: list = []

    try:
        with gzip.open(f'{basedir}/src/db/{AA}', mode='rt') as gz:
            total = len(list(SeqIO.parse(gz, 'fasta')))

        with gzip.open(f'{basedir}/src/db/{AA}', mode='rt') as gz:
            for seq in track(SeqIO.parse(gz, 'fasta'),
            description='[bold green]Saving amino acid sequences...[/bold green]',
            total=total):
                if any(code in seq.id for code in access_codes):
                    desired_seqs.append(seq)

        SeqIO.write(
            desired_seqs,
            f'{target}_aa_{completeness}{"_minimal" if minimal else ""}.fasta',
            'fasta')
    except PermissionError:
        console.print(
            '[bold red]Permission to read directory or write file denied.[/bold red]'
            )
        sys.exit()
