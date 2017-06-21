from flask import Flask, render_template, session, redirect, url_for, escape, request
import sqlite3 as sql
app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/')
def home():
   return render_template('home.html')
   
@app.route('/list')
def list():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from bunga")
   
   rows = cur.fetchall();
   return render_template('list.html', rows = rows)

@app.route('/listadmin')
def listadmin():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from bunga")
   
   rows = cur.fetchall();
   return render_template('listadmin.html', rows = rows)
   
@app.route('/deletepesanan',methods = ['POST', 'GET'])
def deletepesanan():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   pesanId = request.form['postPesananId']

   cur = con.cursor()
   print(pesanId)
   cur.execute("delete from pesan where pesanId=?", (pesanId,))
   con.commit()

   return order()
   
@app.route('/deletebunga',methods = ['POST', 'GET'])
def deletebunga():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   bungaId = request.form['postBungaId']

   cur = con.cursor()
   print(bungaId)
   cur.execute("delete from bunga where bungaId=?", (bungaId,))
   con.commit()

   return listadmin()
   
@app.route('/order')
def order():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   username = session['username']

   cur = con.cursor()
   cur.execute("select * from user where email=?", [username])
   rows = cur.fetchone();
   userId = rows['userId']
   
   cur.execute("select * from bunga")
   rows = cur.fetchall();
   print(rows)
   cur.execute("select * from pesan where userId=?", (userId,))
   rows2 = cur.fetchall();
   print(rows2)
   return render_template('order.html',rows=rows, rows2=rows2)

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/addbunga')
def addbunga():
   return render_template('addbunga.html')

@app.route('/detailbunga',methods = ['POST', 'GET'])
def detailbunga():
   id = request.args.get('id')
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from bunga where bungaId=?", id)

   rows = cur.fetchone();
   
   return render_template('detailBunga.html', row = rows)

@app.route('/pesanbunga',methods = ['POST', 'GET'])
def pesanbunga():
   if request.method == 'POST':
      try:
         username = session['username']
         bungaId = request.form['postBungaId']
         print(bungaId)
         con = sql.connect("tos.db")
         con.row_factory = sql.Row 
   
         cur = con.cursor()
         cur.execute("select * from user where email=?", [username])
         rows = cur.fetchone();
         userId = rows['userId']
         with sql.connect("tos.db") as con:
            cur = con.cursor()
            print(userId)
            print(bungaId)
            cur.execute("INSERT INTO pesan (bungaId, userId) VALUES (?,?)",(bungaId, userId))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return list()

@app.route('/tambahbunga',methods = ['POST', 'GET'])
def tambahbunga():
   if request.method == 'POST':
      try:
         name = request.form['postName']
         description = request.form['postDescription']
         imageUrl = request.form['postImageUrl']
         star = request.form['postStar']
         price = request.form['postPrice']
         
         with sql.connect("tos.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO bunga (name, description, imageUrl, star, price) VALUES (?,?,?,?,?)",(name, description, imageUrl, star, price) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return home()
         
@app.route('/edit',methods = ['POST', 'GET'])
def edit():
   con = sql.connect("tos.db")
   con.row_factory = sql.Row
   bungaId = request.form['postBungaId']

   cur = con.cursor()
   cur.execute("select * from bunga where bungaId=?", [bungaId])
   row = cur.fetchone();
   
   cur.execute("select * from bunga where bungaId=?",[bungaId])
   row = cur.fetchall();
   print(row)
  
   return render_template("edit.html",rows = row)
   
@app.route('/editbunga',methods = ['POST', 'GET'])
def editbunga():
   if request.method == 'POST':
      try:
         name = request.form['postName']
         description = request.form['postDescription']
         imageUrl = request.form['postImageUrl']
         star = request.form['postStar']
         price = request.form['postPrice']
         bungaId = request.form['postBungaId']
         print name, description, imageUrl, star, price, bungaId
         
         con = sql.connect("tos.db")
         cur = con.cursor()

         cur.execute("UPDATE bunga SET name=?, description=?, imageUrl=?, star=?, price=? WHERE bungaId=?",(name, description, imageUrl, star, price, bungaId))
             
         con.commit()
      except Exception as e:
         print e
         con.rollback()
      finally:
         return listadmin()
         
@app.route('/formregister',methods = ['POST', 'GET'])
def formregister():
   if request.method == 'POST':
      try:
         email = request.form['postEmail']
         password = request.form['postPassword']
         
         with sql.connect("tos.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO user (email, password) VALUES (?,?)",(email,password) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return home()
         

@app.route('/formlogin',methods = ['POST', 'GET'])
def formlogin():
   if request.method == 'POST':
      email = request.form['postEmail']
      password = request.form['postPassword']
      con = sql.connect("tos.db")
      con.row_factory = sql.Row
   
      cur = con.cursor()
      cur.execute('SELECT COUNT(*) FROM user WHERE email=? AND password=?', (email, password))
   
      rows = cur.fetchone()

      if rows[0] == 1:
         session['username'] = request.form['postEmail']

         return home()
      else:
         return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return home()
@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
   app.debug = True
   app.run('0.0.0.0', 5507)
