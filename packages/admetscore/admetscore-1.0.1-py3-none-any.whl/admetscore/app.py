from argparse import RawTextHelpFormatter
from .models.BrowserHandler import *
from .models.Screening import *
from .models.Evaluate import * 
from .models.Splitter import*
from .models.Output import*
from .models.texts import*
import argparse
import os

def peso():
    evaluate_instance = Evaluate()
    evaluate_instance.json()
    with open('weights.json','r') as json_file:
        weights = json.load(json_file)
    
    return weights

weights = peso()
weights_note = f"{message_weights + json.dumps(weights, indent=4)}\n"

def main():
    
    global weights
    global weights_note

    parser = argparse.ArgumentParser(description=header,formatter_class=RawTextHelpFormatter, epilog=weights_note)
    parser.add_argument('-v','--version', action='version', version=version)

    parser.add_argument('-i','--sdf_file',type=str, help=sdf_input_file)
    parser.add_argument('-n', '--batch_number', type=int, default=299, help=batch_number_help)
    parser.add_argument('-ps', '--pharmit_score_docking', type=float, help=pharmit_score_docking_help)
    parser.add_argument('-t', '--best_hits_number', type=int, default=50, help=best_hits_number_help)
    parser.add_argument('--search',action='store_true', help=search)


    subparsers = parser.add_subparsers(dest='tool', help=description)

    # SPLIT PARSER:
    parser_split = subparsers.add_parser('split',description=header + split_description,formatter_class=RawTextHelpFormatter, help=split_help)
    parser_split.add_argument('-i', '--sdf_file', type=str, required=True, help=sdf_input_file)
    parser_split.add_argument('-n', '--batch_number', type=int, default=299, help=batch_number_help)
    parser_split.add_argument('-ps', '--pharmit_score_docking', type=float, help=pharmit_score_docking_help)

    # EVALUATE PARSER:
    parser_evaluate = subparsers.add_parser('evaluate',description=header + evaluate_description,formatter_class=RawTextHelpFormatter, help=evaluate_help, epilog=weights_note)
    parser_evaluate.add_argument('-i', '--csv_file', type=str, required=True, help=csv_input_file)
    parser_evaluate.add_argument('-s', '--sdf_batch_file', type=str, default=None, help=batch_number_help)
    parser_evaluate.add_argument('-t', '--best_hits_number', type=int, default=50, help=best_hits_number_help)

    args = parser.parse_args()

    if args.tool is None and args.sdf_file or args.search:
        process_auto(args.sdf_file, args.batch_number, args.pharmit_score_docking, args.best_hits_number, args.search)
    elif args.tool == 'split':
        split(args.sdf_file, args.batch_number, args.pharmit_score_docking)
    elif args.tool == 'evaluate':
        evaluate(args.csv_file,args.sdf_batch_file,args.best_hits_number)
    else:
        print(usage)

def split(sdf_file, batch_number, pharmit_score_docking):
    
    Splitter(verbose=True).split(sdf_file, batch_number, pharmit_score_docking)

def evaluate(csv_file,sdf_batch_file,best_hits_number):
    print(weights_note)
    Evaluate(verbose=True).evaluate_data(csv_file,sdf_batch_file,best_hits_number)
    

def process_auto(sdf_file,batch_number,pharmit_score_docking,best_hits_number,search):

    if sdf_file is not None and search == True:
        print(search_input_error)
        return

    if search == True:
        sdf_files = [file for file in os.listdir() if file.endswith('.sdf')]
        num_files = len(sdf_files)

        if len(sdf_files) == 0:
            print(search_error)
        else:
            print(weights_note)
            print(f'{num_files} files found that will be processed')
            for index, file in enumerate(sdf_files):
                Screening(verbose=True).screen(file, batch_number, pharmit_score_docking, best_hits_number)
                print(f'Processed file {index + 1} of {num_files}')
        return

    print(weights_note)
    
    Screening(verbose=True).screen(sdf_file,batch_number,pharmit_score_docking,best_hits_number)

if __name__ == '__main__':
    main()