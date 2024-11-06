# This is the assignment, the other files are for the lesson.
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/fitness_center'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("name", "age", "id")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

class WorkoutSessionSchema(ma.Schema):
    member_id = fields.Integer(required=True)
    session_date = fields.Date(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)

    class Meta:
        fields = ("member_id", "session_date", "session_time", "activity", "session_id")

workoutsession_schema = WorkoutSessionSchema()
workoutsessions_schema = WorkoutSessionSchema(many=True)

class Member(db.Model):
    __tablename__ = 'Members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable = False)
    age = db.Column(db.Integer())

class WorkoutSession(db.Model):
    __tablename__ = 'WorkoutSessions'
    session_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id'))
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.String(100), nullable=False)
    activity = db.Column(db.String(255), nullable=False)


@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)

@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_member = Member(name=member_data['name'], age=member_data['age'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "New member added successfully."}), 201

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    member.name = member_data["name"]
    member.age = member_data["age"]
    db.session.commit()
    return jsonify({"message": "Member details updated successfully."})

@app.route("/members/<int:id>", methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': "Member removed successfully."}), 200

@app.route('/workoutsessions', methods=['GET'])
def get_workoutsessions():
    workoutsessions = WorkoutSession.query.all()
    return workoutsessions_schema.jsonify(workoutsessions)

@app.route('/workoutsessions', methods=['POST'])
def add_workoutsession():
    try:
        workoutsession_data = workoutsession_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_workoutsession = WorkoutSession(member_id=workoutsession_data['member_id'], session_date=workoutsession_data['session_date'], \
session_time = workoutsession_data['session_time'], activity=workoutsession_data['activity'])
    db.session.add(new_workoutsession)
    db.session.commit()
    return jsonify({"message": "New workout added successfully."}), 201

@app.route('/workoutsessions/<int:id>', methods=['PUT'])
def update_workoutsession(session_id):
    workoutsession = WorkoutSession.query.get_or_404(session_id)
    try:
        workoutsession_data = workoutsession_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    workoutsession.member_id = workoutsession_data["member_id"]
    workoutsession.session_date = workoutsession_data["session_date"]
    workoutsession.session_time = workoutsession_data["session_time"]
    workoutsession.activity = workoutsession_data["activity"]
    db.session.commit()
    return jsonify({"message": "Workout details updated successfully."})

@app.route("/workoutsessions/<int:id>", methods=['DELETE'])
def delete_workoutsession(id):
    workoutsession = WorkoutSession.query.get_or_404(id)
    db.session.delete(workoutsession)
    db.session.commit()
    return jsonify({'message': "Workout removed successfully."}), 200

@app.route('/workoutsessions/<int:member_id>', methods=['GET'])
def get_workoutsessions_by_member(member_id):
    workoutsessions = WorkoutSession.query.filter_by(member_id=member_id).all()
    return workoutsessions_schema.jsonify(workoutsessions)


if __name__ == '__main__':
    app.run(debug=True)