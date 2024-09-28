'''
produces sliding window graph and data
    functions: !!!
'''
from typing import Dict, List
import plotly.graph_objects as go
from egger.utils import io

def plot_sliding_window(
    window_data: Dict, categories: List[str], filename: str, record: str
    ) -> None:
    '''
    make and write plotly graph object from traces
        arguments: 
            window_data: List of graph objects for each category to be plotted
        returns:
            None
    '''
    #figure_title = f'Distribution of XXX in XXX.' ## add to figure and fix
    figure = go.Figure()
    for category in categories:
        x_values = list(window_data.keys())
        y_values = [window_data[x_value][category] for x_value in x_values]
        trace = go.Scatter(x=x_values, y=y_values, mode="lines", name=category)
        figure.add_trace(trace)
    figure.write_html(f'{filename}{record}.html')
    ##update figure with legends etc.

def write_data(contents: Dict, output: str, record: str) -> None:
    '''
     convert sliding window data into a list of lines for writing
        arguments: 
            contents: a dictionary containing window data
        returns:
            None
    '''
    lines = []
    heading = [' ']
    heading.extend({inner_key for key in contents for inner_key in contents[key].keys()})
    lines.append(heading)
    for key in contents.keys():
        line = [key]
        values = list(contents[key].values())
        line.extend(values)
        lines.append(line)
    io.write_to_tsv(f'{output}{record}.tsv', lines)

def slide_window(
    proteins: List[Dict], categories: List[str],
    window_size: int, step_size: int
    ): #add return hint
    '''
    applies a sliding window to datapoints
        data_points: list of tuples describing the protein midpoint and annotation
        categories: a list of categories to plot
    returns:
        window_data: a list of tuples containing the window midpoint and the ...
    '''
    window_position = 0
    maximum_position = max([protein['stop'] for protein in proteins])
    ## ADD CHECK WINDOW SIZE FUNCTON
    if window_size is None:
        window_size = maximum_position/100
        window_size = max(window_size, 5000)
    if step_size is None:
        step_size = window_size/2
    ###
    window_data = {}
    while window_position < maximum_position:
        window_end = window_position + window_size
        window_midpoint = window_position + window_size / 2
        #print(
        #    'window start: %s, window_end: %s, window_midopoint; %s'
        #    % (window_position, window_end, window_midpoint)
        #    )
        #print(maximum_position)
        window_data[window_midpoint] = {category: 0 for category in categories}
        for protein in proteins:
            #check if missing or counted twice in between
            if window_position < protein['start'] < window_end:
                try:
                    window_data[window_midpoint][protein['COG_category']] += 1
                ##except key error split
                except KeyError:
                    for character in protein['COG_category']:
                        window_data[window_midpoint][character] += 1
        window_position += step_size
    return window_data


def get_window_data(record, categories, proteins, window_info) -> None:
    '''
    main routine for slide
        arguments:
            record:
                the current record being analysed
            categories:
                the total unique categories as a set
            proteins:
                the list of protein dictionaries
            window_info:
                window and step size from args parse
        retruns: 
            window_data:
                !!!
    '''
    record_proteins = [protein for protein in proteins if protein['record_name'] == record]
    window_data = slide_window(record_proteins, categories, window_info[0], window_info[1])
    return window_data
