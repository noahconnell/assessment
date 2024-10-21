from flask import Flask, render_template, request, g
import sqlite3   #for the database stuff

app = Flask(__name__)

#the path and filename for the database
DATABASE = "U:\\Profile\\Documents\\Toy_Library_2\\Toy_Library_database.db"

#cool function to automatcally connect and query
def get_db():
    db = sqlite3.connect(DATABASE)
    return db

#routes go here
@app.route('/members')
def members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Members")
    results = cursor.fetchall()
    return render_template('members.html',results=results)

@app.route('/items')
def items():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Items")
    results = cursor.fetchall()
    return render_template('items.html',results=results)

@app.route('/rentals')
def rentals():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Rentals")
    results = cursor.fetchall()
    return render_template('rentals.html',results=results)

@app.route('/member_search', methods=('GET', 'POST'))
def member_search():
    if request.method == 'POST':
        member = request.form['member']
        search_term = '%'+member+'%'
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Members WHERE Name LIKE ?',(search_term, ))
        results = cursor.fetchall()
        return render_template('members.html', results=results, member=member)
    return render_template('search.html')

@app.route('/on_rent')
def on_rent():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Rentals.Name, Rentals.Item, Rentals.Returned_Date FROM Rentals WHERE Rentals.Returned_Date IS NULL")
    results = cursor.fetchall()
    return render_template('on_rent.html',results=results)

@app.route('/oneyear_members')
def oneyear_members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Members.Name, Members.Period FROM Members WHERE Members.Period = '1Y'")
    results = cursor.fetchall()
    return render_template('oneyear_members.html',results=results)

@app.route('/sixmonth_members')
def sixmonth_members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Members.Name, Members.Period FROM Members WHERE Members.Period = '6M'")
    results = cursor.fetchall()
    return render_template('sixmonth_members.html',results=results)

@app.route('/people_renting_games')
def people_renting_games():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Rentals.Name, Items.Item, Items.Type FROM Items, Rentals WHERE Items.Type = 'Game' AND Items.Item = Rentals.Item")
    results = cursor.fetchall()
    return render_template('people_renting_games.html',results=results)

@app.route('/people_renting_toys')
def people_renting_toys():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Rentals.Name, Items.Item, Items.Type FROM Items, Rentals WHERE Items.Type = 'Toy' AND Items.Item = Rentals.Item")
    results = cursor.fetchall()
    return render_template('people_renting_toys.html',results=results)

@app.route('/add_mem', methods=('GET', 'POST'))
def member_add():
    if request.method == 'POST':
        member_name = request.form['member_name']
        member_address = request.form['member_address']
        member_email = request.form['member_email']
        member_phone = request.form['member_phone']
        member_start_date = request.form['member_start_date']
        member_period = request.form['member_period']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO Members (Name, Address, Email, Phone, Start_Date, Period) VALUES (?, ?, ?, ?, ?, ?);',(member_name, member_address, member_email, member_phone, member_start_date, member_period, ))
        results = cursor.fetchall()
        return render_template('members.html', results=results, member_name=member_name, member_address=member_address, member_email=member_email, member_phone=member_phone, member_start_date=member_start_date, member_period= member_period)
    return render_template('add_member.html')


#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(port=8080, debug=True)