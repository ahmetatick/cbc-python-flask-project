from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__) 

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "batch_4"

mysql = MySQL(app)

@app.route('/') 
def home_page(): 
    return render_template("home.html", home_message = "Home page!")


@app.route('/upload_data/', methods=['POST', 'GET'])
def upload_data():
    if request.method == "POST": 
        cur = mysql.connection.cursor()
        user_name = request.form["us_name"]
        user_age = request.form["us_age"]
        user_city = request.form["us_city"]
        user_hobby = request.form["us_hobby"]

        my_insert_query = "INSERT INTO user_info VALUES ('{0}', {1}, '{2}', '{3}');".format(user_name, user_age, user_city, user_hobby)
        cur.execute(my_insert_query)
        mysql.connection.commit()
        return render_template('upload_data.html' , upload_message = 'Data Submitted Successfully')
    else:
        return render_template('upload_data.html')
    
@app.route('/all_data/') 
def all_data(): 
    select_query = "SELECT * FROM user_info;"
    cur = mysql.connection.cursor()
    cur.execute(select_query)
    all_data = cur.fetchall()
    return render_template("data.html", the_data = list(all_data))

@app.route('/filtered_data/', methods=['POST', 'GET']) 
def data_filtered():
    if request.method == "POST":
        user_name = request.form["us_name"]
        user_age = request.form["us_age"]
        user_city = request.form["us_city"]
        user_hobby = request.form["us_hobby"]

        select_query = "SELECT * FROM user_info WHERE user_name = '{0}' OR user_age = '{1}' OR user_city = '{2}' OR user_hobby = '{3}';".format(user_name,user_age,user_city,user_hobby)
        cur = mysql.connection.cursor()
        cur.execute(select_query)
        all_data = cur.fetchall()
        return render_template("filtered_data.html", the_data = list(all_data))
    else:
        select_query = "SELECT * FROM user_info;"
        cur = mysql.connection.cursor()
        cur.execute(select_query)
        all_data = cur.fetchall()
        return render_template("filtered_data.html", the_data = list(all_data))

if __name__ == '__main__': 
	app.run(port=4005, debug=True)