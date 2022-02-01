import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import cross_validate
from surprise import dump
from fuzzywuzzy import fuzz

df = pd.read_excel("user_dataset_final.xlsx")

df.iloc[:, 2].drop_duplicates(keep='first').to_csv("restaurant.csv", index=False, encoding='utf-8')

# matching the restaurants of restaurant_rating and restaurant_CO2
restaurant_CO2 = pd.read_csv("restaurant_CO2.csv")
restaurant = pd.read_csv("restaurant.csv")
CO2 = list()
for r in restaurant.iloc[:, 0]:
    i = 0
    for c in restaurant_CO2.iloc[:, 1]:
        if fuzz.ratio(r.lower(), c.lower()) >= 90:
            CO2.append(float(restaurant_CO2.iloc[i, 2]))
            i = -1
            break
        else:
            i += 1
    if i != -1:
        CO2.append(0)

restaurant["CO2"] = CO2
restaurant.to_csv("restaurant_CO2_final.csv", index=False, encoding='utf-8')

restaurant_CO2 = pd.read_csv("restaurant_CO2_final.csv")
mean = pd.read_csv("restaurant_CO2.csv").iloc[:, 2].mean()
i = 0
for restaurant in restaurant_CO2.iloc[:, 1]:
    index = df[df.iloc[:, 2] == restaurant].index
    df.iloc[index, 3] = float(restaurant_CO2.iloc[i, 2])
    i += 1

adjust_rating = list()
for row in df.index:
    if df.iloc[row, 3] == 0:
        adjust_rating.append(0)
    else:
        adjust_rating.append(mean - df.iloc[row, 3])
df["adjust"] = adjust_rating

df.to_csv("user_rating_CO2.csv", index=False, encoding='utf-8')

adjust_rating = list()
for user in df.index:
    if df.iloc[user, 3] == 0:
        adjust_rating.append(df.iloc[user, 1])
    elif df.iloc[user, 3] <= mean:
        adjust_rating.append(df.iloc[user, 1] * (1 + (1 - df.iloc[user, 3] / mean) / 4))
    elif df.iloc[user, 3] > mean:
        adjust_rating.append(df.iloc[user, 1] / (1 + (1 - mean / df.iloc[user, 3]) / 4))

df["adjust_rating"] = adjust_rating

df.iloc[:, [0, 1, 2, 3, 5]].to_csv("user_rating_CO2.csv", index=False, encoding='utf-8')

reader = Reader(rating_scale=(0, 5 * (1 + 1 / 4)))
data = Dataset.load_from_df(df[['User', 'Restaurant_name', 'adjust_rating']], reader)
train_set, test_set = train_test_split(data, test_size=0.1, random_state=0)
algo = SVD(n_factors=400, n_epochs=100, biased=True, verbose=1)
# cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=10, verbose=True)
algo.fit(train_set)
predictions = algo.test(test_set)
accuracy.rmse(predictions)
user_id, item_id, r_ui = test_set[0]
pred = algo.predict(user_id, item_id, r_ui, verbose=True)
dump.dump('recommender', algo, verbose=1)

pd.read_csv("restaurant.csv").to_csv("restaurant.csv", index=False, encoding='utf-8')

restaurants = pd.read_csv("restaurant.csv")

avg_rating = list()
for restaurant in restaurants.iloc[:, 0]:
    avg_rating.append(round(df[df.iloc[:, 2] == restaurant].iloc[:, 1].mean(), 1))
restaurants["avg_rating"] = avg_rating
restaurants.to_csv("restaurant.csv", index=False, encoding='utf-8')


restaurants = pd.read_csv("restaurant_CO2_final.csv")
CO2 = pd.read_csv("user_rating_CO2.csv")
restaurants_avg = pd.read_csv("restaurant.csv")
restaurants_avg["CO2 score"] = restaurants.iloc[:, 2]
for i in restaurants_avg[restaurants_avg.iloc[:,2] != 0].index:
    restaurants_avg.iloc[i, 2] = round(mean-restaurants_avg.iloc[i, 2], 2)
restaurants_avg.to_csv("restaurant.csv", index=False, encoding='utf-8')

# modify restaurant name in menu to match the name in restaurant.csv
restaurant_CO2 = pd.read_csv("restaurant_CO2.csv")
restaurant = pd.read_csv("restaurant.csv")
menu = pd.read_csv("menu.csv")
for i in restaurant_CO2.iloc[:,1]:
    for j in restaurant.iloc[:,0]:
        if fuzz.ratio(str(i).lower(),str(j).lower())>=90:
            for k in menu[menu.iloc[:,0]==i].index:
                menu.iloc[k, 0]= j
                print(i,menu.iloc[k, 0],j)
menu.to_csv("menu.csv", index=False, encoding='utf-8')
