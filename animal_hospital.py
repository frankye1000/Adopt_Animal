import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle

resp = requests.get("https://right-pet.cc/hospital.php?", verify=False)

soup = BeautifulSoup(resp.text, 'html5lib')
select = soup.select("div#hospital_list_block > div.hospital_bookmarker > a")

domain = "https://right-pet.cc/"
urllists = [domain+i.get('href') for i in select]

hospital_name=[]
hospital_area=[]
hospital_address=[]
hospital_phonenumber=[]
for url in urllists:
    # url = 'https://right-pet.cc/hospital.php?city=76'
    resp = requests.get(url, verify=False)
    soup = BeautifulSoup(resp.text, 'html5lib')
    select_title = soup.select("div#hospital_list_block > div.hospital_list_title > a")
    select_area = soup.select("div#hospital_list_block > div.hospital_list_area > a")
    select_detail = soup.select("div#hospital_list_block > div.hospital_list_detail > a")

    title = [i.text for i in select_title if len(i.text)>0 and i.text!="官網"]
    area = [i.text for i in select_area if len(i.text)>0 ]
    detail = [i.text for i in select_detail if len(i.text)>0 ]
    print(len(title))
    print(len(area))
    print(len(detail[0::2]))
    print(len(detail[1::2]))
    hospital_name.extend(title)
    hospital_area.extend(area)
    hospital_address.extend(detail[0::2])
    hospital_phonenumber.extend(detail[1::2])

hospital_dict = {"hospital_name":hospital_name, "hospital_area":hospital_area, "hospital_address":hospital_address, "hospital_phonenumber":hospital_phonenumber}
hospital_df = pd.DataFrame(hospital_dict)
print(hospital_df)

with open("./animal_hospital.pickle", "wb") as fp:
    pickle.dump(hospital_df, fp)