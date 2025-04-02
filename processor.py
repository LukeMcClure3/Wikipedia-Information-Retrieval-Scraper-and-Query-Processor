from flask import Flask, request, render_template, session
import joblib
import numpy as np
import math
app = Flask(__name__)
index_file = "index.pkl"
#flask --app fltest run
# https://cloud.google.com/container-registry/docs/pushing-and-pulling
data = joblib.load(index_file)



@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/button", methods=["POST"])
def button():
    query = request.form.get('query').lower()
    
    return render_template("loading.html" , query = query)


@app.route("/results", methods=["GET", "POST"])
def results():
    query = request.args.get('query')
    
    # query = request.form.get('query').lower()
    
    # data = joblib.load(index_file)
    
    X = data["X"]
    feature_names = data["feature_names"]
    query_list = query.split()
    rankings = [1] * X.shape[0] 
    #print(X[0])
    query_vector = [0] * X.shape[1]
    query_word_ids = []
    for word in query_list:
        #search for word in inverted index, j=id
        j = np.where(feature_names == word)
        j=j[0]
        if (j.size!=0):
            j=j[0]
            query_word_ids.append(j)
            print(j, len(query_vector))
            query_vector[j] = 1
    sum = 0
    
    for i in range(len(rankings)):
        sum = 0
        doc_vector = []
        for id in query_word_ids:
            sum += X[i , id] 
            doc_vector.append(X[i , id] )
        if sum == 0:
            rankings[i] = -1
        else:
            rankings[i] = sum / (np.linalg.norm(X[i].data )*math.sqrt(len(query_word_ids)))
        
        
            

    rtn = "<h1>Input: {}</h1><br><br>".format(query)

    index_score =  [(i,rankings[i]) for i in range(len(rankings))]

    index_score.sort(key=lambda x: -x[1])
    used = set()
    for i in range(20):
        docID = index_score[i]
        x = data["data_link"][docID[0]]
        y=data["data_title"][docID[0]]
        if y not in used:
            used.add(y)
        rtn+=(" <a href = \"{}\">{}</a><br>".format(x ,y) )
        rtn += "<h2> {} </h2>".format( " "+ str(docID[1]))

    return rtn

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
# if __name__ == "__main__":
#     app.run(debug=True)