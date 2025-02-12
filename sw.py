from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

if __name__ == '__main__':
    app.run(debug=True)
