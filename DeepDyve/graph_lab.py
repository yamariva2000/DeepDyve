import graphlab
import pandas as pd
import numpy as np
from graphlab.toolkits.distances import transformed_dot_product
import matplotlib.pyplot as plt
from graphlab import model_parameter_search, SFrame

def cross_validation(sf):
    training, validation = sf.random_split(0.8)
    params = {'regularization':[.00001,.001,.1,1]}
    mf = graphlab.recommender.factorization_recommender.create(sf, user_id='user', item_id='movie',target='rating',solver='als',regularization=.001)

    job = model_parameter_search.create((training, validation),
                                    graphlab.recommender.factorization_recommender.create,
                                    params, max_models=4)
    results=job.get_results()
    return results.column_names()












df = pd.read_table('data/u.data', names=['user','movie','rating','timestamp'])
sf = graphlab.SFrame(df)
del sf['timestamp']

print cross_validation(sf)
exit()
mf = graphlab.recommender.factorization_recommender.create(sf, user_id='user', item_id='movie',target='rating',solver='als',regularization=.001)

one_datapoint_sf = graphlab.SFrame({'user': [1], 'movie': [100]})
print mf.predict(one_datapoint_sf) #4.545
print "-----------------"
user_sf = mf.coefficients['user']
user_1_vector = user_sf[user_sf['user'] == 1]['factors']
movie_sf = mf.coefficients['movie']
movie_100_vector = movie_sf[movie_sf['movie'] == 100]['factors']
intercept = mf.coefficients['intercept']

rating = np.dot(user_1_vector[0],movie_100_vector[0]) + intercept
print rating

calc_intercept = sf['rating'].mean()

sf['predicted_rating']=mf.predict(sf[['user','movie']])

sf['error_squared']=(sf['rating']-sf['predicted_rating'])**2
rmse = sf['error_squared'].mean()**.5

print rmse
mf.training_rmse==rmse

pd.Series(sf['rating']).describe()
pd.Series(sf['predicted_rating']).describe()

plt.violinplot([sf['rating'],sf['predicted_rating']],[-1,1],points =60,widths=.5,showmeans=True)