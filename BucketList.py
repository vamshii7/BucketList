from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="your-mysql-host",
    user="your-mysql-user",
    password="your-mysql-password",
    database="your-mysql-database"
)

cursor = db.cursor()

# Create a table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bucket_list (
        id INT AUTO_INCREMENT PRIMARY KEY,
        dream VARCHAR(255) NOT NULL
    )
""")
db.commit()

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        return add_dream()
    else:
        return print_dream()

def print_dream():
    html = '<html>'
    html += '<head><link rel="stylesheet" type="text/css" href="static/style.css"></head>'
    html += "<h3>The bucket list. Dream Big!</h3>"
    html += '''
        <form action="/" method="post">
        <label for="dream">Add item:</label>
        <input type="text" id="dream" name="dream"><br\ ><br\ >
        <input type="submit" value="Submit">
        </form> <br><br>
        '''
    html += "<h4>My bucket list:</h4>"

    # Fetch data from MySQL
    cursor.execute("SELECT dream FROM bucket_list")
    dreams = cursor.fetchall()

    if dreams:
        for dream in dreams:
            html += f"{dream[0]} <br \>"
    else:
        html += "The list is empty. Go ahead - add the first item!"

    html += '</html>'
    return html

def add_dream():
    dream = request.form.get('dream')
    
    # Insert data into MySQL
    cursor.execute("INSERT INTO bucket_list (dream) VALUES (%s)", (dream,))
    db.commit()

    html = print_dream()
    return html

if __name__ == '__main__':
    app.run(debug=True)
