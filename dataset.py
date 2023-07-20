import json
import os

import requests

if not os.path.exists('components'):
    os.mkdir('components')

filename = 'components/scraped.json'
with open(filename) as f:
    data = json.load(f)

dataset_name = 'dataset'
if not os.path.exists(dataset_name):
    os.mkdir(dataset_name)

print("\nThe process may take some time to finish")
for champ in data:
    champ_name = list(champ.keys())[0]
    champ_path = os.path.join(dataset_name, champ_name)
    if not os.path.exists(champ_path):
        os.mkdir(champ_path)
    for value in list(champ.values())[0]:
        for img_url in value:
            img_name = img_url[img_url.rfind('/')+1::]
            if 'splash' in img_url:
                img_name = img_name[len(champ_name)+1::]
                path = os.path.join(champ_path, 'splash')
                if not os.path.exists(path):
                    os.mkdir(path)
            elif 'spell' in img_url:
                img_name = img_name[len(champ_name)::]
                path = os.path.join(champ_path, 'spell')
                if not os.path.exists(path):
                    os.mkdir(path)
            if 'passive' in img_url:
                img_name = img_name[len(champ_name)+1::]
                path = os.path.join(champ_path, 'passive')
                if not os.path.exists(path):
                    os.mkdir(path)
            if 'ability' in img_url:
                for i in ['E1', 'P1', 'Q1', 'R1', 'W1']:
                    if i in img_name:
                        img_name = i[0] + '.jpg'
                        break
                path = os.path.join(champ_path, 'ability')
                if not os.path.exists(path):
                    os.mkdir(path)

            img_data = requests.get(img_url).content
            try:
                with open(os.path.join(path, img_name), 'wb') as handler:
                    handler.write(img_data)
            except:
                print("\nerror in:")
                print(path)

print("\nFinished Downloading")
