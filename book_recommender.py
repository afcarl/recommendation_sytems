import csv
from lightfm import LightFM
import get_data
import numpy as np


data = get_data.fetch_bx_book_ratings(min_rating = 5)

model = LightFM(loss='warp')
model.fit(data['train'],epochs=100,num_threads=2)

def recommend(model,data,user_ids):
    # set number of users and number of items
    n_users,n_books = data['train'].shape
    # print(data['train'].shape(),data['train'].shape)
    for user_id in user_ids:
        # todo :  add known positives

        # model predicts
        scores = model.predict(user_id,np.arange(n_books))
        print(np.argsort(-scores))
        # print(np.argsort(-scores))

        # sort in most ranked to least
        top = np.array(data['list_of_books'])[np.argsort(-scores)]
        # print(top[:5])

        # printing results
            # print("user %s" %user_id)
            # print('     known likes')
            # for movie in known[:5]:
            #     print(movie)

        print('recommended for user %s' %str(user_id))
        for movie in top[0:5]:
            print('			%s' % '-'.join(movie))

recommend(model,data,[276744,276747,276747])
