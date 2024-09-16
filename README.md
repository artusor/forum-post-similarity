# Natural Language Processing Using Public Forum Data
###### Jul 2020 - Sep 2020
Scraped posts from multiple discourse forums using a web driver and used TF-IDF vectorization to then determine cosine similarity in order to recommend the most similar posts (across forums) to a given post chosen at random.

The data is scraped, cleaned, and organized in `getting-data.py`, while `tfidf-cossim.ipynb` includes the TF-IDF vectorization process and example results of most similar post recommendation using cosine similarity.
