from sklearn.feature_extraction.text import TfidfVectorizer

import json
import joblib
input_file = "small.json"
output_file = "index2.pkl"

vectorizer = TfidfVectorizer()

with open(input_file , 'r') as f :
    data = json.load(f)
    print(type(data))
print(len(data))
data_content = list(map(lambda x : x["content"] , data))
data_title = list(map(lambda x : x["title"] , data))
data_link = list(map(lambda x : x["link"] , data))

#print(data_content[0])
X = vectorizer.fit_transform(data_content)
print(X.shape) #(doucments , terms)
feature_names = vectorizer.get_feature_names_out()
pickle = {"feature_names" : feature_names , "X" : X, "data_title" : data_title, "data_link" : data_link}
joblib.dump(pickle, output_file)