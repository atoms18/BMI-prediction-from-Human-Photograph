
import time
import pandas
import requests
from os import listdir
from pathlib import Path
from bs4 import BeautifulSoup

df = pandas.read_csv('celeb_name.csv')

already_files = set(df["image"] + ".jpg")
all_files = set(listdir("data/"))

for f in sorted(all_files - already_files):

    with open('data/' + f, 'rb') as fa:
        r = requests.post('https://starbyface.com/Home/LooksLikeByPhoto', files={'imageUploadForm': fa})
        soup = BeautifulSoup(r.text, 'html.parser')
        #with open("test.html") as fp:
        #    soup = BeautifulSoup(fp, 'html.parser')
        try:
            male_best_pair = soup.find("select", id='male-pair-select')
            male_name = male_best_pair.option.get_text()
            male_tag = soup.find(attrs={"name": male_name})
            male_percentage = int(male_tag.find(class_="progress-bar")["similarity"])
        except:
            male_percentage = 0
        
        try:
            female_best_pair = soup.find("select", id='female-pair-select')
            female_name = female_best_pair.option.get_text()
            female_tag = soup.find(attrs={"name": female_name})
            female_percentage = int(female_tag.find(class_="progress-bar")["similarity"])
        except:
            female_percentage = 0
        
        result = "none"
        if male_percentage > 50 and female_percentage > 50:
            if male_percentage > female_percentage:
                result = "male"
            elif male_percentage < female_percentage:
                result = "female"
        else:
            if male_percentage > 50:
                result = "male"
            elif female_percentage > 50:
                result = "female"
        
        if result == "male":
            name = male_name
            percentage = male_percentage
        elif result == "female":
            name = female_name
            percentage = female_percentage
        else:
            name = "none"
            percentage = 0
            
        df = df.append({"image": Path(f).stem, "celeb_name": name, "prop": percentage}, ignore_index=True)
        df.to_csv('celeb_name.csv', index=False)
        print(f"Saved {name} to {f}")
    
    time.sleep(5)