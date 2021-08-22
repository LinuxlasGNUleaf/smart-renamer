import re
import sys, os
import secrets

if __name__ == '__main__':
    # compiling list of files
    directory = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.getcwd(),'')
    print(f'working directory is: {directory}')
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]

    print(f'{len(files)} found, using RegEx to filter for files to fix.')

    # regex search
    pattern = re.compile(r"images(-[\d]*)?( +\(copy [\d]*\))*\.(\w+)")
    res = [f for f in files if re.search(pattern, f)]

    # renaming
    print(f'found {len(res)} files to fix.')
    if not res:
        print('aborting.')
        exit(0)
    
    max_len = len(max([os.path.splitext(item)[0] for item in res], key=len))
    for result in res:
        fname, fext = os.path.splitext(result)
        while True:
            new_fname = secrets.token_hex(4)
            sys.stdout.write(f'renaming "{fname.ljust(max_len)}" --> "{new_fname}" ({fext}) ...')
            if os.path.isfile(f'{directory}{new_fname}{fext}'):
                print(f'\nWARN: File with name "{new_fname}{fext}" already exists in this directory!')
            else:
                break
        os.rename(os.path.join(directory,fname+fext), os.path.join(directory,new_fname+fext))
        print('done.')
    
    print('All files have been renamed successfully.')