import tempfile
import datetime
import os
import re

class Splitter:
    '''Receives the sdf file from the docking result made on the Pharmit website, and divides it into several SDFs to be uploaded at a time to ADMETlab 3.0.'''
    
    def __init__(self, verbose=False):
        self.verbose = verbose

    def extract_database_name(self, input_file):
        '''Function that extracts the database name from the first line of the SDF file.'''
        with open(input_file, 'r') as file:
            input_file = file.read()

        molecules = input_file.split('$$$$')

        for molecule in molecules:
            lines = molecule.strip().splitlines()
            if lines:
                first_line = lines[0].strip()
                if first_line:
                    first_id = first_line.split()[0]

                    if '-' in first_id:
                        database_name = first_id.split('-')[0]
                    else:
                        match = re.match(r"([A-Za-z]+)", first_id)
                        if match:
                            database_name = match.group(1)
                        else:
                            database_name = first_id

                    return database_name

        return None

    @staticmethod
    def __removing_duplicates(input_file, database):
        '''Removes duplicates from the original SDF before going to the split function, so the final amount of files is smaller and more efficient.'''
        with open(input_file, 'r') as file, tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sdf') as temp_sdf:
            molecules = set()
            current_molecule = []
            write_molecule = False

            for line in file:
                if line.startswith(database):
                    mol_id = line.strip()
                    if mol_id not in molecules:
                        molecules.add(mol_id)
                        write_molecule = True
                    else:
                        write_molecule = False
                if write_molecule:
                    current_molecule.append(line)
                if line.startswith('$$$$'):
                    if write_molecule:
                        temp_sdf.writelines(current_molecule)
                    current_molecule = []
            temp_file_name = temp_sdf.name

        return temp_file_name

    @staticmethod
    def __save_batch(batch, database, index):
        '''Function that will be used in process SDF to save each division in files.'''
        with open(os.path.join("sdf", f"{database}_{index:04d}.sdf"), 'w') as f:
            f.writelines(batch)

    def __log(self, message: str):
        '''Helper method to print messages if verbose mode is enabled.'''
        if self.verbose:
            print(message)

    def split(self, input_file: str, batch_size: int = 299, affinity_cutoff: float = None):
        """
        **Split SDF Files in Batches**
        
        Function that will create the folder called 'sdf' to place the divisions of the original SDF there. It provides the possibility of filtering by the first characteristic after 'M  END' and allows changing the number of molecules in each division.

        **Parameters:**
        -----------
        input_file : str
            Path to the input SDF file that needs to be processed.
        
        batch_size : int
            Number of molecules that will come out in each part.
        
        affinity_cutoff : float, optional
            If provided, only molecules with a score less than or equal to this value for the first characteristic after 'M  END' will be included in the output batches. Default is None, meaning no filtering by this score.

        **Raises**
        -------
        ValueError
            If the user provides an invalid input when prompted to overwrite existing files.
        
        **Side Effects**
        -------------
        Creates a folder named 'sdf' in the current working directory if it doesn't already exist.
        Prompts the user to confirm file deletion if files already exist in the 'sdf' folder.

        **Returns**
        --------
        None
            This function does not return any value. It writes the output files directly to the disk.

        **Examples**
        --------
        >>> split('molecules.sdf', 'MolPort')
        >>> split('molecules.sdf', 'CHEMBL', 1000)
        >>> split('molecules.sdf', 'PubChem', 500, -8)
        """

        database = self.extract_database_name(input_file)
        temp_file = self.__removing_duplicates(input_file, database)
        input_file = temp_file 


        self.__log('')
        if os.path.exists("sdf"):
            existing_files = [f for f in os.listdir("sdf") if f.startswith(database)]
            if existing_files:
                user_choice = input(f'There are already {database} files in the sdf folder.\nDo you want: (y): To delete these files and create new ones? Or (n): Continue processing with copies of the files? (y/n): ').strip().lower()
                match user_choice:
                    case 'y':
                        for file in existing_files:
                            os.remove(os.path.join("sdf", file))
                        self.__log(f'\nAll {database} files have been deleted and new processing was done.')
                    case 'n':
                        now = datetime.datetime.now()
                        timestamp = now.strftime("%Y%m%d_%H%M%S")
                        database += '_' + timestamp
                    case _:
                        raise ValueError()
        else:
            os.makedirs("sdf")

        with open(input_file, 'r') as file:
            lines = file.readlines()

        current_molecule = []
        current_value = None
        first_database_name = None

        batch = []
        file_index = 1
        molecule_count = 0

        for i, line in enumerate(lines):
            if not current_molecule:
                first_database_name = line.split()[0] if line.strip() else None
                if first_database_name:
                    current_molecule.append(first_database_name + '\n')
            else:
                current_molecule.append(line)

            if line.startswith("M  END"):
                # Find the first characteristic after "M  END"
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('>  <'):
                        current_value = float(lines[j + 1].strip())
                        break

            if line.strip() == '$$$$':
                if affinity_cutoff is None or (current_value is not None and current_value <= affinity_cutoff):
                    batch.extend(current_molecule)
                    molecule_count += 1

                current_molecule = []
                current_value = None
                first_database_name = None

                if molecule_count == batch_size:
                    self.__save_batch(batch, database, file_index)
                    file_index += 1
                    batch = []
                    molecule_count = 0

        if batch:
            self.__save_batch(batch, database, file_index)
            match database:
                case 'CSC':
                    self.__log('Database: ChemSpace')
                    self.__log(f'ID: {database}')
                case 'Z':
                    self.__log('Database: Enamine')
                    self.__log(f'ID: {database}')
                case 'LN':
                    self.__log('Database: WuXi LabNetwork')
                    self.__log(f'ID: {database}')
                case 'NSC':
                    self.__log('Database: NCI Open Chemical Repository')
                    self.__log(f'ID: {database}')
                case _:
                    self.__log(f'ID: {database}')
            
        else:
            raise ValueError('\n\nNO MOLECULES FOUND IN THE INPUT.\n')

        self.__log(f"Number of batches in sdf folder: {file_index}\n")
