import pandas as pd
from surprise import SVD, Reader, Dataset 
from surprise.model_selection import cross_validate
import sys
import pickle

model_path = 'model.pkl'

if len(sys.argv) == 2:
    dataset_path = sys.argv[1]

    column_names=['userId','productId','rating','timestamp']
    df=pd.read_csv(dataset_path, names=column_names)
    
    print("Dataset was loaded")

    svd = SVD()
    reader = Reader()

    data = Dataset.load_from_df(df[['userId', 'productId', 'rating']], reader)
    trainset = data.build_full_trainset()

    print("Start model training")
    svd.fit(trainset)
    print("End model training, saving model to %s file path" % model_path)
    
    with open(model_path, 'wb') as model_file:
        pickle.dump(svd, model_file)

else:
    print("The path to the dataset was not given in argument")