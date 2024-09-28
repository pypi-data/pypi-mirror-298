# extracTR

## Introduction

extracTR is a tool for extracting and analyzing tandem repeats from raw DNA sequences. It utilizes advanced algorithms to identify repetitive patterns in genomic data, providing valuable insights for researchers in genomics and bioinformatics.

## Features

- Efficient tandem repeat detection from raw sequencing data
- Support for paired-end FASTQ files
- Customizable parameters for fine-tuning repeat detection
- Output in easy-to-analyze CSV format
- Multi-threaded processing for improved performance

## Requirements

- Python 3.7 or later
- Jellyfish 2.3.0 or later

To install Jellyfish:

```bash
conda install -c bioconda jellyfish
```

## Installation

Install extracTR using pip:

```bash
pip install extracTR
```

## Usage

Before running extracTR, ensure that you have removed adapters from your sequencing reads. This is crucial to prevent contamination of predicted repeats with adapter sequences.

Basic usage:

```bash
extracTR -1 reads_1.fastq -2 reads_2.fastq -o output_prefix
```

Advanced usage with custom parameters:

```bash
extracTR -1 reads_1.fastq -2 reads_2.fastq -o output_prefix -t 64 -c 30 -k 25
```

Options:
- `-1, --fastq1`: Input file with forward DNA sequences in FASTQ format
- `-2, --fastq2`: Input file with reverse DNA sequences in FASTQ format
- `-o, --output`: Prefix for output files
- `-t, --threads`: Number of threads to use (default: 32)
- `-c, --coverage`: Coverage to use for indexing (default: 1)
- `-k, --k`: K-mer size to use for indexing (default: 23)

## Output

extracTR generates the following output files:
- `{output_prefix}.csv`: Main output file containing detected tandem repeats
- `{output_prefix}.sdat`: Intermediate file with k-mer frequency data
- Additional files for detailed analysis and debugging