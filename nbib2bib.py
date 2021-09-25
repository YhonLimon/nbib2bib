##################################################################
'''Script to convert .nbib to bibTeX. Written by Thiago Santos.'''
##################################################################
import os
from time import strftime
from time import sleep, time
import urllib.request as req
from urllib.error import HTTPError

def n_files(directory):
    '''Counts the number of files in the directory that can be converted'''
    total = 0
    for file in os.listdir(directory):
        if (file.lower().endswith('.nbib')):
            total += 1
    return total

def create_bibs_folder(directory):
    '''Creates a new directory within current directory called bibs'''
    directory = os.path.join(directory, 'bibs')
    if not os.path.exists(directory + '/bibs'):
        os.makedirs(directory + '/bibs')

if __name__ == "__main__":
    input('Press enter to continue...')

    ti = time()

    directory = os.getcwd()

    if n_files(directory) == 0: # verifying how many nbib files are present in the current folder (if 0, the program doesn't do anything and stop)
        print('There are no files to convert')
        exit()

    create_bibs_folder(directory)

    print('Starting conversion... \n')

    try:
        files = [file for file in os.listdir(directory) if file.endswith('.nbib')]
        print(f"I find {len(files)} nbib files at folder {directory}")
        new_file = "./bibs"

        BASE_URL = 'http://dx.doi.org/'

        with open(f'bibs/ref.bib', 'w') as output:
            for i, file in enumerate(files):
                ending = '.nbib'

                with open(file, "r") as f:
                    for line in f:
                        string = "doi"
                        doi = ""

                        if string in line: # checking if string is present in line
                            # the doi begins after "PID - ", what means the 7th character (6th, when considered that python starts to count on 0)
                            # the doi string ends before " " (blank space)
                            doi = line[6:line.rfind(" ")]
                            print(f"DOI {i+1}: {doi}")
                            break

                if os.path.getsize(file) == 0 or doi == "":
                    print(f"Can't find DOI in {file}.")
                    continue

                url = BASE_URL + doi
                
                r = req.Request(url, headers={"Accept": "application/x-bibtex"})
                
                try:
                    with req.urlopen(r) as reqopen:
                        bib = reqopen.read().decode()
                except HTTPError:
                    if HTTPError.code == 404:
                        print('DOI not found')
                    else:
                        print('Service unavailable')

                output.write(f'{bib}\n\n')

            output.close()

        tf = time()
        print(f"Processing time: {tf-ti}")
        input("Press enter to finish process...")
    except Exception as e:
        print(e)

    print('\nConversion finished at ' + strftime("%H:%M:%S"))
    