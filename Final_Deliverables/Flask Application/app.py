from flask import Flask,request,render_template
import pickle
import cv2
from skimage import feature
import os.path

app = Flask(__name__)


@app.route('/')
def start():
    return render_template("index.html")
class my_dictionary(dict):
  def __init__(self):
    self = dict()
  def add(self, key, value):
    self[key] = value
database=my_dictionary()

@app.route('/form_reg',methods=['POST','GET'])
def reg():
    name2=request.form['userid']
    pwd1=request.form['pwd']
    if name2 in database:
        return render_template('index.html',info='Username Already Taken!')
    else:
        database.add(name2,pwd1)
        return render_template("index.html")



@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['userid']
    pwd=request.form['pwd']
    if name1 not in database:
        return render_template('index.html',info='Invalid User!!')
    else:
        if database[name1]!=pwd:
            return render_template('index.html',info='Invalid Password!')
        else:
	         return render_template('home.html',name=name1)

             
@app.route("/") 
def about():
    return render_template("home.html")

@app.route("/home") 
def home():
    return render_template("home.html")

@app.route("/upload")
def test():
    return render_template("predict.html")

@app.route("/logout")
def log():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f=request.files['file'] #requesting the file
        basepath=os.path.dirname(os.path.realpath('__file__'))#storing the file directory
        filepath=os.path.join(basepath,"uploads",f.filename)#storing the file in uploads folder
        f.save(filepath)  #saving the file

        #Loading the saved model
        print("Loading model for prediction")
        model = pickle.loads(open('parkinson.pkl', "rb").read())

        # Pre-processing the image before giving it to the model
        image = cv2.imread(filepath)
        output = image.copy()

        output = cv2.resize(output, (128, 128))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 200))
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        features = feature.hog(image, orientations=9,pixels_per_cell=(5, 5), cells_per_block=(2, 2),transform_sqrt=True, block_norm="L1")
        preds = model.predict([features])
        print(preds)
        r=["You are healthy !","You may have Parkinson's disease."]
        result = r[preds[0]] 
        return result
    return None

    
if __name__ == '__main__':
    app.run()