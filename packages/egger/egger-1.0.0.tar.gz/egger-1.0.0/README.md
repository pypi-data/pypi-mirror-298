# egger
a python package to plot results from eggnog-mapper

## Description

`egger` can plot COG functional annotations from eggnog-mapper annotation files.

The repository for eggnog-mapper can be found, [here](https://github.com/eggnogdb/eggnog-mapper).

It has two modes:
- `compare`: compares the correlation of COG categories across several genomes.
- `window`: plots sliding window plots of COG category distribution across a genome.

See below for usage examples.

## Installation

You can install egger with `pip`.

Either use the PyPI installation: `pip install egger`.

Or, clone this repository and install manually. 

`egger` only requires Python dependencies, which should be installed automatically. 

## Usage and Example Output
As described above, `egger` has two modes:

### compare

#### compare output
`egger compare` will calculate the correlation of COG category annotations across genomes and build a dendrogram-heatmap. 
It will write this as .svg file along with the raw data in .tsv formats. It can perform Spearman's rank (`-s`) or Pearson's (`-p`) correlation. 
It can also produce barcharts (`-b`). Use: `egger compare -h` for more information.

Here is an example using this repository's `example_data/outputs/compare_outputs` as the working directory:

`$ egger compare -b barchart -s spearmans -p pearsons ../../inputs/annotations/*`

#### compare output
These heatmaps can help identify relationships between genomes or other sequences. 

![Compare example output](https://github.com/drboothtj/egger/blob/main/example_data/outputs/compare_outputs/spearmans.svg)

### window

#### window usage
`egger window` will take eggnog-mapper annotations and plot them using a sliding window.
Please note, as eggnog-mapper annotations do not contain location data, the original genome used for the analysis is also required.
You will also need to define outputs with `-swo` or `-swp`. You can also modify the window and step size using. Use: `egger window -h` for more information.

Here is an example using this repository's `example_data/outputs/window_outputs` as the working directory:

`egger window -a ../../inputs/annotations/Lactococcus_lactis.annotations -g ../../inputs/genomes/Lactococcus_lactis.gb -swo output_ -swp plot_`

#### window output
This will produce two files:

1. `-swo` writes a .tsv file with the raw data used for plotting the sliding window.
2. `-swp` writes a .html file for an interactive plot of the sliding window data.

This analysis is particularly useful for finding regions of the genome that are dedicated to a specific function. In the example, *Lactococcus lactis* has three notable islands for the COG categories J, M and P (among others).
![example window output](https://github.com/drboothtj/egger/blob/main/example_data/outputs/window_outputs/plot_AP018499.png)

## Citation

Coming soon...

## Patch Notes
- v1.0.0 - Initial version
  
