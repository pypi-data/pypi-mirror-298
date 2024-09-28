"""
Get arguments from user.
"""

import argparse


def get_args() -> argparse.Namespace:
    '''
    Recieve user arguments and return them to main function.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Search term to query in database',
        type=str)
    parser.add_argument('-c', '--completeness', help='Loci completeness.',
        type=str, choices=['complete', 'incomplete', 'Unknown'],
        default='complete')
    parser.add_argument('-m', '--minimal', action="store_true",
                        help='Minimal annotation.')
    return parser.parse_args()
