# importing dependencies
import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM

np.set_printoptions(threshold=np.nan)
# getting datasets
data = fetch_movielens(min_rating=4.0)
# print(data['item_labels'][0])
# print(data['item_labels'][data['train'].tocsr()[0].indices])
# print(data['train'].shape)
# for key,value in data.items():
#     print(key,data)

# print('Training data')
# print(repr(data['train']))

# print('test data')
# print(repr(data['test']))

# create model
model = LightFM(loss='warp')

# train model
model.fit(data['train'],epochs=30,num_threads=2)

def recommend(model,data,user_ids):
    # set number of users and number of items
    n_users,n_items = data['train'].shape
    # print(data['train'].shape(),data['train'].shape)
    for user_id in user_ids:
        known = data['item_labels'][data['train'].tocsr()[user_id].indices]

        # model predicts
        scores = model.predict(user_id,np.arange(n_items))
        print(np.argsort(-scores))
        # print(np.argsort(-scores))

        # sort in most ranked to least
        top = data['item_labels'][np.argsort(-scores)]
        print(top[:5])
        return

        printing results
        print("user %s" %user_id)
        print('     known likes')
        for movie in known[:5]:
            print(movie)

        print('     recommended')
        for movie in top[0:5]:
            print(movie)

recommend(model,data,[2,4,6])
