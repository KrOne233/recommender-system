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
df_algo = df.sample(frac=0.9)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['User', 'Restaurant_name', 'Rating']], reader)
train_set, test_set = train_test_split(data, test_size=0.25, random_state=0)
algo = SVD(n_factors=350, n_epochs=100, biased=True, verbose=1)
# cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=10, verbose=True)
algo.fit(train_set)
predictions = algo.test(test_set)
accuracy.rmse(predictions)
user_id, item_id, r_ui = test_set[0]
pred = algo.predict(user_id, item_id, r_ui, verbose=True)
dump.dump('recommender', algo, verbose=1)

df.iloc[:, 2].drop_duplicates(keep='first').to_csv("restaurant.csv", index=False)

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
restaurant.to_csv("restaurant_CO2_final.csv", )

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
        adjust_rating.append(df.iloc[user, 1] * (2 - df.iloc[user, 3] / mean))
    elif df.iloc[user, 3] > mean:
        adjust_rating.append(df.iloc[user, 1] / (2 - mean / df.iloc[user, 3]))

df["adjust_rating"] = adjust_rating

df.iloc[:,[0,1,2,3,5]].to_csv("user_rating_CO2.csv", index=False, encoding='utf-8')