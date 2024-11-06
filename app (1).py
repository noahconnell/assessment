from flask import Flask, render_template, request, g
import sqlite3   #for the database stuff

app = Flask(__name__)

#the path and filename for the database
DATABASE = "C:\\Users\\noahr\\OneDrive\\Documents\\Toy_Library_2\\Toy_Library_Database.db"


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
    cursor.close()
    return render_template('members.html',results=results)

@app.route('/items')
def items():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Items")
    results = cursor.fetchall()
    cursor.close()
    return render_template('items.html',results=results)

@app.route('/rentals')
def rentals():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Rentals")
    results = cursor.fetchall()
    cursor.close()
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
        cursor.close()
        return render_template('members.html', results=results, member=member)
    return render_template('search.html')

@app.route('/on_rent')
def on_rent():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Rentals.Name, Rentals.Item, Rentals.Returned_Date FROM Rentals WHERE Rentals.Returned_Date IS NULL")
    results = cursor.fetchall()
    cursor.close()
    return render_template('on_rent.html',results=results)

@app.route('/oneyear_members')
def oneyear_members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Members.Name, Members.Period FROM Members WHERE Members.Period = '1Y'")
    results = cursor.fetchall()
    cursor.close()
    return render_template('oneyear_members.html',results=results)

@app.route('/sixmonth_members')
def sixmonth_members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Members.Name, Members.Period FROM Members WHERE Members.Period = '6M'")
    results = cursor.fetchall()
    cursor.close()
    return render_template('sixmonth_members.html',results=results)

@app.route('/people_renting_games')
def people_renting_games():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Rentals.Name, Items.Item, Items.Type FROM Items, Rentals WHERE Items.Type = 'Game' AND Items.Item = Rentals.Item")
    results = cursor.fetchall()
    cursor.close()
    return render_template('people_renting_games.html',results=results)

@app.route('/people_renting_toys')
def people_renting_toys():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT Rentals.Name, Items.Item, Items.Type FROM Items, Rentals WHERE Items.Type = 'Toy' AND Items.Item = Rentals.Item")
    results = cursor.fetchall()
    cursor.close()
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
        db.commit()
        cursor.close()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members")
        results = cursor.fetchall()
        cursor.close()
        return render_template('members.html', results=results, member_name=member_name, member_address=member_address, member_email=member_email, member_phone=member_phone, member_start_date=member_start_date, member_period= member_period)
    return render_template('add_member.html')

@app.route('/delete_mem', methods=('GET', 'POST'))
def member_delete():
    if request.method == 'POST':
        member_name = request.form['member_name']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM Members WHERE Name = ?', (member_name,))
        db.commit()
        cursor.close()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Members")
        results = cursor.fetchall()
        cursor.close()
        return render_template('members.html', results=results, deleted_member_name=member_name)
    return render_template('delete_member.html')

@app.route('/add_rent', methods=('GET', 'POST'))
def rental_add():
    if request.method == 'POST':
        rental_name = request.form['rental_name']
        rental_item = request.form['rental_item']
        rental_rental_date = request.form['rental_rental_date']
        rental_returned_date = request.form['rental_returned_date']
        rental_cost = request.form['rental_cost']
        rental_late_fee = request.form['rental_late_fee']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO Rentals (Name, Item, Rental_Date, Returned_Date, Rental_Cost, Late_Fee) VALUES (?, ?, ?, ?, ?, ?);',(rental_name, rental_item, rental_rental_date, rental_returned_date, rental_cost, rental_late_fee))
        db.commit()
        cursor.close()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Rentals")
        results = cursor.fetchall()
        cursor.close()
        return render_template('rentals.html', results=results, rental_name = rental_name, rental_item = rental_item, rental_rental_date = rental_rental_date, rental_returned_date = rental_returned_date, rental_cost = rental_cost, rental_late_fee = rental_late_fee)
    return render_template('add_rental.html')

@app.route('/add_item', methods=('GET', 'POST'))
def item_add():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_type = request.form['item_type']
        purchase_price = request.form['purchase_price']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO Items (Item, Type, Purchase_Price) VALUES (?, ?, ?);', (item_name, item_type, purchase_price))
        db.commit()
        cursor.close()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Items")
        results = cursor.fetchall()
        cursor.close()
        return render_template('items.html', results=results, item_name=item_name, item_type=item_type, purchase_price=purchase_price)
    return render_template('add_item.html')


#this bit of code runs the app that we just made with debug on
if __name__ == "__main__":
    app.run(port=8080, debug=True)