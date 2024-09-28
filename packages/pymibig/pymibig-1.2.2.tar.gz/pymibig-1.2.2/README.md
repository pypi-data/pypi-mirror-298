# pyMIBiG

A small tool to download, match and save target sequences from [MIBiG](https://mibig.secondarymetabolites.org/).

## Usage

Download the available package of `pyMIBiG` and execute `pymibig <target>`
where target is the term you wanto to search in MIBiG database.

By default `pyMIBiG` will fetch sequences with complete cluster data and
complete information.

You may change that using optional aguments passed along with the `<target>`:

```{bash}
usage: pymibig [-h] [-c {complete,incomplete,Unknown}] [-m] target

positional arguments:
  target                Search term to query in database

options:
  -h, --help            show this help message and exit
  -c {complete,incomplete,Unknown}, --completeness {complete,incomplete,Unknown}
                        Loci completeness.
  -m, --minimal         Minimal annotation.
```

On first execution `pyMIBiG` will download the database files from
[MIBiG](https://mibig.secondarymetabolites.org/download) and save locally,
so an internet connection will be needed, after that it can be used offline.

As for this release `pymibig` will download from MIBiG
**Version 3.1 (October 7th, 2022)** of:
- [Metadata](https://dl.secondarymetabolites.org/mibig/mibig_json_3.1.tar.gz)
in compressed format, including several JSON files;
- [Nucleotide](https://dl.secondarymetabolites.org/mibig/mibig_gbk_3.1.tar.gz)
sequences of the biosynthetic gene clusters in compressed format, including
several GBK files;
- [Amino acid sequence translations](https://dl.secondarymetabolites.org/mibig/mibig_prot_seqs_3.1.fasta)
of all genes from MIBiG entries are also available in a single compressed FASTa file.

## License

`pyMiBiG` is distributed under the terms of the [LGPL 3.0](https://spdx.org/licenses/LGPL-3.0-or-later.html) license.
