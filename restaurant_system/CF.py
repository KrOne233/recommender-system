import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import cross_validate
from surprise import dump

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
