from rdkit import Chem, RDLogger
from rdkit import DataStructs
from rdkit.Chem import AllChem
import pandas as pd

RDLogger.DisableLog('rdApp.*')


class Merge:
       
    def __init__(self):
        self.first_prop_name = None

    def __normalize_smiles(self,smiles):
        """
        Normalize the given SMILES string by removing hydrogens, ensuring canonical form, 
        and replacing specific patterns.
        """
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            normalized_smiles = Chem.MolToSmiles(Chem.RemoveHs(mol), canonical=True, isomericSmiles=True)
            return normalized_smiles
        return smiles
    
    def __extract_ids_affinities_from_sdf(self, sdf_file):
        """
        Extracts molecule IDs, affinities, and normalized SMILES from an SDF file.
        """
        ids_affinity = []
        with Chem.SDMolSupplier(sdf_file) as suppl:
            for mol in suppl:
                if mol is not None:
                    props = mol.GetPropNames()
                    self.first_prop_name = list(props)[0]
                    mol_id = mol.GetProp('_Name')
                    affinity = mol.GetProp(self.first_prop_name)
                    smiles = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
                    smiles = self.__normalize_smiles(smiles)
                    ids_affinity.append((mol_id, affinity, smiles))

        df = pd.DataFrame(ids_affinity, columns=['ID_Molecula', self.first_prop_name , 'smiles'])

        return df
    
    def __find_closest_smiles(self, target_smiles, smiles_list):
        """
        Finds the closest SMILES in the smiles_list to the target_smiles based on Tanimoto similarity.
        """
        target_mol = Chem.MolFromSmiles(target_smiles)
        target_fp = AllChem.GetMorganFingerprintAsBitVect(target_mol, 2)
        
        max_similarity = 0
        closest_smiles = None
        for smiles in smiles_list:
            mol = Chem.MolFromSmiles(smiles)
            if mol is not None:
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2)
                similarity = DataStructs.TanimotoSimilarity(target_fp, fp)
                if similarity > max_similarity:
                    max_similarity = similarity
                    closest_smiles = smiles
        return closest_smiles

    def __merge_with_approximation(self, df_final, df_csv):
        """
        Merge df_final and df_csv using an exact match and then find closest matches for non-matched SMILES.
        """

        df_merged = pd.merge(df_final, df_csv, on='smiles', how='left')
        df_merged['Match'] = 'exact'
        unmatched_final = df_merged[df_merged.isnull().any(axis=1)]
        df_csv['smiles'] = df_csv['smiles'].astype(str)

        unmatched_csv = df_csv[~df_csv['smiles'].isin(df_merged['smiles'])]

        for index, row in unmatched_final.iterrows():
            closest_smiles = self.__find_closest_smiles(row['smiles'], unmatched_csv['smiles'].tolist())
            if closest_smiles:
                closest_row = df_csv[df_csv['smiles'] == closest_smiles]
                if not closest_row.empty:
                    for col in closest_row.columns:
                        df_merged.at[index, col] = closest_row.iloc[0][col]
                    df_merged.at[index, 'Match'] = 'similar'

        df_merged.drop_duplicates(inplace=True)
        new_cols_to_move = ['SCORE', 'ABSORTION', 'DISTRIBUTION', 'TOXICITY', 'TOX21_PATHWAY', 'METABOLISM', 'TOXICOPHORE_RULES', 'EXCRETION', 'MEDICINAL_CHEMISTRY']

        move_cols =  ['ID_Molecula', self.first_prop_name,'Match'] + new_cols_to_move + ['smiles'] + [col for col in df_merged.columns if col not in new_cols_to_move and col not in ['ID_Molecula', self.first_prop_name ,'Match', 'smiles']]

        df_merged = df_merged[move_cols]

        return df_merged, self.first_prop_name

    def extract(self, df_csv, sdf_file):
        """
        Extracts data from a CSV file and an SDF file, merges them based on the 'smiles' column,
        and returns the merged DataFrame.
        """ 
        try:
            df = self.__extract_ids_affinities_from_sdf(sdf_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo SDF {sdf_file} não encontrado.")
        
        df_merged, first_prop_name  = self.__merge_with_approximation(df, df_csv)


        return df_merged, first_prop_name