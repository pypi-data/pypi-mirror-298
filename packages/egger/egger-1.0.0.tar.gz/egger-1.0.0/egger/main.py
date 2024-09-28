'''
egger: visualise eggnog-mapper data

functions:
    !!!!!!!!
'''
from egger.window import window
from egger.compare import compare
from egger.parser import parser


## add logging
## add error
## figureout which categories we can chart
## finish parser - fix arguments to binary
## sort out architecture
## seriously clean up code
## make plots pretty
## specify an output directory

def main() -> None:
    '''
    main routine for egger
        arguments:
            annotation_filename: path to .annotations file
            gbk_filename: path to .gbk file
            annotation_type: annotation header to plot
        returns:
            None
    '''
    args = parser.parse_args()
    if args.command == 'window':
        window.main(args)
    elif args.command == 'compare':
        compare.main(args)
    