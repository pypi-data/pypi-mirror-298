import pandas as pd
import os

class Output:

    def __init__(self, verbose = False):
        self.verbose = verbose


    @staticmethod
    def __get_column_letter(col_idx):
        """
        Converts a column index to its corresponding letter representation.
        """
        letter = ''
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter

    def __conditional_formatting(self,df,excel_path,first_prop_name):
        """
        Apply conditional formatting to an Excel file based on specified rules. The function uses the xlsxwriter library to write the formatted data.
        """
        writer = pd.ExcelWriter(excel_path, engine="xlsxwriter")

        df.to_excel(writer, sheet_name="Sheet1", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        (max_row, max_col) = df.shape

        green_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
        yellow_format = workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C5700'})
        red_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        gray_format = workbook.add_format({'bg_color': '#D3D3D3'})
        number_format = workbook.add_format({'num_format': '0.00'})
        center_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'}) 


        columns = ['PAMPA', 'pgp_inh', 'pgp_sub', 'hia', 'f20', 'f30', 'f50','OATP1B1', 'OATP1B3', 'BCRP', 'BSEP', 'BBB', 'MRP1','hERG', 'hERG-10um', 'DILI', 'Ames', 'ROA', 'FDAMDD', 'SkinSen', 'Carcinogenicity', 'EC', 'EI', 'Respiratory', 'H-HT', 'Neurotoxicity-DI', 'Ototoxicity', 'Hematotoxicity', 'Nephrotoxicity-DI', 'Genotoxicity', 'RPMI-8226', 'A549', 'HEK293','NR-AhR', 'NR-AR', 'NR-AR-LBD', 'NR-Aromatase', 'NR-ER', 'NR-ER-LBD', 'NR-PPAR-gamma', 'SR-ARE', 'SR-ATAD5', 'SR-HSE', 'SR-MMP', 'SR-p53','CYP1A2-inh', 'CYP1A2-sub', 'CYP2C19-inh', 'CYP2C19-sub', 'CYP2C9-inh', 'CYP2C9-sub', 'CYP2D6-inh', 'CYP2D6-sub', 'CYP3A4-inh', 'CYP3A4-sub', 'CYP2B6-inh', 'CYP2B6-sub', 'CYP2C8-inh', 'LM-human','Aggregators', 'Fluc', 'Blue_fluorescence', 'Green_fluorescence', 'Reactive', 'Promiscuous']

        string_columns = ['NonBiodegradable', 'NonGenotoxic_Carcinogenicity', 'SureChEMBL', 'Skin_Sensitization', 'Acute_Aquatic_Toxicity', 'Genotoxic_Carcinogenicity_Mutagenicity','FAF-Drugs4 Rule','Alarm_NMR', 'BMS', 'Chelating', 'PAINS']

        gray_columns = ['smiles','MW','Vol','Dense','nHA','nHD','TPSA','nRot','nRing','MaxRing','nHet','fChar','nRig','Flex','nStereo','Natural Product-likeness','logS','logD','logP','mp','bp','pka_acidic','pka_basic','MDCK','BCF','IGC50','LC50DM','LC50FM','Other_assay_interference','LD50_oral']

        additional_gray_columns = ['ID_Molecula',first_prop_name,'Match']

        scores_columns = ['SCORE', 'ABSORTION', 'DISTRIBUTION', 'TOXICITY', 'TOX21_PATHWAY', 'METABOLISM', 'TOXICOPHORE_RULES', 'EXCRETION', 'MEDICINAL_CHEMISTRY']

        special_conditions = {
            'Lipinski': [(0, 0, green_format), (1, float('inf'), red_format)],
            'Pfizer': [(0, 0, green_format), (1, float('inf'), red_format)],
            'gasa': [(1, 1, green_format), (0, 0, red_format)],
            'Synth': [(float('-inf'), 6000, green_format), (6000.01, float('inf'), red_format)],
            'GoldenTriangle': [(float('-inf'), 0, green_format), (1, float('inf'), red_format)],
            'GSK': [(float('-inf'), 0, green_format), (1, float('inf'), red_format)],
            'caco2': [(-5150, float('inf'), green_format), (float('-inf'), -5150.01, red_format)],
            'QED': [(670, float('inf'), green_format), (490, 669.99, yellow_format), (float('-inf'), 489.99, red_format)],
            't_0_5': [(8, float('inf'), green_format), (1, 7.9, yellow_format), (float('-inf'), 0, red_format)],
            'PPB': [(float('-inf'), 90, green_format), (90.01, float('inf'), red_format)],
            'Fsp3': [(420, float('inf'), green_format), (float('-inf'), 419, red_format)],
            'MCE_18': [(45000, float('inf'), green_format), (float('-inf'), 44999.99, red_format)],
            'Fu': [(5, float('inf'), green_format), (float('-inf'), 4.99, red_format)],
            'cl_plasma': [(0, 5, green_format), (5.01, 15, yellow_format), (15.01, float('inf'), red_format)],
            'logVDss': [(40, 200, green_format), (float('-inf'), 39.99, red_format), (200.01, float('inf'), red_format)]
        }

        numeric_cols = df.select_dtypes(include=['number']).columns
        for col_name in numeric_cols:

            col_idx = df.columns.get_loc(col_name)
            col_letter = self.__get_column_letter(col_idx + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'
            worksheet.set_column(f'{col_letter}:{col_letter}', None, number_format)


        for col_name in columns:
            col_idx = df.columns.get_loc(col_name)
            col_letter = self.__get_column_letter(col_idx + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'
            
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 0, 'maximum': 300, 'format': green_format})
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 300.01, 'maximum': 700, 'format': yellow_format})
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 700.01, 'maximum': 1000, 'format': red_format})

        for col_name in scores_columns:
    
            col_idx = df.columns.get_loc(col_name)
            col_letter = self.__get_column_letter(col_idx + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'
            
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 7, 'maximum': 10, 'format': green_format})
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 4, 'maximum': 6.99, 'format': yellow_format})
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 0, 'maximum': 3.99, 'format': red_format})

        for col_name in string_columns:
            col_idx = df.columns.get_loc(col_name)
            col_letter = self.__get_column_letter(col_idx + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'

            worksheet.conditional_format(cell_range, {'type': 'text', 'criteria': 'containing', 'value': "['-']", 'format': green_format})
            worksheet.conditional_format(cell_range, {'type': 'text', 'criteria': 'not containing', 'value': "['-']", 'format': red_format})

        for col_name, conditions in special_conditions.items():
            col_idx = df.columns.get_loc(col_name)  
            col_letter = self.__get_column_letter(col_idx + 1)  
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'

            for min_val, max_val, fmt in conditions:
                criteria = 'between'
                if min_val == float('-inf'):
                    criteria = 'less than or equal to'
                    min_val = max_val
                elif max_val == float('inf'):
                    criteria = 'greater than or equal to'
                    max_val = min_val

                worksheet.conditional_format(cell_range, {
                    'type': 'cell',
                    'criteria': criteria,
                    'minimum': min_val,
                    'maximum': max_val,
                    'format': fmt
                })
    
        for col_name in gray_columns:
            col_idx = df.columns.get_loc(col_name)
            col_letter = self.__get_column_letter(col_idx + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'

            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': gray_format})


        try:
            for col_name in additional_gray_columns:
                col_idx = df.columns.get_loc(col_name)
                col_letter = self.__get_column_letter(col_idx + 1)
                cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'

                worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': gray_format})
        except:
            pass    

        worksheet.set_column(f'{col_letter}:{col_letter}', None, workbook.add_format({'num_format': '0.00'}))

        writer.close()

    def __log(self, message: str):
        '''Helper method to print messages if verbose mode is enabled'''
        if self.verbose:
            print(message)

    def __making_top_best_file(self,df,best_hits,first_prop_name):
        """
        Creates an Excel file with the top best molecules based on the given dataframe.
        """
        excel_top_path = os.path.join(f'scoreadmet_{best_hits}_tops.xlsx')
        top_df = df.head(best_hits)
        self.__conditional_formatting(top_df, excel_top_path,first_prop_name)
        

    def output(self,df,best_hits,first_prop_name):
        """
        Updates an existing Excel spreadsheet or creates a new one with the given DataFrame.
        """

        excel_path = os.path.join('scoreadmet.xlsx')

        if os.path.exists(excel_path):
            existing_df = pd.read_excel(excel_path, sheet_name='Sheet1')
            initial_count = len(existing_df)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df = updated_df.sort_values(by='SCORE', ascending=False)
            updated_df.drop_duplicates(subset='ID_Molecula', keep="first", inplace=True)
            final_count = len(updated_df)
            new_entries = final_count - initial_count

            self.__log(f'\n{new_entries} new molecules were added.\n')
        else:
            updated_df = df
            updated_df = updated_df.sort_values(by='SCORE', ascending=False)
    
            try:
                updated_df.drop_duplicates(subset='ID_Molecula', keep='first', inplace=True)
            except:
                pass
        
            final_count = len(updated_df)
            self.__log(f'\nThe spreadsheet was created with {final_count} molecules.\n')

        self.__making_top_best_file(updated_df,best_hits,first_prop_name)
        self.__conditional_formatting(updated_df,excel_path,first_prop_name)

        return updated_df