from math import floor
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from scipy import sparse
import numpy as np

class vnchar:
    def __init__(self, num_chars=25, ignore_traits = [], verbose=True, exclude_same_vns=True, match_gender=True):
        self.num_chars = num_chars
        self.data = None
        self.model_knn = None
        self.knn_matrix = None
        self.verbose = verbose
        self.exclude_same_vns = exclude_same_vns
        self.match_gender = match_gender

        self.df_chars = None
        self.char_vns = None

        # Ignore these traits (primarily presentation-related)
        self.ignore_traits = ignore_traits

        self.load_data()
        
    def load_data(self):
        # Load the character info
        # Load the header
        with open('./data/chars.header', 'r') as f:
            header = f.read().split('\t')

        # Load the data
        self.df_chars = pd.read_csv('./data/chars', sep='\t', names=header)
        self.df_chars['id'] = self.df_chars['id'].apply(lambda x: int(x[1:]))

        # Replace \N with NaN for easier handling
        self.df_chars.replace(r'\\N', np.nan, regex=True, inplace=True)

        # Create a new column that contains the latin name if available, otherwise the regular name
        self.df_chars['lookup_name'] = np.where(self.df_chars['latin'].isna(), self.df_chars['name'], self.df_chars['latin'])



        # Read the VNs that the chars appear in
        if self.verbose:
            print("Loading char vns")
        self.char_vns = pd.read_csv('./data/chars_vns', sep='\t', names=['id', 'vid', 'rid', 'role', 'spoil'], na_values='\\N')

        # remove 'c' and 'v' from 'id' and 'vid' columns respectively and convert to int
        self.char_vns['id'] = self.char_vns['id'].apply(lambda x: int(x[1:])).astype(int)
        self.char_vns['vid'] = self.char_vns['vid'].apply(lambda x: int(x[1:])).astype(int)




        # Load the traits
        if self.verbose:
            print("Loading traits")
        self.data = pd.read_csv('./data/chars_traits', sep='	', header=None, names=['id', 'tid', 'spoiler', 'spoiler_level'])

        # Removing the initial 'c' from character id and converting to integer
        self.data['id'] = self.data['id'].apply(lambda x: int(x[1:]))
        self.data['tid'] = self.data['tid'].apply(lambda x: int(x[1:]))

        # Remove ignored traits
        self.data = self.data[~self.data['tid'].isin(self.ignore_traits)]

        # Instead of converting to dummies and creating a dense matrix, we'll create a sparse matrix
        # Here, we're using the 'coo_matrix' format, but other formats may be more suitable depending on the data
        # 'coo_matrix' stands for 'coordinate format', and is suitable for when we know the indices where the matrix has non-zero entries
        if self.verbose:
            print("Building knn sparse matrix")
        row  = self.data['id'].values
        col  = self.data['tid'].values  # Assuming tid is in the form 'iXXX'
        data = np.ones(len(row))  # Since all our entries are just presence/absence of traits, we can just use 1s
        matrix = sparse.coo_matrix((data, (row, col)))
        # Convert COO matrix to CSR format
        self.knn_matrix = matrix.tocsr()

        if self.verbose:
            print("Building kNN model")
        self.model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
        self.model_knn.fit(self.knn_matrix)

    def get_character_name(self, character_id):
        return self.df_chars[self.df_chars['id'] == character_id]['lookup_name'].values[0]
    
    def get_char_vns(self, character_id):
        # filter DataFrame by character id
        df_filtered = self.char_vns[self.char_vns['id'] == character_id]

        # return an array of VN ids
        return df_filtered['vid'].to_numpy()
        
    def min_max_normalize(self, series):
        return (series - series.min()) / (series.max() - series.min())
        
    def resize_list(self, l):
        init_size = len(l)
        for i in range(init_size, self.num_chars):
            l.append(0)
        if(len(l) > self.num_chars):
            l = l[:self.num_chars]
        return l
        
    def get_trait_recommendations_scores(self, character_id):
        # Get the gender for the specified character
        character_gender = self.df_chars[self.df_chars['id'] == character_id]['gender'].values[0]

        # Get num_chars * 10 to account for the fact that the closest characters may not share the same gender, as the queries are very fast.
        distances, indices = self.model_knn.kneighbors(self.knn_matrix[character_id].reshape(1, -1), n_neighbors = self.num_chars*10 + 1)
        recommended_characters = indices[0][1:]
        scores = 1 - distances[0][1:]

        # Get the VNs for the character
        character_vns = set(self.get_char_vns(character_id))

        # Function to check whether a character shares any VNs with the target character
        def shares_vn(other_character_id):
            other_character_vns = self.get_char_vns(other_character_id)
            return bool(character_vns & set(other_character_vns))

        # Create a DataFrame of recommended characters and their scores
        recommendations_df = pd.DataFrame({'id': recommended_characters, 'similarity': scores})

        # Filter the recommended characters to exclude those who have appeared in the same VN as the given character
        if self.exclude_same_vns:
            recommendations_df = recommendations_df[~recommendations_df['id'].apply(shares_vn)]

        if not self.match_gender:
            character_score_pairs = list(zip(recommendations_df['id'].values, recommendations_df['score'].values))
            return character_score_pairs

        # Merge with df_chars to get genders
        recommendations_df = recommendations_df.merge(self.df_chars[['id', 'gender']], on='id')

        # Filter to get only characters of the same gender
        if self.match_gender:
            same_gender_recommendations = recommendations_df[recommendations_df['gender'] == character_gender]

        # Return the top num_recommendations characters as a list of tuples
        same_gender_recommendations = same_gender_recommendations.nlargest(self.num_chars, 'similarity')[['id', 'similarity']]
        
        character_score_pairs = list(zip(same_gender_recommendations['id'].values, same_gender_recommendations['similarity'].values))
        
        return character_score_pairs
    
    def get_trait_recommendations(self, character_id):
        return self.resize_list([pair[0] for pair in self.get_trait_recommendations_scores(character_id)])