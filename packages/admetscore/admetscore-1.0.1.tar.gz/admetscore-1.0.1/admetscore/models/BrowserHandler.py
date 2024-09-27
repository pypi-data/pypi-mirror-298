from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from .Evaluate import * 
import threading
import shutil
import time
import os

class BrowserHandler:

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.evaluate = Evaluate(self.verbose)

    def __log(self, message: str, end='\n'):
        '''Helper method to print messages if verbose mode is enabled'''
        if self.verbose:
            print(message, end=end)

    @staticmethod
    def wait_for_download(directory, timeout=600):
        '''
        Waits for a file to be downloaded in the specified directory.
        Parameters:
        - directory (str): The directory where the file is expected to be downloaded.
        - timeout (int): The maximum time to wait for the file to be downloaded, in seconds. Default is 600 seconds.
        Returns:
        - str: The path of the downloaded file if it is found within the timeout period, otherwise None.
        '''
        end_time = time.time() + timeout
        while time.time() < end_time:
            files = [f for f in os.listdir(directory) if not f.endswith('.crdownload')]
            if files:
                return os.path.join(directory, files[0])
            time.sleep(1)
        return None

    def animate(self):
        '''
        Animates a loading animation.
        This method displays a loading animation using a sequence of characters.
        The animation will continue until the `stop_animation` flag is set to True.
        '''
        animation = "|/-\\"
        idx = 0
        while not stop_animation:
            self.__log(animation[idx % len(animation)], end="\r")
            idx += 1
            time.sleep(0.3)

    def run_tasks(self,best_hits_number):
        """
            This method performs the following tasks:
            1. Sets up the necessary options for the Chrome webdriver.
            2. Creates a temporary download directory if it doesn't exist.
            3. Initializes the Chrome webdriver.
            4. Navigates to the screening page on the website.
            5. Retrieves the list of files to process.
            6. For each file, uploads it to the website, starts an animation, and processes it.
            7. Downloads the processed file and saves it with a new name.
            8. Stops the animation and evaluates the folder for best hits.
            9. Cleans up the download directory.
            10. Handles exceptions and logs any errors.
            Note:
            - This method assumes that the Chrome webdriver is installed and available in the system's PATH.
            - The animation is started and stopped using the 'stop_animation' global variable.
        """
        
        global stop_animation



        self.__log('  Starting screening...',end='\r')
        try:

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            download_dir = os.path.join(os.getcwd(), 'temp')
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            options.add_experimental_option('prefs', {
                'download.default_directory': download_dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            })

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

            driver.get('https://admetlab3.scbdd.com/server/screening')
            input_dir = 'sdf'
            output_dir = 'admetlab3_files'

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and 'done' not in f]

            for file in files:
                file_path = os.path.join(input_dir, file)
                absolute_file_path = os.path.abspath(file_path)

                upload_element = driver.find_element(By.ID, 'molecule-file')
                upload_element.send_keys(absolute_file_path)

                stop_animation = False
                animation_thread = threading.Thread(target=self.animate)
                animation_thread.start()
                self.__log(f'  Processing {file}.',end='\r')

                submit_button = driver.find_element(By.XPATH, "//button[@class='btn btn-success' and @onclick='submit1()']")
                submit_button.click()

                download_button = WebDriverWait(driver, 600).until(
                    EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-outline-success' and @onclick='download()']"))
                )

                download_button.click()

                downloaded_file_path = self.wait_for_download(download_dir)
                if downloaded_file_path:

                    new_file_name = os.path.splitext(file)[0] + '.csv'
                    new_file_path = os.path.join(output_dir, new_file_name)
                    os.rename(downloaded_file_path, new_file_path)
                    stop_animation = True
                    self.evaluate.folder_handler(best_hits_number)

                else:
                    pass

                driver.get('https://admetlab3.scbdd.com/server/screening')


            driver.quit()

            shutil.rmtree(download_dir)
        except:
            self.__log('admetlab3.scbdd.com is offline. \n')
            return

        finally:    
            stop_animation = True
            animation_thread.join()
