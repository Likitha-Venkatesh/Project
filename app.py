from flask import Flask,render_template,request
from flask_mysqldb import *
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.metrics import AUC

app = Flask(__name__)
app.secret_key="signin"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'signin'
mysql=MySQL(app)
# print(mysql)

yieldmodel = pickle.load(open('yield.pkl', 'rb'))
cropmodel = pickle.load(open('crop.pkl', 'rb'))
model = load_model('plants.h5')

dependencies = {
    'auc_roc': AUC
}

verbose_name = {
 0:":Apple___Apple_scab",
 1:'Apple___Black_rot',
 2:'Apple___Cedar_apple_rust',
 3:'Apple___healthy',
 4:'Blueberry___healthy',
 5:'Cherry_(including_sour)___Powdery_mildew',
 6:'Cherry_(including_sour)___healthy',
 7:'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 8:'Corn_(maize)___Common_rust_',
 9:'Corn_(maize)___Northern_Leaf_Blight',
 10:'Corn_(maize)___healthy',
 11:'Grape___Black_rot',
 12:'Grape___Esca_(Black_Measles)',
 13:'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 14:'Grape___healthy',
 15:'Orange___Haunglongbing_(Citrus_greening)',
 16:'Peach___Bacterial_spot',
 17:'Peach___healthy',
 18:'Pepper,_bell___Bacterial_spot',
 19:'Pepper,_bell___healthy',
 20:'Potato___Early_blight',
 21:'Potato Late blight',
 22:'Potato___healthy',
 23:'Raspberry___healthy',
 24:'Soybean___healthy',
 25:'Squash___Powdery_mildew',
 26:'Strawberry___Leaf_scorch',
 27:'Strawberry___healthy',
 28:'Tomato___Bacterial_spot',
 29:'Tomato___Early_blight',
 30:'Tomato___Late_blight',
 31:'Tomato___Leaf_Mold',
 32:'Tomato___Septoria_leaf_spot',
 33:'Tomato___Spider_mites Two-spotted_spider_mite',
 34:'Tomato___Target_Spot',
 35:'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 36:'Tomato___Tomato_mosaic_virus',
 37:'Tomato___healthy'}

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')

@app.route('/login')
def loginpage():
    return render_template('Login.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register')
def register():
    return render_template('Register.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/yieldpredection')
def yieldpredection():
    return render_template('yieldpredection.html')

@app.route('/fertilizerRecommendation')
def fertilizerRecommendation():
    return render_template('fertilizerRecommendation.html')

@app.route('/plantdisease')
def plantdisease():
    return render_template('plantdisease.html')

@app.route('/validate',methods=['post'])
def validate():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    name=request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirmpassword = request.form['confirm']
    
    cursor.execute("SELECT * FROM user WHERE email = %s",(email,))
    if(cursor.fetchone()):
        return render_template('Login.html')
    else:
        cursor.execute("INSERT INTO user VALUES(%s,%s,%s,%s)",(name,email,password,confirmpassword))
        mysql.connection.commit()
        return render_template('Login.html')
    
    
@app.route('/savecontact',methods=['post'])
def savecontact():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    uname=request.form['uname']
    email = request.form['email']
    message = request.form['message']
    
    cursor.execute("INSERT INTO contact VALUES(%s,%s,%s)",(uname,email,message,))
    mysql.connection.commit()
    return render_template('contact.html',msg="Contact submitted")
    
@app.route('/reset',methods=['post'])
def reset():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    email = request.form['email']
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']
    
    cursor.execute("update user set password=%s where email=%s",(newpassword,email))
    mysql.connection.commit()
    return render_template('Login.html',msg="Password Reset Success")
    
@app.route('/login_validate',methods=['post'])
def login_validate():
    email=request.form['email']
    password=request.form['password']
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    email=request.form['email']
    pwd=request.form['password']
    cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s",(email,pwd,))
    if(cursor.fetchone()):
        return render_template("prediction.html")
    else:
        return 'login failed'


# with open('fertilizer.pk1', 'rb') as file:
#  model =pickle.load(file)

@app.route('/fertilizer',methods=['post'])
def fertilizer():
    values = [x for x in request.form.values()]
    print(values)
    arrvalues = np.array([values])
    
    ans = cropmodel.predict(arrvalues)
    print(ans)
    if ans[0] == 0:
        print("TEN-TWENTY SIX-TWENTY SIX")
        return render_template('fertilizerRecommendation.html', result="TEN-TWENTY SIX-TWENTY SIX")
    elif ans[0] == 1:
        print("Fourteen-Thirty Five-Fourteen")
        return render_template('fertilizerRecommendation.html', result="Fourteen-Thirty Five-Fourteen")
    elif ans[0] == 2:
        print("Seventeen-Seventeen-Seventeen")
        return render_template('fertilizerRecommendation.html', result="Seventeen-Seventeen-Seventeen")   
    elif ans[0] == 3:
        print("TWENTY-TWENTY")
        return render_template('fertilizerRecommendation.html', result="TWENTY-TWENTY")
    elif ans[0] == 4:
        print("TWENTY EIGHT-TWENTY EIGHT")
        return render_template('fertilizerRecommendation.html', result="TWENTY EIGHT-TWENTY EIGHT")
    elif ans[0] == 5:
        print("DAP")
        return render_template('fertilizerRecommendation.html', result="DAP")
    else:
        print("UREA")
        return render_template('fertilizerRecommendation.html', result="UREA")

# model1= pickle.load(open("yield.pkl","rb"))

@app.route('/yieldpred',methods=['post'])
def yieldpred():
    if request.method == "POST":
        print(request.form)
        State_Name = request.form['State_Name']
        Crop = request.form['Crop']
        Area = request.form['Area']
        Soil_type = request.form['soil_type']
         
        pred_args = [State_Name,Crop,Area,Soil_type]
        pred_args_arr = np.array(pred_args)
        pred_args_arr = pred_args_arr.reshape(1,-1)
        output = yieldmodel.predict(pred_args_arr)
        print(output)
        pred=format(int(output[0]))
        Yield= int(pred) / float(Area)
        yields= Yield*1000

    return render_template("yieldpredection.html",prediction_text=pred, yield_predictions= int(yields))

def predict_label(img_path):
	test_image = image.load_img(img_path, target_size=(224,224))
	test_image = image.img_to_array(test_image)/255.0
	test_image = test_image.reshape(1, 224,224,3)

	predict_x=model.predict(test_image) 
	classes_x=np.argmax(predict_x,axis=1)
	
	return verbose_name[classes_x[0]]

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/tests/" + img.filename	
		img.save(img_path)

		predict_result = predict_label(img_path)

	return render_template("plantdisease.html", prediction = predict_result, img_path = img_path)    


if __name__ == '__main__':
 app.run(debug=True)