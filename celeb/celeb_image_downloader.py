
import time
import pandas
import matplotlib.pyplot as plt
from simple_image_download import simple_image_download as simp

df = pandas.read_csv('celeb_name.csv')
sure_df = df[df["prop"] == 100]
shuffle_df = sure_df.sample(frac=1)

ds_df = pandas.read_csv('celeb_datasets.csv')
annotation_df = pandas.read_csv('annotation.csv')

bmi = ds_df["weight"] * 703 / (ds_df["foot"] * 12 + ds_df["inch"]) ** 2



data_num = 100

i = 0
for ind in shuffle_df.index: 
    if i == data_num: break
    
    celeb_name = shuffle_df['celeb_name'][ind]
    name = celeb_name.replace(' ', '').lower()
    
    annotation = annotation_df[annotation_df['image'] == shuffle_df['image'][ind]]
    if annotation["BMI"].iloc[0] < 25:
        print(f"BMI of {celeb_name} is under 25. (Skipped)")
        continue
        
    pound = round(annotation["weight"].iloc[0] * 2.205)
    foot_float = annotation["height"].iloc[0] * 3.281
    foot = int(foot_float)
    inch = round((foot_float - foot) * 12)

    if not ds_df[ds_df['image_filename'] == name + '1.jpg'].empty:
        print(f"Image of {celeb_name} is already exist. (Skipped)")
        continue
    
    response = simp.simple_image_download
    response().download(celeb_name + ' entire body', 5, filename=name)
    
    for j in range(5):
        ds_df = ds_df.append({"image_filename": f"{name}{j+1}.jpg", "weight": pound, "foot": foot, "inch": inch}, ignore_index=True)
    ds_df.to_csv('celeb_datasets.csv', index=False)

    i += 1
    print(f"Downloading {celeb_name}'s image is complete. ({i}/{data_num})")

    time.sleep(5)

