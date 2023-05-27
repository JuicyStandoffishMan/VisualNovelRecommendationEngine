from vnrec import vn
import sqlite3

engine = vn(num_vns=100)

print("Num VNs:" + str(engine.get_last_vn_id()))

# Connect to the database
conn = sqlite3.connect('rec.db')
c = conn.cursor()

# Check if recommendations table exists
c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='recommendations' ''')

# Delete it if it exists
if c.fetchone()[0] == 1:
    c.execute('''DROP TABLE recommendations''')

create_table_str = f'''
CREATE TABLE recommendations (
    vn_id INT,
    category TEXT,
'''

for i in range(1, engine.num_vns + 1):
    create_table_str += f'rec_{i} INT'
    if i != engine.num_vns + 1:
        create_table_str += ','

create_table_str += '''
    PRIMARY KEY (vn_id, category)
)
'''
c.execute(create_table_str)

# Insert the data
for vn_id in range(1, engine.get_last_vn_id() + 1):  # Replace with the list or range of your vn_ids
    recommendations = {
        'user_ratings': engine.get_user_recommendations(vn_id),
        'tags': engine.get_tag_recommendations(vn_id),
        'combined': engine.get_combined_recommendations(vn_id)
    }

    print(f'Inserting recommendations for VN_ID {vn_id}...')
    
    for category, recs in recommendations.items():
        query = f'''
            INSERT INTO recommendations (vn_id, category, {', '.join(f'rec_{i+1}' for i in range(engine.num_vns))})
            VALUES (?, ?, {', '.join('?' for _ in range(engine.num_vns))})
        '''
        c.execute(query, (vn_id, category, *recs))

# Commit the changes and close the connection
conn.commit()
conn.close()

