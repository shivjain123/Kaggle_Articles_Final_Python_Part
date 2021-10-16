import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

shared_articles = pd.read_csv('shared_articles_proccessed.csv')
shared_articles = shared_articles[shared_articles['title'].notna()]

count = CountVectorizer(stop_words='english')
count_met = count.fit_transform(shared_articles["title"])

cosine_sim = cosine_similarity(count_met, count_met)
shared_articles = shared_articles.reset_index()
indices = pd.Series(shared_articles.index, index=shared_articles["contentId"])

def getRecomm(contentId, cosine_sim):
  index = indices[contentId]
  sim_score = list(enumerate(cosine_sim[index]))
  sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
  sim_score = sim_score[1:11]
  movie_indices = [i[0] for i in sim_score]
  return shared_articles[["url", "title", "text", "lang", "total_events"]].iloc[movie_indices].values.tolist()