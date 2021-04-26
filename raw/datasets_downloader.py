
# python script to downloads all image from www.height-weight-chart.com

import time

import pandas
import requests
from bs4 import BeautifulSoup

URL = 'http://www.height-weight-chart.com'

df = pandas.read_csv('height-weight-chart_dataset.csv')

for foot in range(4, 7):
    if foot == 4: continue

    for inch in range(0, 12):
        if (foot == 4 and inch < 10) or (foot == 6 and inch > 8):
            continue
        for pound in range(90, 390, 10):
            time.sleep(5)
            url_path = f"{foot}{inch:02}-{pound:03}"
            page_requests = requests.get(f'{URL}/{url_path}.html')
            if not page_requests.ok:
                print(f"{url_path} was not found")
            else:
                soup = BeautifulSoup(page_requests.content, 'html.parser')
                img_largepic = soup.find_all("img", class_='largepic')
                
                if len(img_largepic) == df[df.image_filename.str.startswith(url_path)].shape[0]:
                    print(f"{url_path} have already exist")
                    continue
                
                i = 0
                for each_img_largepic in img_largepic:
                    if each_img_largepic['src'] == "l/missing-guy.jpg":
                        print(f"{url_path} have no person image")
                        continue
                        
                    img_requests = requests.get(f"{URL}/{each_img_largepic['src']}")

                    file_name = f"{url_path}-{i}.jpg"
                    with open("datasets/" + file_name, 'wb') as img_file:
                        img_file.write(img_requests.content)
                        print(f"Download {file_name} completed")
                        df = df.append({"image_filename": file_name, "weight": pound, "foot": foot, "inch": inch}, ignore_index=True)
                        df.to_csv('height-weight-chart_dataset.csv', index=False)
                    i += 1
                    