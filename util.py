from tokenize import Double
import pandas as pd
import pymysql
from sklearn.neighbors import NearestNeighbors
import numpy as np

def kNN(conn,lang):
    try:
        query="select id,mail"
        for l in lang:
            query=query+",(Select score from score where technologyId=(Select id from technology where technology='"+l+"') and score.coderId = coders.id) as '"+l+"'"
        query=query+" from coders"


        sql_query = pd.read_sql_query (query, conn)
        df = pd.DataFrame(sql_query)
        df.fillna(0,inplace=True)

        for l in lang:
            df[l]=df[l].astype(float)
            df=df[df[l]>=60]


        knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
        knn.fit(df.drop(["mail","id"],axis=1).values)

        n_people_to_recommend = 10

        if(df.shape[0]>=n_people_to_recommend):
            distances , indices = knn.kneighbors([[100 for i in range(len(lang))]],n_neighbors=n_people_to_recommend+1)
            rec_people_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
            print(rec_people_indices)
            recommend_frame = []
            for val in rec_people_indices:
                # people_idx = df.iloc[val[0]]['id']
                # idx = df[df['id'] == people_idx].index
                recommend_frame.append({'mail':df.iloc[val[0]]['mail'],'Distance':val[1]})
            df2 = pd.DataFrame(recommend_frame,index=range(1,n_people_to_recommend+1))
            return df2["mail"].to_list()
        else:
            return df["mail"].to_list()
    except Exception as e:
        print(e)

#db connect
hostname = 'localhost'
username = 'root'
password = ''
database = 'mingleBox'
myconn = pymysql.connect( host=hostname, user=username, passwd=password, db=database ,cursorclass=pymysql.cursors.DictCursor)
conn = myconn.cursor()
kNN(myconn,["python"])