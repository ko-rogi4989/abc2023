from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデルの定義
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

class RefreshToken(db.Model):
    __tablename__ = 'RefreshToken'
    id = db.Column(db.BigInteger, primary_key=True)
    userId = db.Column(db.BigInteger, db.ForeignKey('User.id'))
    hashedToken = db.Column(db.String(255))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

# Flaskのルート定義
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(name=data['name'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name}), 201

@app.route('/refresh_tokens', methods=['POST'])
def create_refresh_token():
    data = request.json
    refresh_token = RefreshToken(userId=data['userId'], hashedToken=data['hashedToken'])
    db.session.add(refresh_token)
    db.session.commit()
    return jsonify({'id': refresh_token.id, 'userId': refresh_token.userId}), 201

# エラーハンドリング
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    db.create_all()  # データベーステーブルを作成する
    app.run(debug=True)