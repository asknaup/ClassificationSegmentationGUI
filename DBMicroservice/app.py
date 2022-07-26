from flask import Flask, render_template, request, redirect
from flask_injector import FlaskInjector
from injector import inject
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'

# Initialize the database
db = SQLAlchemy(app)

# Create db model
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key = True) # id is column name
    category = db.Column(db.String(200), nullable = False) # 200 characters for string input
    date_created = db.Column(db.Date, default = date.today())
    price = db.Column(db.Numeric(precision=10, scale=2), nullable = False)
    notes = db.Column(db.String(250))

    # create a function to retunr a string when we add something
    def __repr__(self):
        return '<Item id %r>' % self.id

## TODO: run following code to create db, must be in this file dir
# python # open python terminal
# from app import db
# db.create_all()
# exit()

@app.route('/budget', methods=['POST', 'GET'])
def budget():
    title = "About my Budget!"

    if request.method == 'POST':
        category = request.form['category']
        date_create = request.form['date']
        price = float(request.form['price'])
        notes = request.form['notes']

        print(date_create)
        if date_create:
            date_create = datetime.strptime(date_create, '%Y-%m-%d').date()
        else:
            date_create = date.today()

        # add item to database
        newItem = Budget(
            category = category, 
            date_created = date_create,
            price = price,
            notes = notes) 

        # push to database
        try:
            db.session.add(newItem)
            db.session.commit()
            return redirect('/budget')
        except:
            return "There was an error adding item to the database"
    else:
        items = Budget.query.order_by(Budget.date_created)
        return render_template("budget.html", title = title, items = items)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)