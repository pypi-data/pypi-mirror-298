'''Main entrypoint for egger'''

from egger import main

def entrypoint():
    '''Entry point for setup.py'''
    try:
        main.main()
    except Exception as error:
        print(error)        
