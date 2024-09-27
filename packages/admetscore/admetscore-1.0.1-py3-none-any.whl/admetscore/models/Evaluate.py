import importlib.resources as pkg_resources
from .Output import *
from .Merge import *
import pandas as pd
import numpy as np 
import json
import os

class Evaluate:
   
    def __init__(self, verbose = False): # ok
        self.verbose = verbose

    def __log(self, message: str): # ok
        if self.verbose:
            print(message)

    @staticmethod
    def json(): # ok
        """
        This function loads the weights from the 'weights.json' file located in the 'admetscore' package and saves it in the current working directory as 'weights.json'.
        If the 'weights.json' file does not exist in the current working directory, it creates a new file and saves the weights in it.
        """
        try:
            with pkg_resources.open_text('admetscore', 'weights.json') as json_file:
                weights = json.load(json_file)
        except: # For testing in the development environment
            with open('admetscore/weights.json') as json_file:
                weights = json.load(json_file)

        new_json_path = os.path.join(os.getcwd(), 'weights.json')
        
        if not os.path.exists(new_json_path):
            with open(new_json_path, 'w') as new_json_file:
                json.dump(weights, new_json_file, indent=4)
        else:
            pass

    @staticmethod
    def __replace_interval(value, intervals, values): # ok
        """
        Replace a given value with a corresponding value from a list based on intervals.
        """
        for interval, replaced_value in zip(intervals, values):
            if interval[0] <= value <= interval[1]:
                return replaced_value
        return value

    @staticmethod
    def __replace_string(value, string, value1, value2): # ok
        return value1 if value == string else value2
    
    @staticmethod
    def __normalize_values(value): # ok
        """
        Normalize the given value.
        """
        try:
            if value <= 1.0:
                return float(value * 1000)
            return value
        except TypeError:
            print(f"Valor inválido encontrado: {value} (tipo: {type(value)})")
            raise  # Re-levanta o erro para manter a pilha de rastreamento
    
    @staticmethod
    def __rename(df): # ok
        """
        Renames the columns of the given DataFrame by replacing hyphens (-) and periods (.)
        with underscores (_) for better compatibility and ease of use. Hyphens and periods can cause issues when accessing DataFrame columns using dot notation or when performing certain operations.To avoid these issues, this function replaces them with underscores.
        """
        df = df.rename(columns={
            'cl-plasma': 'cl_plasma',
            't0.5': 't_0_5',
            'MCE-18': 'MCE_18',
            })
        return df

    def __replace_values(self, df, columns, intervals, values): # ok
        """
        Replaces values in specified columns of a DataFrame based on given intervals and corresponding replacement values.
        """
        replace = lambda x: self.__replace_interval(pd.to_numeric(x, errors='coerce'), intervals, values)
        for col in columns:
            df[col] = df[col].apply(replace)
        return df

    def score(self, df):

        self.json()

        with open('weights.json','r') as json_file:
            weights = json.load(json_file)

        df = self.__rename(df)

        try:
            df.drop('molstr',axis=1,inplace=True)
        except:
            pass

        df.replace('Invalid Molecule', np.nan, inplace=True)
        df = df.dropna(how='all', axis=1) 
        df_original = df.copy()

        new_cols_to_move = ['SCORE', 'ABSORTION', 'DISTRIBUTION', 'TOXICITY', 'TOX21_PATHWAY', 'METABOLISM', 'TOXICOPHORE_RULES', 'EXCRETION', 'MEDICINAL_CHEMISTRY']

        # Only columns with the same parameters are in the list:
    
        # Absorption
        absorption_columns = ['PAMPA', 'pgp_inh', 'pgp_sub', 'hia', 'f20', 'f30', 'f50'] # Caco2 and MDCK IS THE FOLLOWING INCLUDED IN THE GROUP SUM AND AVERAGE.
        

        # Distribution
        distribution_columns = ['OATP1B1', 'OATP1B3', 'BCRP', 'BSEP', 'BBB', 'MRP1'] # PPB, Fu and logVDss IS THE FOLLOWING INCLUDED IN THE GROUP SUM AND AVERAGE.

        # Toxicity
        toxicity_columns = ['hERG', 'hERG-10um', 'DILI', 'Ames', 'ROA', 'FDAMDD', 'SkinSen', 'Carcinogenicity', 'EC', 'EI', 'Respiratory', 'H-HT', 'Neurotoxicity-DI', 'Ototoxicity', 'Hematotoxicity', 'Nephrotoxicity-DI', 'Genotoxicity', 'RPMI-8226', 'A549', 'HEK293']

        # The Environmental Toxicity group does not have an empirical decision in the admetlab3.0 documentation, so it was not considered in the analysis.

        # Tox21
        tox21_columns = ['NR-AhR', 'NR-AR', 'NR-AR-LBD', 'NR-Aromatase', 'NR-ER', 'NR-ER-LBD', 'NR-PPAR-gamma', 'SR-ARE', 'SR-ATAD5', 'SR-HSE', 'SR-MMP', 'SR-p53']

        # Metabolism
        metabolism_columns = ['CYP1A2-inh', 'CYP1A2-sub', 'CYP2C19-inh', 'CYP2C19-sub', 'CYP2C9-inh', 'CYP2C9-sub', 'CYP2D6-inh', 'CYP2D6-sub', 'CYP3A4-inh', 'CYP3A4-sub', 'CYP2B6-inh', 'CYP2B6-sub', 'CYP2C8-inh', 'LM-human']

        # Toxicophore
        toxicophore_columns = ['NonBiodegradable', 'NonGenotoxic_Carcinogenicity', 'SureChEMBL', 'Skin_Sensitization', 'Acute_Aquatic_Toxicity', 'Genotoxic_Carcinogenicity_Mutagenicity','FAF-Drugs4 Rule']

        # Medicinal Chemistry
    
        # NPscore is not included in the analysis because it is a parameter that is not calculated for all molecules.
        

        medicinal_chemistry_columns_str = ['Alarm_NMR', 'BMS', 'Chelating', 'PAINS']
        medicinal_chemistry_columns_float_divergent = ['gasa', 'QED', 'Synth', 'Fsp3', 'MCE_18', 'Lipinski', 'Pfizer', 'GSK', 'GoldenTriangle']
        medicinal_chemistry_columns_float_similar = ['Aggregators', 'Fluc', 'Blue_fluorescence', 'Green_fluorescence', 'Reactive', 'Promiscuous']
        medicinal_chemistry = medicinal_chemistry_columns_str + medicinal_chemistry_columns_float_divergent + medicinal_chemistry_columns_float_similar

        # The excretion group is not listed because the only two members of the group have different parameters, and are calculated without the need for a list.

        # normalization
        to_normalize = ['caco2','PPB', 'Fu','logVDss','cl_plasma', 't_0_5', 'QED', 'Synth', 'Fsp3', 'MCE_18']
        normalize = absorption_columns + distribution_columns + toxicity_columns + tox21_columns + metabolism_columns + medicinal_chemistry_columns_float_similar + to_normalize

        for coluna in normalize:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
        
        for coluna in normalize:
            try:
                df[coluna] = df[coluna].apply(self.__normalize_values)
            except TypeError as e:
                print(f"Erro na coluna: {coluna}")
                raise e  # Re-levanta o erro para interromper a execução


        # The score is calculated based on parameter classification (green, yellow, red) per ADMETscore documentation.(https://admetlab3.scbdd.com/explanation/#/)
        # Each group is allocated 10 points, which are distributed among its parameters: green gets full points, yellow gets half, and red gets none.
        # We calculate the average to get the group's score, then a weighted average across groups.
        # The weights are defined in the weights.json file, created after running the script for the first time in the desired folder, making it possible to change the weights
        # The final score ranges from 0 to 10, with higher scores indicating better performance in the ADMET analysis.
    

        # calculation of columns that have equal check intervals
        common_intervals = [(0, 300), (300, 700), (700, 1000)]
        replacement_values = {
            tuple(absorption_columns): [1.111111111, 0.55, 0.0],
            tuple(distribution_columns): [1.111111111, 0.55, 0.0], 
            tuple(toxicity_columns): [0.5, 0.25, 0.0],
            tuple(tox21_columns): [0.833333333, 0.41, 0.0],
            tuple(metabolism_columns): [0.714285714, 0.35, 0.0],
            tuple(medicinal_chemistry_columns_float_similar):[0.5263157895, 0.26, 0.0],
        }        
        for columns, values in replacement_values.items():
            df = self.__replace_values(df, columns, common_intervals, values)

        # Dealing with columns that are str
        for col in toxicophore_columns:
            df[col] = df[col].apply(self.__replace_string, args=("['-']", 1.428571429, 0))

        for col in medicinal_chemistry_columns_str:
            df[col] = df[col].apply(self.__replace_string, args=("['-']", 0.5263157895, 0))

        # Calculation of columns of different parameters
        df = (
            df.assign(
                caco2=pd.to_numeric(df['caco2'], errors='coerce').apply(lambda x: 1.111111111 if x > -5150 else 0),
                MDCK=pd.to_numeric(df['MDCK'], errors='coerce').apply(lambda x: 1.111111111 if x > 2e-6 else 0),

                PPB=pd.to_numeric(df['PPB'], errors='coerce').apply(lambda x: 1.111111111 if x <= 90 else 0),
                Fu=pd.to_numeric(df['Fu'], errors='coerce').apply(lambda x: 1.111111111 if x >= 5 else 0),
                logVDss=pd.to_numeric(df['logVDss'], errors='coerce').apply(lambda x: 1.111111111 if 40 <= x <= 200 else 0),

                cl_plasma=pd.to_numeric(df['cl_plasma'], errors='coerce').apply(lambda x: 5 if 0 <= x <= 5 else (2.5 if 5 < x <= 15 else 0)),
                t_0_5=pd.to_numeric(df['t_0_5'], errors='coerce').apply(lambda x: 5 if x > 8 else (2.5 if 1 <= x <= 8 else 0)),

                Lipinski=pd.to_numeric(df['Lipinski'], errors='coerce').apply(lambda x: 0.5263157895 if x == 0 else 0),
                Pfizer=pd.to_numeric(df['Pfizer'], errors='coerce').apply(lambda x: 0.5263157895 if x == 0 else 0),
                GSK=pd.to_numeric(df['GSK'], errors='coerce').apply(lambda x: 0.5263157895 if x == 0 else 0),
                GoldenTriangle=pd.to_numeric(df['GoldenTriangle'], errors='coerce').apply(lambda x: 0.5263157895 if x == 0 else 0),
                
                gasa=pd.to_numeric(df['gasa'], errors='coerce').apply(lambda x: 0.5263157895 if x == 1 else 0),
                QED=pd.to_numeric(df['QED'], errors='coerce').apply(lambda x: 0.5263157895 if x > 670 else (0.26 if 490 <= x <= 670 else 0)),
                Synth=pd.to_numeric(df['Synth'], errors='coerce').apply(lambda x: 0.5263157895 if x <= 6000 else 0),
                Fsp3=pd.to_numeric(df['Fsp3'], errors='coerce').apply(lambda x: 0.5263157895 if x >= 420 else 0),
                MCE_18=pd.to_numeric(df['MCE_18'], errors='coerce').apply(lambda x: 0.5263157895 if x >= 45000 else 0),
            ))

        # sum of columns
        new_cols = pd.DataFrame({
            'ABSORTION': df[absorption_columns + ['caco2','MDCK']].sum(axis=1, skipna=True), #
            'DISTRIBUTION': df[['PPB', 'Fu','logVDss'] + distribution_columns].sum(axis=1, skipna=True), #
            'TOXICITY': df[toxicity_columns].sum(axis=1, skipna=True), 
            'TOX21_PATHWAY': df[tox21_columns].sum(axis=1, skipna=True), 
            'METABOLISM': df[metabolism_columns].sum(axis=1, skipna=True), 
            'TOXICOPHORE_RULES': df[toxicophore_columns].sum(axis=1, skipna=True), 
            'EXCRETION': df[['cl_plasma', 't_0_5']].sum(axis=1, skipna=True), 
            'MEDICINAL_CHEMISTRY': df[medicinal_chemistry].sum(axis=1, skipna=True) 
        })

        df = pd.concat([df, new_cols], axis=1)

        # calculates the average with the weights
        df['SCORE'] = (df['ABSORTION'] * weights['ABSORTION'] +
                        df['DISTRIBUTION'] * weights ['DISTRIBUTION'] +
                        df['TOXICITY'] * weights ['TOXICITY'] +
                        df['TOX21_PATHWAY'] * weights ['TOX21_PATHWAY'] +
                        df['METABOLISM'] * weights['METABOLISM'] +
                        df['TOXICOPHORE_RULES'] * weights ['TOXICOPHORE_RULES'] +
                        df['EXCRETION'] * weights['EXCRETION'] +
                        df['MEDICINAL_CHEMISTRY'] * weights['MEDICINAL_CHEMISTRY']) / sum(weights.values())
        
        df = pd.merge(df_original, df[['smiles'] + new_cols_to_move], on='smiles', how='left')

        new_cols = new_cols_to_move + ['smiles'] + [col for col in df.columns if col not in new_cols_to_move and col not in ['smiles']]
        
        df = df[new_cols]
        
        df[new_cols_to_move] = df[new_cols_to_move].round(2)
    
        try:
            df.drop('molstr',axis=1,inplace=True)
        except:
            pass
        
        df = self.__rename(df)

        df.replace('Invalid Molecule', np.nan, inplace=True)
        df = df.dropna(how='all', axis=1) 

        for coluna in normalize:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
        for coluna in normalize:
            df[coluna] = df[coluna].apply(self.__normalize_values)


        return df

    def evaluate_data(self,csv_file:str,sdf_file:str,best_hits_number:int):
        """ 
        
        **Ranks the best molecules based on an admet analysis**
        
        This function takes an SDF file containing the molecules and a CSV file with ADMET analysis results for each molecule. The function ranks the molecules based on their performance in each component of the analysis, assigns specific weights to each analysis group, and calculates an overall score for each molecule ranging from 0 (worst performance) to 10 (best performance).
        
        **Parameters**
        ----------
        csv_file : str
            Path to the CSV file containing ADMET analysis results.
    
        sdf_file : str
            Path to the SDF file containing molecular structures.

        best_hits_number : int
            Number of top-performing molecules to include in the final output.

        **Returns**
        -------
        None
            The function saves the results in scoreadmet.xlsx file, and there is also a spreadsheet with only the best molecules as an output.
        
        **Notes**
        -----
        The score for each molecule is calculated based on the weighted sum of its performance in the ADMET components. 
        
        **Examples**
        --------
        >>> score('admet_results.csv', 'molecules.sdf')
        >>> score('admet_results.csv', 'molecules.sdf', 10)
        """
        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo CSV {csv_file} não encontrado.")

        df = self.score(df)
        first_prop_name = None
        if sdf_file is not None:
            df,first_prop_name = Merge().extract(df,sdf_file)
            done_sdf_file = sdf_file.replace('.sdf', '_done.sdf')
            os.rename(sdf_file, done_sdf_file)
            

        Output(self.verbose).output(df,best_hits_number,first_prop_name)
        ok_csv_file = csv_file.replace('.csv', '_ok.csv')
        os.rename(csv_file, ok_csv_file)

    def folder_handler(self,best_hits_number):
        csv_directory = 'admetlab3_files'
        sdf_directory = 'sdf'
        for csv_file in os.listdir(csv_directory):
            if csv_file.endswith('.csv'):

                csv_path = os.path.join(csv_directory, csv_file)
                sdf_file = os.path.join(sdf_directory, csv_file.replace('.csv', '.sdf'))
                if os.path.exists(sdf_file):
                        df = pd.read_csv(csv_path)
                        df = self.score(df)
                        df, first_prop_name = Merge().extract(df,sdf_file)
                        Output(self.verbose).output(df,best_hits_number, first_prop_name)
                      
                        done_sdf_file = sdf_file.replace('.sdf', '_done.sdf')
                        os.rename(sdf_file, done_sdf_file)
                        ok_csv_file = csv_path.replace('.csv', '_ok.csv')
                        os.rename(csv_path, ok_csv_file)
