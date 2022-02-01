import spacy
import pandas as pd

df = pd.read_excel('Menu_with Ingredient Map.xlsx')
df = df.iloc[:,[0,1,2,3]]

nlp = spacy.load('en_core_web_sm')
desc = df["ITEM_DESC"]
item = list()
for i in desc:
    if isinstance(i, str):
        doc = nlp(i)
        for chunk in doc.noun_chunks:
            print(chunk.text)
            item.append(chunk.text)

import nltk
from nltk.corpus import wordnet as wn

food = wn.synset('food.n.02')
food_list = list(set([w for s in food.closure(lambda s: s.hyponyms()) for w in s.lemma_names()]))

from fuzzywuzzy import fuzz

food_extract = list()
count_old = 0
count_new = 0
for word in item:
    words = word.split(" ")
    if len(words) > 2:
        continue
    for food in food_list:
        if fuzz.ratio(word, food) > 70:
            food_extract.append(word)
            break
        for i in words:
            if fuzz.ratio(i, food) > 80:
                food_extract.append(word)
                count_new = count_old + 1
                break
        if count_new - count_old == 1:
            count_old = count_new
            break
    print(count_old)

ingredients = pd.DataFrame({"ingredient": food_extract}).drop_duplicates(keep="first").reset_index(drop=True)

import requests

item = ingredients.iloc[643, 0]
url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=MEnPJixx3VqrlIg9jFrSOgcDC0zEF1Gzh1FDOMZO&query=" + item + "&dataType=Foundation,SR Legacy"
req = requests.get(url)  # 请求连接
req_jason = req.json()  # 获取数据

count = 0
foodCategory1 = list()
foodCategory2 = list()
for item in ingredients.iloc[:, 0]:
    url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=MEnPJixx3VqrlIg9jFrSOgcDC0zEF1Gzh1FDOMZO&query=" + item + "&dataType=Foundation,SR Legacy&sortBy=dataType.keyword&pageSize=5"
    req = requests.get(url)
    req_jason = req.json()
    keys = list(req_jason.keys())
    if "error" in keys:
        foodCategory1.append("error")
        foodCategory2.append("error")
        print(item, "error", "error")
        count += 1
        print(count)
        continue
    if req_jason['totalHits'] == 0:
        foodCategory1.append("0")
        foodCategory2.append("0")
        print(item, 0, 0)
    elif req_jason['totalHits'] == 1:
        foodCategory1.append(req_jason["foods"][0]["foodCategory"])
        foodCategory2.append("0")
        print(item, req_jason["foods"][0]["foodCategory"], 0)
    else:
        foodCategory1.append(req_jason["foods"][0]["foodCategory"])
        foodCategory2.append(req_jason["foods"][1]["foodCategory"])
        print(item, req_jason["foods"][0]["foodCategory"], req_jason["foods"][1]["foodCategory"])
    count += 1
    print(count)

ingredients["foodCategory1"] = foodCategory1
ingredients["foodCategory2"] = foodCategory2
is_differ = list()
for i in ingredients.index:
    if ingredients.iloc[i, 1] != ingredients.iloc[i, 2]:
        print(ingredients.iloc[i, :])
        is_differ.append(1)
    else:
        is_differ.append(0)
ingredients["is_differ"] = is_differ
ingredients.to_csv("ingredients.csv", encoding="utf-8")

foodCategory_CO2 = pd.read_excel("ingredients_CO2.xlsx", sheet_name="Sheet3")
basicFood_C02 = pd.read_excel("ingredients_CO2.xlsx", sheet_name="Sheet4")
food_category = pd.read_excel("ingredients_CO2.xlsx", sheet_name="Sheet1")

# Assign co2 score to each restaurant
nlp = spacy.load('en_core_web_sm')
restaurant = df.iloc[:, 0].drop_duplicates(keep="first").reset_index(drop=True)
restaurant_CO2 = dict()
count = 0
for res_name in restaurant:
    level = list()
    index = df[df.iloc[:, 0] == res_name].index  # get the index of current restaurant in the dataframe
    for i in list(index):  # for each menu of this restaurant
        doc = df.iloc[i, 2]  # get menu description
        if isinstance(doc, str):  # extract noun from the text
            doc = nlp(doc)
            for chunk in doc.noun_chunks:  # for each noun, matching it the the basicFood list
                if len(chunk.text.split(" ")) > 2:
                    continue
                for word in chunk.text.lower().replace("/n", " ").split(" "):
                    j = 0
                    for food in basicFood_C02.iloc[:, 0].str.lower():
                        if fuzz.ratio(word, food) >= 90:
                            level.append(float(basicFood_C02.iloc[j, 3]))
                            j = -1
                            break
                        else:
                            j += 1
                    if j == -1:
                        break
                if j == -1:
                    continue
                else:
                    k = 0
                    for food in food_category.iloc[:, 1].str.lower():
                        if fuzz.ratio(chunk.text.lower().replace("/n", " "), food) >= 90:
                            category = food_category.iloc[k, 5]
                            if category in list(foodCategory_CO2.iloc[:, 0]):
                                level.append(
                                    float(foodCategory_CO2[foodCategory_CO2.iloc[:, 0] == category].iloc[:, 1]))
                                k = -1
                                break
                            else:
                                k += 1
                        else:
                            k += 1
    restaurant_CO2[res_name] = level
    count += 1
    print(count)

score = list()
for key in restaurant_CO2.keys():
    score.append(sum(restaurant_CO2.get(key)) / len(df[df.iloc[:, 0] == key].index))
restaurant = pd.DataFrame({"restaurant": restaurant, "CO2 level": score})
restaurant.to_csv("restaurant_CO2.csv")

df.to_csv("menu.csv", index=False, encoding='utf-8')