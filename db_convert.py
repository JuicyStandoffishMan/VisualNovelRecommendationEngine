from vnrec import vn
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import os

user = 'vnlikeor_admin'
passw = os.environ.get['vndb_pass']
host = 'localhost'
port = 3306
database = 'vnlikeor_vndb'

engine = create_engine(f"mysql+mysqlconnector://{user}:{passw}@{host}:{port}/{database}")
with engine.connect() as c:


    #
    # vn_titles
    #
    df_names = pd.read_csv('./data/vn_titles', sep='	', header=None, names=['id', 'lang', 'official', 'title', 'latin'])
    df_names['id'] = df_names['id'].str.slice(1)
    df_names['id'] = df_names['id'].astype(int)

    # Insert data into the vn_titles table
    df_names.to_sql('vn_titles', engine, if_exists='replace', index=False)

    c.execute(text("DROP TABLE IF EXISTS recommendations"))

    vn = vn(num_vns=100)
    sql = "CREATE TABLE recommendations (vn_id INT, cat INT, "
    for i in range(0, vn.num_vns - 1):
        sql += "rec_" + str(i) + " INT, "
    sql += "rec_" + str(vn.num_vns) + " INT)"
    c.execute(text(sql))

    base_sql = "INSERT INTO recommendations (vn_id, cat, "
    for i in range(0, vn.num_vns - 1):
        base_sql += "rec_" + str(i) + ", "
    base_sql += "rec_" + str(vn.num_vns) + ") VALUES ("

    # Fetch and store recommendations
    for vn_id in range(1, vn.get_last_vn_id() + 1):
        recommendations = {
            0: vn.get_user_recommendations(vn_id),
            1: vn.get_tag_recommendations(vn_id),
            2: vn.get_combined_recommendations(vn_id)
        }
        
        for category, recs in recommendations.items():
            rec_id = 0
            sql = base_sql + str(vn_id) + ", " + str(category) + ", "
            for rec in recs:
                if rec_id == vn.num_vns - 1:
                    sql += str(rec)
                else:
                    sql += str(rec) + ", "
                rec_id += 1
            sql += ")"
            c.execute(text(sql))
        
        print("Finished VN " + str(vn_id))

    # Commit the changes
    c.commit()