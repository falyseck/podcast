from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)

DATABASE = 'comments.db'

# Function to connect to the SQLite database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Create table for comments if it doesn't exist
def create_table():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS comments
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         text TEXT NOT NULL,
                         user TEXT NOT NULL);''')

# Route to get all comments
@app.route('/comments', methods=['GET'])
def get_comments():
    cursor = get_db().execute('SELECT * FROM comments')
    comments = cursor.fetchall()
    return jsonify([{'id': row[0], 'text': row[1], 'user': row[2]} for row in comments])

# Route to add a comment
@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    text = data['text']
    user = data['user']
    with get_db() as conn:
        conn.execute('INSERT INTO comments (text, user) VALUES (?, ?)', (text, user))
    return jsonify({'status': 'Comment added'}), 201

# Route to delete a comment (admin only)
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    with get_db() as conn:
        conn.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    return jsonify({'status': 'Comment deleted'})

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
