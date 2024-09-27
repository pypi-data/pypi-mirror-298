from .Evaluate import *
from .BrowserHandler import *
from .Output import *
from .Splitter import *
import pandas as pd

class Screening:
        
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.evaluate = Evaluate(self.verbose)
        self.browser_handler = BrowserHandler(self.verbose)
        self.splitter = Splitter(self.verbose)

    def __log(self, message: str):
        '''Helper method to print messages if verbose mode is enabled'''
        if self.verbose:
            print(message)

    def screen(self,input_file:str, batch_size:int=299, affinity_cutoff:float=None,best_hits_number=50):
        """ 
        
        **Ranks the best molecules based on an admet analysis**
        
        This function takes an SDF file from Pharmit docking and the name of the database used to search for molecules as input. It then divides the SDF file into smaller parts for screening on the ADMETlab 3.0 website. After each part has been screened, the function generates a spreadsheet that ranks the molecules based on their performance across various analysis components. It assigns specific weights to each analysis group and calculates an overall score for each molecule, ranging from 0 (worst performance) to 10 (best performance).

        **Parameters**
        ----------
   
        sdf_file : str
            Path to the SDF file containing molecular structures.
            
        batch_size : int
            number of molecules that will come out in each part.
        
        affinity_cutoff : float, optional
            If provided, only molecules with an affinity score less than or equal to this value will be included in the output batches. Default is None, meaning no filtering by affinity score.
        
        best_hits_number : int, optional
            Number of top-performing molecules to include in the final output. By default, the top 50 molecules are included.
        
        **Examples**
        --------
        >>> screen('molecules.sdf')
        >>> screen('molecules.sdf',1000)
        >>> screen('molecules.sdf', 500, -8)
        >>> screen('molecules.sdf', 500, -8, 10)
        """

        self.splitter.split(input_file,batch_size,affinity_cutoff)
        self.browser_handler.run_tasks(best_hits_number)

        #self.__log(f'↳ File with the {best_hits_number} best molecules was created\n')


