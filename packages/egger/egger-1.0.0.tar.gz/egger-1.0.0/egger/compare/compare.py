'''
main routine for compare module
    functions:
        !!!
'''
from collections import Counter
from typing import Dict, List

from egger.utils.process import process, get_categorys
from egger.utils.errors import BadArgumentsError
from egger.compare import barchart, rank

def check_args(args):
    '''
    Check for valid input and outputs
    '''
    #check enough samples for correlations
    if args.spearmans or args.pearsons:
        if len(args.annotations) < 3:
            raise BadArgumentsError(
                'Must select at least three files when performing correlation analysis.'
                )

def get_proteomes(annotation_files: List) -> List[Dict]:
    '''
    takes a list of eggnog annotation files and 
    returns a list of dictionaries containing the name of the file and the annotations
    as a dictionary
        arguments: 
            annotation_files: list of paths to eggnog annotation files
        returns:
            proteomes:
                list of dictionaries containing formatted annotations
    '''
    proteomes = []
    for file in annotation_files:
        proteins = process(file)
        proteome = {
            'name' : file,
            'proteins' : proteins
        }
        proteomes.append(proteome)
    return proteomes

def count_categories(proteome):
    ''' return a count of each category'''
    all_categories = ''.join([protein['COG_category'] for protein in proteome['proteins']])
    counts = Counter(all_categories)
    return counts

def get_category_counts(proteomes):
    '''
    count COG categories for each annotation file
    '''
    for proteome in proteomes:
        proteome['category_counts'] = count_categories(proteome)
    return proteomes

def main(args):
    '''
    main routine for the compare functions
    '''
    check_args(args)
    proteomes = get_proteomes(args.annotations)
    categories = sorted(
        get_categorys([protein for proteome in proteomes for protein in proteome['proteins']])
        )
    proteomes = get_category_counts(proteomes)
    if args.barchart:
        barchart.plot_bar_chart(proteomes, categories, args.barchart)
    if args.spearmans:
        rank.rank(proteomes, categories, args.spearmans, 'spearmans')
    if args.pearsons:
        rank.rank(proteomes, categories, args.pearsons, 'pearsons')
