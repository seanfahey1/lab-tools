#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import plotly.graph_objects as go
from Bio import SeqIO


def get_args():
    parser = argparse.ArgumentParser(
        description="Plots contig lengths from all input files, colored by source file"
    )
    parser.add_argument(
        "-i",
        "--input",
        nargs="+",
        required=False,
        help="Input .fasta file(s)",
    )
    return parser.parse_args()


def main():
    args = get_args()
    print(args.__dict__)

    fig = go.Figure()
    for file_path in args.input:
        file_name = Path(file_path).stem
        lengths = []
        headers = []
        with open(file_path, "r") as file:
            for record in SeqIO.parse(file, "fasta"):
                lengths.append(len(record.seq))
                headers.append(record.description)
        # TODO: add headers on hover
        # TODO: get blast result and split phage v. not-phage
        fig.add_trace(go.Box(y=lengths, boxpoints="all", pointpos=-1.3, jitter=0.1, name=file_name))
    fig.show()


if __name__ == "__main__":
    sys.exit(main())
