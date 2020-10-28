from os import listdir
from os.path import isfile, join

from pathlib import Path
import shutil


mypath = "outlier"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for file in onlyfiles:
    shutil.move("raw_datasets/"+Path(file).stem+".jpg", "raw_outlier_datasets/"+Path(file).stem+".jpg")