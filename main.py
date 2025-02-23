import requests
import math
import time
import pandas as pd
import seaborn
import get_photos
import SatalliteClassifier

prices = pd.read_csv('prices.csv')

coor = (36.01029,-96.1725)
cen_coor = (36.153977, -95.992714)

def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1])

miles_range = 10

num_rows = 25
num_cols = 31

ijmatrix = {}

last_zipcode = None

#25 rows, 31 cols

# city_lat, city_lon = get_photos.get_city_coordinates("Tulsa, Oklahoma")
# get_photos.capture_gee_images(city_lat, city_lon, date1='2018-01-01', date2='2025-02-22', deltalr=0.0058, deltaud=0.0058, miles_range=10)


ams = SatalliteClassifier.process_all_images('data')


class Ov:
    def __init__(self, a):
        self.iloc = [a]

center = (num_rows // 2, num_cols // 2)


for row in range(0, num_rows):
    for col in range(0, num_cols):
        isCircle = True

        if math.sqrt((col - center[0])**2 + (row - center[1])**2) > center[1]:
            isCircle = False

        qpos = (
            round(coor[0] + row * 2 * (cen_coor[0] - coor[0]) / num_cols, 5),
            round(coor[1] + col * 2 * (cen_coor[1] - coor[1]) / num_rows, 5)
        )

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={qpos[0]}&lon={qpos[1]}"

        r = requests.get(url, headers={"Accept": "*/*", 'Connection': 'keep-alive', 'User-Agent': 'PostmanRuntime/7.26.8'})
        resp = r.json()
        try:
            zipcode = resp['address']['postcode']
        except:
            zipcode = "696969"
            if "class" in resp and resp["class"] == "highway":
                zipcode = "696969420"
            print("invalid address", resp, qpos)

        if zipcode[0] == "4":
            # swap first two
            zipcode = zipcode[1] + zipcode[0] + zipcode[2] + zipcode[3] + zipcode[4]
        elif zipcode[0] != "7" and zipcode != "696969" and zipcode != "696969420":
            print("skipping", zipcode, qpos)
            zipcode = last_zipcode
        last_zipcode = zipcode

        wr = requests.get(f"https://is-on-water.balbona.me/api/v1/get/{qpos[0]}/{qpos[1]}").json()
        isWater = wr['isWater']

        # match "RegionName" with zipcode
        price_for_this_address = prices.get(prices['RegionName'] == int(zipcode))['2025-01-31']

        if len(list(price_for_this_address)) == 0:
            print("skipping", zipcode, qpos, list(price_for_this_address))
            price_for_this_address = Ov(80000) # flexible num

        isValid = (isCircle and (not isWater))
        ijmatrix["data_"+str(col)+"-"+str(row)] = {
            "price": int(price_for_this_address.iloc[0]) * max(ams[(row, col)], 1),
            "isValid": isValid,
            "i": str(col),
            "j": str(row)
        }

        # print(list(price_for_this_address.iloc), zipcode, qpos)

        # time.sleep(0.5)

        print(row, col, qpos, int(price_for_this_address.iloc[0]), zipcode, isValid)
    
print(ijmatrix)
# invert ij matrix
df = pd.DataFrame(ijmatrix)
# transpose
df = df.T
df.to_csv('ijmatrix.csv')
# print prices as csv
# print prices as csv
