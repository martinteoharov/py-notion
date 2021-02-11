import glob
import pathlib
import zipfile
import os
import shutil
import re
import fileinput

rootPath = pathlib.Path(__file__).parent.absolute()
refactor_dir = 'to_refactor'              # zip files located here
temp_dir = '{}/_temp_/*'.format(rootPath) # for temporary storing files

def deleteInDir(dirname):
    for f in glob.glob(dirname):
        if os.path.isfile(f):
            os.remove(f)
        else:
            shutil.rmtree(f)

def extractFileFromPath(filename):
    # capture after last '/'
    regexSlash = "([^\/]+$)"
    # capture before first '.'
    regexDot = "[^.]*"
    filename = re.search(regexSlash, filename)[0]
    filename = re.search(regexDot, filename)[0]
    return filename







# /home/martin/notion-git/to_refactor
path = '{}/{}'.format(rootPath, refactor_dir)
# /home/martin/notion-git/to_refactor/*
query = '{}/*'.format(path)

# grab all files
files = glob.glob(query)
files_zip = [_ for _ in files if _.find('zip') != -1]

for file_zip in files_zip:
    print('Working on {}:'.format(file_zip))
    deleteInDir(temp_dir)

    with zipfile.ZipFile(file_zip,"r") as zip_ref:
        zip_ref.extractall("_temp_")

    files_unzipped = glob.glob(temp_dir)

    # names
    html_path = next(_ for _ in files_unzipped if _.find('html') != -1) # path of OLD file

    html_name = extractFileFromPath(html_path)                          # name of OLD file

    html_name_target = extractFileFromPath(file_zip)
    html_name_target = "{}.html".format(html_name_target)

    dir_name = html_path.replace(".html", "")                           # name of OLD directory for images
    dir_name_target = "images"                                          # name of NEW directory for images

    # SEARCH & REPLACE dir name
    search = html_path.replace(".html", "")
    search = html_name.replace(" ", "%20")
    print('[ \n\tRefactoring {}.. \n\tReplacing {}/ with {}/'.format(html_path, search, dir_name_target))
    with fileinput.FileInput(html_path, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(search, dir_name_target), end='')

    target_name_dir_out = '{}/{}/{}'.format(rootPath, 'out', dir_name_target)
    target_name_html_out = '{}/{}/{}'.format(rootPath, 'out', html_name_target)

    print('\tSimplifying dir: {} to {}'.format(dir_name, target_name_dir_out))
    print('\tSimplifying html: {} to {} \n]'.format(html_name, target_name_html_out))

    os.rename(html_path, target_name_html_out)

    existing_images = os.listdir(target_name_dir_out)
    for _ in os.listdir(dir_name):
        if _ not in existing_images:
            shutil.move(os.path.join(dir_name, _), target_name_dir_out)
