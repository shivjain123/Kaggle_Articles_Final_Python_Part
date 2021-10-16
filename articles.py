import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

users_interactions = pd.read_csv('users_interactions.csv')
shared_articles = pd.read_csv('shared_articles.csv')

"""Demographic Filtering"""

shared_articles = shared_articles[shared_articles["eventType"] == "CONTENT SHARED"]
shared_articles = shared_articles[shared_articles["lang"] == "en"]

def findTotalEvents(rowdf):
  total_views = users_interactions[(users_interactions['contentId'] == rowdf['contentId']) & (users_interactions['eventType'] == "VIEW")].shape[0]
  total_likes = users_interactions[(users_interactions['contentId'] == rowdf['contentId']) & (users_interactions['eventType'] == "LIKE")].shape[0]
  total_bookmarks = users_interactions[(users_interactions['contentId'] == rowdf['contentId']) & (users_interactions['eventType'] == "BOOKMARK")].shape[0]
  total_follows = users_interactions[(users_interactions['contentId'] == rowdf['contentId']) & (users_interactions['eventType'] == "FOLLOW")].shape[0]
  total_commentCreated = users_interactions[(users_interactions['contentId'] == rowdf['contentId']) & (users_interactions['eventType'] == "COMMENT CREATED")].shape[0]
  return (total_views + total_likes + total_bookmarks + total_follows + total_commentCreated)

shared_articles["Total Events"] = shared_articles.apply(findTotalEvents, axis = 1)

shared_articles = shared_articles.sort_values(["Total Events"], ascending=[False])

"""Content-Based"""

def convert_to_lowercase(x):
  if isinstance(x, str):
    return x.lower()
  return ''

shared_articles["title"] = shared_articles["title"].apply(convert_to_lowercase)

count = CountVectorizer(stop_words = 'english')
count_met = count.fit_transform(shared_articles["title"])

cosine_sim = cosine_similarity(count_met, count_met)
shared_articles = shared_articles.reset_index()
indices = pd.Series(shared_articles.index, index = shared_articles["contentId"])

def getRecomm(contentId, cosine_sim):
  index = indices[contentId]
  sim_score = list(enumerate(cosine_sim[index]))
  sim_score = sorted(sim_score, key = lambda x: x[1], reverse = True)
  sim_score = sim_score[1:11]
  movie_indices = [i[0] for i in sim_score]
  return shared_articles["contentId"].iloc[movie_indices]

shared_articles.to_csv('proccessed.csv')