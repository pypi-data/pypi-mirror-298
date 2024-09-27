


# HEADER
header = "LAMBDA - Laboratório Multiusuário e Analise de Dados\n\nJúlio César Albuquerque Xavier\nEdson Luiz Folador"

# TOOL DESCRIPTION
description = "Admetscore is a software that automates the comparison of ADMET analyses between molecules. It accepts molecules in .sdf files and performs analyses on ADMETlab 3.0, assigning scores from 0 to 10 for ADMET properties based on the site's classification. The tool ranks the molecules by their overall score and generates a spreadsheet with IDs, SMILES, scores, and ADMET details, using colors to indicate the quality of the analyzed parameters, making the results easier to interpret.\n\n"

# WEIGHT MESSAGE
message_weights = "\nNote: The weights used in the analysis were those below. If you want to change them, change the values in the weights.json file created in the folder where the script is running.\n"


# PARAMETER HELP
####################################
sdf_input_file = '(required): sdf file path with molecules to be analyzed.\n''\n'

csv_input_file = '(required): csv file path with admet analysis from admetlab3.0 website.\n''\n'

batch_number_help = '(optional): Use this parameter to specify the number of molecules in each partition. By default, the tool will create partitions with 299 molecules.\n''\n'

pharmit_score_docking_help = '(optional): Use this parameter to partition the sdf from the specified docking score. This will reduce the number of partitions created, since by default the entire SDF file is partitioned.\n''\n'

best_hits_number_help = '(optional): Specify the number of top-scoring molecules you want to view. The spreadsheet will be non-cumulative and a separate file will be created in the score folder. By default, a spreadsheet is created with the 50 best results\n''\n'

search = '(optional): Use this parameter to search for sdf files in the current directory. If the parameter is used, the tool will search for sdf files in the current directory and process them automatically.\n''\n'

####################################


# SPLIT PARSER
split_description = '\n''\nThis component allows the splitting of an SDF file into multiple smaller files. Each SDF file contains 299 molecules by default, though this number can be adjusted via a parameter. This splitting is necessary for screening in ADMETLab 3.0. Users can then upload each file to the ADMETLab site and download the results, proceeding to the second component of the tool, evaluate.'

split_help = split_description+"""
  ↳  More information about the parameters: admetscore split -h
                                       """

# EVALUATE PARSER 
evaluate_description = '\n''\n''After splitting the SDF file and screening each partition with ADMETlab 3.0, you can provide this module with one partition of the SDF file along with its corresponding CSV result file from ADMETlab 3.0. The module will then generate a cumulative spreadsheet that compiles the ADMET analysis for each molecule in the partition. Each molecule is assigned a score from 0 to 10, where a higher score indicates better performance in the ADMET analysis. The spreadsheet will accumulate results from each partition you process, consolidating all analyses in a single document.'

evaluate_help = evaluate_description+"""
  ↳  More information about the parameters: admetscore score -h
                                         """

# NOTICES: 
usage = 'usage: admetscore [-h] [-v] -i SDF_FILE [-n BATCH_NUMBER] [-ps PHARMIT_SCORE_DOCKING] [-t BEST_HITS_NUMBER] {split,evaluate}'
search_input_error = "\nPlease, choose between processing a single file or search mode.\nTo use search mode, use only the optional parameters along with the -s parameter.\n"
search_error = "\nNo SDF files found in the current directory.\n"

version ="""
░█▀█░█▀▄░█▄█░█▀▀░▀█▀░█▀▀░█▀▀░█▀█░█▀▄░█▀▀░░░▀█░░░░░▄▀▄░░░░▀█░
░█▀█░█░█░█░█░█▀▀░░█░░▀▀█░█░░░█░█░█▀▄░█▀▀░░░░█░░░░░█/█░░░░░█░
░▀░▀░▀▀░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░░▀▀▀░▀░░░▀░░▀░░▀▀▀"""