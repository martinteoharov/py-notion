import glob
import pathlib
import zipfile
import os
import shutil
import re
import fileinput

rootPath = pathlib.Path(__file__).parent.absolute()
refactor_dir = 'to_refactor'              # zip file located here
temp_dir = '{}/_temp_/*'.format(rootPath) # for temporary storing files

# delete everything from rootPath/temp_dir
for f in glob.glob(temp_dir):
    if os.path.isfile(f):
        os.remove(f)
    else:
        shutil.rmtree(f)


# /home/martin/notion-git/to_refactor
path = '{}/{}'.format(rootPath, refactor_dir)

# /home/martin/notion-git/to_refactor/*
query = '{}/*'.format(path)

# grab all files
files = glob.glob(query)
file_zip = next(_ for _ in files if _.find('zip') != -1)
print('Working on {}:'.format(file_zip))
with zipfile.ZipFile(file_zip,"r") as zip_ref:
    zip_ref.extractall("_temp_")


# capture after last '/'
regexSlash = "([^\/]+$)"
# capture before first '.'
regexDot = "[^.]*"

files_unzipped = glob.glob(temp_dir)

# location of html file
file_html = next(_ for _ in files_unzipped if _.find('html') != -1)

name_html = re.search(regexSlash, file_html)[0]
name_html = re.search(regexDot, name_html)[0]
name_html = name_html.replace(" ", "%20")

name_dir = file_html.replace(".html", "")

target_name_html = "images"
target_name_dir = target_name_html

print('[ \n\tRefactoring {}.. \n\tReplacing {}/ with {}/'.format(file_html, name_html, target_name_html))
with fileinput.FileInput(file_html, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(name_html, target_name_html), end='')


# move name_dir to target_name_dir
target_name_dir = 'images'
target_name_html = 'Functions Intro.html'.format(target_name_dir)

print('\tSimplifying dir: {} to {}'.format(name_dir, target_name_dir))
print('\tSimplifying html: {} to {} \n]'.format(file_html, target_name_html))

target_name_dir_out = '{}/{}/{}'.format(rootPath, 'out', target_name_dir)
target_name_html_out = '{}/{}/{}'.format(rootPath, 'out', target_name_html)

os.rename(name_dir, target_name_dir_out)
os.rename(file_html, target_name_html_out)

