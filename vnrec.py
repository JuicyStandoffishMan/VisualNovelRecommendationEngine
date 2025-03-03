from math import floor
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class vn:
    def __init__(self, num_vns=25, tag_weight=1.5, vote_weight=1.0, tag_exp=2.0, vote_exp=1.0, ignore_tags = [32, 2040, 2461, 1434, 1431, 43], verbose=True, skip_recs=False):
        self.num_vns = num_vns
        self.tag_weight = tag_weight
        self.vote_weight = vote_weight
        self.tag_exp = tag_exp
        self.vote_exp = vote_exp
        self.average_ratings = None
        self.similarity_matrix = None
        self.df_names = None
        self.df_ratings = None
        self.df_tags = None
        self.verbose = verbose
        self.skip_recs = skip_recs

        # Ignore these tags (primarily presentation-related)
        self.ignore_tags = ignore_tags

        self.load_data()
        
    def load_data(self):
        # All the data loading code here
        if self.verbose:
            print("Loading titles")
        self.df_names = pd.read_csv('./data/vn_titles', sep='	', header=None, names=['VN_ID', 'Language', 'Official', 'Title', 'Latin Title'])
        self.df_names['VN_ID'] = self.df_names['VN_ID'].str.slice(1)
        self.df_names['VN_ID'] = self.df_names['VN_ID'].astype(int)

        if self.skip_recs:
            return

        # Read the text file
        if self.verbose:
            print("Loading votes")
        self.df_ratings = pd.read_csv('./data/votes', sep=' ', header=None, names=['VN_ID', 'user_ID', 'Rating', 'date'])
        self.df_ratings['Rating'] = np.sign(self.df_ratings['Rating']) * np.power(np.abs(self.df_ratings['Rating']), self.vote_exp)

        # Calculate average rating for each VN
        if self.verbose:
            print("Calculating average ratings")
        self.average_ratings = self.df_ratings.groupby('VN_ID')['Rating'].mean()

        # Load the tag data
        if self.verbose:
            print("Loading tags_vn")
        self.df_tags = pd.read_csv('./data/tags_vn', delimiter='\t', header=None, usecols=[1, 2, 4], names=['tag_ID', 'VN_ID', 'rating'])
        self.df_tags.loc[self.df_tags['tag_ID'].str.slice(1).astype(int).isin(self.ignore_tags), 'rating'] = 0
        self.df_tags['rating'] = np.sign(self.df_tags['rating']) * np.power(np.abs(self.df_tags['rating']), self.tag_exp)

        # Remove the first character from each ID
        self.df_tags['tag_ID'] = self.df_tags['tag_ID'].str.slice(1)
        self.df_tags['VN_ID'] = self.df_tags['VN_ID'].str.slice(1)

        # Convert the IDs and ratings to the correct data types
        self.df_tags['tag_ID'] = self.df_tags['tag_ID'].astype(int)
        self.df_tags['VN_ID'] = self.df_tags['VN_ID'].astype(int)
        self.df_tags['rating'] = self.df_tags['rating'].astype(float)

        # Calculate average vote for each tag for each VN
        if self.verbose:
            print("Building average tags")
        average_tag_votes = self.df_tags.groupby(['VN_ID', 'tag_ID'])['rating'].mean().reset_index()

        # Filter the DataFrame to remove rows with a rating of 0
        average_tag_votes = average_tag_votes[average_tag_votes['rating'] != 0]

        # Export to CSV
        # average_tag_votes.to_csv('average_tag_votes.csv', index=False)

        # Create a sparse matrix of VN x tag, with weights as values
        if self.verbose:
            print("Calculating tag similarity matrix.")
        data_sparse = csr_matrix((average_tag_votes['rating'], 
                                (average_tag_votes['VN_ID'], average_tag_votes['tag_ID'])))

        # Compute the cosine similarity matrix
        self.similarity_matrix = cosine_similarity(data_sparse, dense_output=False)
        if self.verbose:
            print("Similarity matrix computed.")
            print("Loading complete.")
            print("")

        # model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
        # model_knn.fit(data_sparse)

        # The similarity matrix is slow to build, but very fast to evaluate.
        # The knn model is fast to build, but takes even longer to evaluate than the similarity matrix.
        # A nzr dump is around 600MB and takes an insane amount of time to save.
        # A joblib dump is around 10GB and takes almost just as much time to load as it does to build.

    def get_average_rating(self, vn_id):
        vn_id = int(vn_id)
        if vn_id in self.average_ratings:
            return self.average_ratings[vn_id]
        else:
            return "No ratings available for this VN."
    
    def get_last_vn_id(self):
        # Get number of VNs per the self.df_names DataFrame by looking at the last element
        return self.df_names['VN_ID'].iloc[-1]

    def get_title(self, vn_id):
        # Filter the DataFrame for the given VN_ID
        vn_data = self.df_names[self.df_names['VN_ID'] == vn_id]

        # Check if there's an English title
        en_title = vn_data[vn_data['Language'] == 'en']['Title'].values
        if len(en_title) > 0:
            return en_title[0]

        # Check if there's a Latin Japanese title
        jp_title = vn_data[vn_data['Language'] == 'ja']['Latin Title'].values
        if len(jp_title) > 0 and jp_title != "\\N":
            return jp_title[0]

        # Check if there's a Japanese title
        jp_title = vn_data[vn_data['Language'] == 'ja']['Title'].values
        if len(jp_title) > 0:
            return jp_title[0]

        # Return the Latin official title if it exists
        official_title = vn_data[vn_data['Official'] == 't']['Latin Title'].values
        if len(official_title) > 0 and official_title != "\\N":
            return official_title[0]

        # Return the official title if it exists
        official_title = vn_data[vn_data['Official'] == 't']['Title'].values
        if len(official_title) > 0:
            return official_title[0]

        # Return None if no title is found
        return "v" + str(vn_id)
        
        
    def min_max_normalize(self, series):
        return (series - series.min()) / (series.max() - series.min())
        
    def get_user_recommendations_scores(self, vn_id):
        # Get all users who rated this VN
        users_who_rated = self.df_ratings[self.df_ratings['VN_ID'] == vn_id]['user_ID'].unique()

        # Get all VNs these users rated
        similar_vns = self.df_ratings[self.df_ratings['user_ID'].isin(users_who_rated) & (self.df_ratings['VN_ID'] != vn_id)]

        # Compute average rating and count of ratings for these VNs
        similar_vns_avg_rating = similar_vns.groupby('VN_ID')['Rating'].mean()
        similar_vns_rating_count = similar_vns.groupby('VN_ID')['Rating'].count()

        # Combine these into a DataFrame
        similar_vns_df = pd.DataFrame({'avg_rating': similar_vns_avg_rating, 'count_rating': similar_vns_rating_count})

        # Compute a score that combines the average rating and the count of ratings
        similar_vns_df['score'] = similar_vns_df['avg_rating'] * similar_vns_df['count_rating']

        # Now you can safely get the top num_vns rows
        return self.min_max_normalize(similar_vns_df['score'].nlargest(self.num_vns))


    def get_tag_recommendations_score(self, vn_id):
        # Get the row corresponding to the given VN
        vn_similarity = self.similarity_matrix[vn_id, :]

        # Get the indices of the top N most similar VNs
        most_similar = vn_similarity.toarray().argsort()[0][::-1][:self.num_vns+1]

        # Exclude the given VN
        most_similar = [vn for vn in most_similar if vn != vn_id]

        top_similar_scores = vn_similarity.toarray()[0][most_similar]
        return self.min_max_normalize(pd.Series(top_similar_scores, index=most_similar))

    def get_combined_recommendations_score(self, vn_id):
        # Get top recommendations and their scores from both models
        user_based_rec = self.get_user_recommendations_scores(vn_id)
        tag_based_rec = self.get_tag_recommendations_score(vn_id)

        # Weigh the scores
        user_based_rec = user_based_rec * self.vote_weight
        tag_based_rec = tag_based_rec * self.tag_weight

        # Combine the scores
        combined_scores = user_based_rec.add(tag_based_rec, fill_value=0)

        # Get the top_n recommendations based on the combined scores
        combined_rec = combined_scores.nlargest(self.num_vns)

        return combined_rec
    
    def resize_list(self, l):
        init_size = len(l)
        for i in range(init_size, self.num_vns):
            l.append(0)
        if(len(l) > self.num_vns):
            l = l[:self.num_vns]
        return l
    
    def get_user_recommendations(self, vn_id):
        return self.resize_list(self.get_user_recommendations_scores(vn_id).index.tolist())
    
    def get_tag_recommendations(self, vn_id):
        return self.resize_list(self.get_tag_recommendations_score(vn_id).index.tolist())
    
    def get_combined_recommendations(self, vn_id):
        return self.resize_list(self.get_combined_recommendations_score(vn_id).index.tolist())