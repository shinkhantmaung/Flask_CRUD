from flask import Flask,render_template,request,make_response,url_for
from werkzeug.utils import secure_filename
import os
import mysql.connector


app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = os.path.join('static\images')


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="python_crud"
)
mycursor = mydb.cursor()

msg = ''
tags = ''
def select(postid): 
    sql = "SELECT * FROM post WHERE id= %s"
    mycursor.execute(sql, (postid,))    
    myresult = mycursor.fetchall()
    return myresult

@app.route('/') 
def index(): 
    mycursor.execute("SELECT * FROM `post`")
    myresult = mycursor.fetchall() 
    return render_template('index.html', myresult=myresult,i=1) 
    
@app.route('/post')
def post(): 
	return render_template('post.html')

@app.route('/store', methods = ['POST', 'GET'])
def store():
	if request.method == 'POST': 
		title = request.form['title']
		author = request.form['author']
		category = request.form['category']
		date = request.form['date']
		photo = request.files['photo']
		status = request.form['status']
		content = request.form['content']

		filename = secure_filename(photo.filename)
		photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		sql = "INSERT INTO `post`(  `title`, `author`, `content`, `category`, `photo`, `date`, `status`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		val = (title,author,content,category,filename,date,status,)
		mycursor.execute(sql, val)
		mydb.commit()

		tags = "alert alert-primary alert-dismissible fade show"
		msg = "Successfully! Your post is successfully uploaded."
		return render_template('post.html',msg = msg,tags = tags)	
	else:
		tags = "alert alert-warning alert-dismissible fade show"
		msg = "Someting was Wrong! Please try again!"
		return render_template('post.html',msg = msg,tags = tags)

@app.route("/update/<string:id>",methods=['GET'])
def update(id):
    sql = "SELECT * FROM post WHERE id= %s"
    mycursor.execute(sql, (id,))    
    myresult = mycursor.fetchall()
    return render_template('update.html', myresult=myresult)

@app.route("/updatestore",methods=['POST', 'GET'])
def updatestore():
     if request.method == 'POST':
        msg = ''
        postid = request.form['id']
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        date = request.form['date']
        status = request.form['status']
        content = request.form['content']
        
        photo = request.files['photo']
        if not photo:
            # flash('Image not Found !')
            msg = "Failed! Image is not selected"
            msg_class = "alert alert-warning"
            return render_template('index.html',msg = msg,tags=msg_class)
        else:
            result = select(postid)
            image  = result[0][5]
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image))

            filename = secure_filename(photo.filename)
            file = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            photo.save(file)
            

        sql = "UPDATE `post` SET `title`=%s,`author`=%s,`content`=%s,`category`=%s,`photo`=%s,`date`=%s,`status`=%s WHERE id=%s"
        val = (title, author,content,category,filename,date,status,postid,)
        mycursor.execute(sql, val)  
        
        sql = "SELECT * FROM post "
        mycursor.execute(sql)    
        myresult = mycursor.fetchall()   

        mydb.commit()

        msg = "Successfully Updated"
        msg_class = "alert alert-info"
        return render_template('index.html',msg = msg,tags=msg_class,myresult=myresult)

        mydb.close()

@app.route("/delete/<string:postid>",methods=['GET'])
def delete(postid):
    result = select(postid)
    image  = result[0][5]
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image))
    
    sql = "DELETE FROM `post` WHERE id=%s"
    mycursor.execute(sql,(postid,))
    
    mycursor.execute("SELECT * FROM `post`")   
    myresult = mycursor.fetchall()  


    mydb.commit()
    msg = "Successfully Deleted"
    msg_class = "alert alert-danger"
    # print(mycursor.rowcount, "record inserted.")
    return render_template('index.html',msg = msg,tags=msg_class,myresult=myresult)

@app.route("/view")
def view():
    mycursor.execute("SELECT * FROM `post`")
    myresult = mycursor.fetchall() 
    return render_template('view.html', myresult=myresult) 

if __name__ == '__main__': 
	app.run(debug = True)
