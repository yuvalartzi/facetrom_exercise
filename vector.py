import numpy as np
import pandas as pd
from sqlalchemy.orm import sessionmaker

import db
from config import Config

Session = sessionmaker(bind=db.engine)
session = Session()


def create_facial_vectors():
    vectors = np.random.uniform(0.0, 100.0, (Config.IMAGES_NUM, Config.M, Config.DIME_POINT))

    for image in range(Config.IMAGES_NUM):
        for cell in range(Config.M):
            x = vectors[image, cell, 0]
            y = vectors[image, cell, 1]
            fv = db.FacialVectors(image, cell, x, y, None, None, None, None)
            session.add(fv)

    session.commit()


def calc_mean_and_std():
    df = pd.read_sql_query(sql="select * from facial_vectors;", con=db.engine)

    for image in range(Config.IMAGES_NUM):
        i_df = df.loc[df['f_id'] == image]

        df.loc[(df['f_id'] == image), 'x_mean'] = i_df['x'].mean()
        df.loc[(df['f_id'] == image), 'y_mean'] = i_df['y'].mean()
        df.loc[(df['f_id'] == image), 'x_std'] = i_df['x'].std()
        df.loc[(df['f_id'] == image), 'y_std'] = i_df['y'].std()

    df.to_sql('facial_vectors', db.engine, if_exists='replace')


def get_exceptional_images():
    sql = """
        select f_id, cell from facial_vectors
        where x_mean - x_std > x or x > x_mean + x_std or y_mean - y_std > y or y > y_mean + y_std;
    """
    df = pd.read_sql_query(sql=sql, con=db.engine)

    res = {}

    for index, row in df.iterrows():
        if row['f_id'] in res:
            res[row['f_id']].append(row['cell'])
        else:
            res[row['f_id']] = [row['cell']]

    return np.array(list(res.items()))
