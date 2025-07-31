from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import Error



app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'port': 5432,
    'user': 'postgres',
    'password': 'admin'
}



def get_connection():
    try:
        connection=psycopg2.connect(**DB_CONFIG)
        print("connection with database established successfully")
        return connection
    except Error as e:
        print("Error while connecting with the database")

def create_table():
    try:
        conn=get_connection()
        cursor=conn.cursor()
        create_table_query='''
            CREATE TABLE if not exist  ojoto_student (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            phone VARCHAR(20),
                            email VARCHAR(100),
                            roll_number varchar(20)
                        );
            '''
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print("error while creating the table")


def save_student(name, phone, email, roll_number):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        insert_query = '''
                        INSERT INTO ojoto_student (name, phone, email, roll_number) 
                        VALUES (%s, %s, %s, %s)
                       '''
        cursor.execute(insert_query,(name,phone,email,roll_number))
        conn.commit()
        conn.close()
    except Error as e:
        print("error while inserting")




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name=request.form['name']
    phone=request.form['phone']
    email=request.form['email']
    roll_number = request.form['roll_number']
    print("name is",name)
    print("phone is", phone)
    print("email is", email)
    print("roll_number is", roll_number)
    create_table()
    save_student(name,phone,email,roll_number)
    return f"Data saved successfully! Student: {name}"




if __name__ == '__main__':
    print("i am running this file directly")

    app.run(debug=True, host='0.0.0.0', port=5000)





















