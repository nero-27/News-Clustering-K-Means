import io
import collections
import random
from flask import Flask, render_template, request, redirect, url_for , make_response       
from flask import Response, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from werkzeug import secure_filename
import os
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans 
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt





PEOPLE_FOLDER = os.path.join('static', 'photo')

app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route("/")                   # at the end point 
def index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'back1.png')
    return render_template("index.html", user_image = full_filename)
    
@app.route("/uploader" , methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      fname = f.filename
      k=5

      return redirect(url_for('preprocess',fname = fname,clst=k))


@app.route('/preprocess/<fname>/<clst>')
def preprocess(fname,clst):
  file = open(fname)
  text = file.read()
  k=int(clst)
  sentences = text.split('\n')

  tfidf_vectorizer=TfidfVectorizer(tokenizer=tokenizer, stop_words=stopwords.words('english'), lowercase=True)
  tfidf_matrix=tfidf_vectorizer.fit_transform(sentences)
  kmeans=KMeans(n_clusters=k)
  kmeans.fit(tfidf_matrix)

  clusters=collections.defaultdict(list)
  for i, label in enumerate(kmeans.labels_):
    clusters[label].append(i)
  f= open("sortedclst.txt","w+")
  for cluster in range(k):
    f.write(str(cluster)+" : ")
    for i, sentence in enumerate(clusters[cluster]):
      f.write(sentences[sentence]+",")
    f.write("\n")
  f.close()
  


  List=[]
  List = open("sortedclst.txt").readlines()
  cnt=0

  data = dict()
  cnt= len(List)
  for x in range(cnt):
   for l in List:   
       a=l.split(" : ")
       if x==int(a[0]):
         data[x] = a[1]




  random_state=0
  cls= MiniBatchKMeans(n_clusters=k, random_state=random_state)
  cls.fit(tfidf_matrix)
  #cls.predict(tfidf_matrix)
  #cls.labels_
  
  pca = PCA(n_components=2,random_state=random_state)
  reduced_features= pca.fit_transform(tfidf_matrix.toarray())

  reduced_cluster_centers = pca.transform(cls.cluster_centers_)
  plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.predict(tfidf_matrix))
  plt.scatter(reduced_cluster_centers[:,0],reduced_cluster_centers[:,1], marker='x', s=150,c='b')
  plt.savefig('plot.png')
  #plt.show()
  return render_template("table.html", aa=data)
  #return 'Hello %s as Guest' % fname 





def tokenizer(text):
  tokens=word_tokenize(text)
  stemmer=PorterStemmer()
  tokens=[stemmer.stem(t) for t in tokens if t not in stopwords.words('english')]
  return tokens

@app.route('/plot.png',methods = ['GET', 'POST'])
def plot_png():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')
    r = make_response(render_template("image.html", user_image = full_filename))

    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return render_template("image.html", user_image = full_filename)

# @app.after_request
# def add_header(response):
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Expires'] = '0'
#     return response
      #return "NO Image Found!!"


@app.route('/index.html')
def index_html():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'back1.png')
    return render_template("index.html", user_image = full_filename)



if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)


'''
from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))

if __name__ == '__main__':
   app.run(debug = True)
'''