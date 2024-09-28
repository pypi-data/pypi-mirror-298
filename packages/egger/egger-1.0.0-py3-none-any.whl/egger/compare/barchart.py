'''
plot bar charts for egger
    functions:
        !!!
'''
from typing import List, Dict
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

def convert_counter_to_percentages(counters: List) -> List:
    '''
    Take a list of counters and convert each from raw values to percentage of total
        arguments: 
            counters:
                a list of counter objects
        returns:
            percentage_counters:
                a list of counters with values converted to percentages
    '''
    percentage_counters = []
    for counter in counters:
        total_values = sum(counter.values())
        percentages = {key: (value / total_values) * 100 for key, value in counter.items()}
        percentage_counters.append(percentages)
    return percentage_counters


def draw_barchart(labels: List, counters: List[Counter], categories: List, filename: str) -> None:
    '''
    Uses matplotlib to draw a bar chart from counter objects
        arguments:
            labels:
                the labels for the counter objects - must be in the same order!
            counters:
                a list of counter objects
            categories: 
                a list of the discrete categories to be plotted
            filename: 
                prefix for the .svg file
        returns:
            None
    '''
    data = np.array([[counter.get(category, 0) for category in categories] for counter in counters])
    # Set up parameters for the plot
    fig, ax = plt.subplots(figsize=(10, 6)) #maybe change the size?
    n_counters = len(counters)
    bar_width = 10 / (n_counters * 12) #adjust the bar width to the number of samples
    index = np.arange(len(categories))
    # Plot each counter
    for i in range(n_counters):
        ax.bar(index + i * bar_width, data[i], bar_width, label=labels[i]) #color=colors[i]
    # Add labels and titles
    ax.set_xlabel('COG Category')
    ax.set_ylabel('Count')
    ax.set_xticks(index + bar_width * (n_counters / 2 - 0.5))
    ax.set_xticklabels(categories)
    ax.legend(title="Source")
    # Save as svg
    plt.savefig(filename + '.svg') #add options

def plot_bar_chart(proteomes: List[Dict], categories, filename: str) -> None:
    '''
    plot the bar chart in plotly
        arguments: 
            proteomes:
                list of dictionaries containing the eggnog annotations from the proteomes
            categories:
                a list of the discrete categories from the COG categories counters
            filename:
                prefix to be used for output files
        returns:
            None
    '''
    labels = [proteome['name'] for proteome in proteomes]
    counters = [proteome['category_counts'] for proteome in proteomes]
    draw_barchart(labels, counters, categories, filename)
    percentage_counters = convert_counter_to_percentages(counters)
    draw_barchart(labels, percentage_counters, categories, filename + '_percentages')
