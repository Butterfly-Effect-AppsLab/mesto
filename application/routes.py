from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Users, Stop, Line, Platform, LineDirection, LinePlatform
from flask import jsonify
from datetime import datetime
import json


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

    return jsonify({'lines': output}), 200


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


@app.route('/favourites/line', methods=['POST'])
def favourite_lines():
    # id_user = request.form['id_user']
    # id_platform = request.form['id_platform']
    # id_line = request.form['id_line']
    # id_direction = request.form['id_direction']
    #
    # new_f_line = Favourite_line(id_user, id_platform, id_line, id_direction)
    # db.session.add(new_f_line)
    # db.session.commit()
    return "Line has been added to favourites", 201


@app.route('/favourites/stop', methods=['POST'])
def favourite_stops():
    # id_user = request.form['id_user']
    # id_platform = request.form['id_platform']
    # id_line = request.form['id_line']
    # id_direction = request.form['id_direction']
    #
    # new_f_line = Favourite_line(id_user, id_platform, id_line, id_direction)
    # db.session.add(new_f_line)
    # db.session.commit()
    return "Stop has been added to favourites", 201


@app.route('/lines/line/<line_name>/<int:line_direction>', methods=['GET'])
def test(line_name, line_direction):
    linka = line_name
    smer = line_direction
    lines_data = []
    datas = db.session.query(LinePlatform)
    name = {}
    for data in datas:
        if data.line_direction.line.line_name == linka:
            name['line_name'] = data.line_direction.line.line_name
            if data.line_direction.id_stop == smer:
                name['line_direction'] = data.line_direction.stop.stop_name
    stops = []
    x = 1
    for data in datas:
        if data.line_direction.id_stop == smer and data.line_direction.line.line_name == linka:
            x = {
                'stop_name': data.platform.stop.stop_name,
                'time': data.time_span,
                'request_stop': False
            }
            stops.append(x)

    lines_data.append(name)
    # lines_data.append(stops)
    name['stops'] = stops

    return jsonify(lines_data)

