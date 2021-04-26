
import shutil

from os import listdir
from os.path import isfile, join
from pathlib import Path


outlier_files = {f for f in listdir("outlier") if isfile(join("outlier", f))}
raw_outlier_files = {Path(f).stem + ".jpg" for f in listdir("raw_outlier_datasets/") if isfile(join("raw_outlier_datasets/", f))}

move_files = outlier_files - raw_outlier_files
print(raw_outlier_files)

#for file in move_files:
#    shutil.move("outlier/"+Path(file).stem+".png", "outlier/nude/"+Path(file).stem+".png")

