from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Users, Stop, Line
from flask import jsonify
from datetime import datetime
from flask_restful import Resource, Api


@app.route('/stops', methods=['GET'])
def stops():

    stopss = Stop.query.all()

    output = []

    for sstop in stopss:
        stop_data = {}
        stop_data['name'] = sstop.stop_name
        output.append(stop_data)

    return jsonify({'stops': output}), 200


@app.route('/lines', methods=['GET'])
def lines():
    lines = Line.query.all()

    output = []

    for line in lines:
        line_data = {}
        line_data['name'] = line.line_name
        output.append(line_data)

    return jsonify({'lines': output})


@app.route('/user/add', methods=['POST'])
def add_user():
    id = request.form['id1']
    id2 = request.form['id2']
    onboard = request.form['on_type']
    os_type = request.form['os_type']

    new_user = Users(id, id2, onboard, os_type, datetime.now())
    db.session.add(new_user)
    db.session.commit()

    return 'User added to DB', 201


@app.route('/lines/line/<line_name>', methods=['GET'])
def line(line_name):
    line_1 = Line.query.filter_by(line_name=line_name).first()
    return str(line_1)


@app.route('/favourites/line', methods=['POST'])
def favourite_lines():
    d = request.json
    # store received data in DB
    #
    #
    return "Line has been added to favourites", 201


@app.route('/favourites/stop', methods=['POST'])
def favourite_stops():
    d = request.json
    # store received data in DB
    #
    #
    return "Stop has been added to favourites", 201

#
# @app.route('/stops', methods=['GET'])
# def stops():
#     return render_template('stops.html',
#                            stops=Stop.query.all(),
#                            title="Show Stops")


# @app.route('/lines', methods=['GET'])
# def lines():
#     return render_template('lines.html',
#                            lines=Line.query.all(),
#                            title="Show lines")
#
#
# @app.route('/stop', methods=['GET'])
# def stop():
#     # stps = []
#     wer = Stop.query.all()
#     result_list = []
#     for row in wer:
#         result_list.append({
#             'id': wer.id,
#             'name': wer.stop_name
#             })
#     return row

# class HelloWorld(Resource):
#     def get(self):
#         return {'hello' : 'world'}
#
# api.add_resource(HelloWorld, '/')
#
# wer = Stop.query.first()
#     return wer.stop_name
