'''
main routine for plot module
'''
from egger.window import slide
from egger.utils import process
from egger.utils.errors import BadArgumentsError

def main(args):
    '''
    main routine for the plot module
        arguments:
            args: argsparse object from parser
        returns:
            None
    '''
    ### Get args -- move to parser
    annotation_filename = args.annotations
    gbk_filename = args.genbank
    window_info = args.window_size, args.step_size
    sw_output = args.sliding_window_output #os.path!
    sw_plot = args.sliding_window_plot #os.path!
    if sw_plot is None and sw_output is None: ## UPDATE FOR BAR CHART
        raise BadArgumentsError('No output specified. Specify either -swp or -swo.')
    ### Combine data from .annotation and .gbk ###
    proteins = process.process(annotation_filename, gbk_filename)
    records = {protein['record_name'] for protein in proteins if 'record_name' in protein}
    categories = process.get_categorys(proteins)
    ### Make frame plots for each record ###
    if sw_plot or sw_output:
        for record in records:
            window_data = slide.get_window_data(record, categories, proteins, window_info)
            #parse out slide.get_window_data and slide.slide_window
            if sw_plot:
                slide.plot_sliding_window(window_data, categories, sw_plot, record)
            if sw_output:
                slide.write_data(window_data, sw_output, record)
    print('egger is done!')
