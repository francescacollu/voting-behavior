import os
import argparse

from ScrapingCamera import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', required=True)
    parser.add_argument('--legislature', required=True)
    parser.add_argument('--min_index', required=False, type=int)
    parser.add_argument('--max_index', required=False, type=int)
    parser.add_argument('--folder_name', required=True)
    args = parser.parse_args()    
    congressmen_list = open('Congressmen_list.txt', 'r').read()
    congressmen_list = congressmen_list.split('\n')
    year=args.year
    legislature=args.legislature
    if args.min_index:
        min_index = args.min_index
    else:
        min_index = 0
    if args.max_index:
        max_index = args.max_index
    else:
        max_index = len(congressmen_list)
    if not os.path.exists(args.folder_name):
        os.mkdir(args.folder_name)
    else:
        raise RuntimeError('The specified folder '+args.folder_name+' already exists.')
    
    run_scraping(congressmen_list, args.folder_name, year, legislature, min_index, max_index)

if __name__ == '__main__':
    main()