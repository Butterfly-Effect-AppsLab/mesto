from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Users, Stop, Line, Platform, LineDirection, LinePlatform, Timetable, TimetableType
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
    line, direction = (db.session.query(Line, LineDirection)
                       .join(Line.directions)
                       .filter(
        Line.line_name == line_name,
        LineDirection.id_stop == line_direction)
                       .one())
    line_data = {
        'name': line.line_name,
        'direction': direction.stop.stop_name,
    }

    stops = []
    for platform in direction.platforms:
        stop = {
            'stop_name': platform.platform.stop.stop_name,
            'request_stop': platform.request_stop,
            'time': platform.time_span
        }
        stops.append(stop)

    line_data['stops'] = stops

    return jsonify(line_data)

# @app.route('/lines/line/<line_name>/<int:line_direction>', methods=['GET'])
# def test(line_name, line_direction):
#     linka = line_name
#     smer = line_direction
#     lines_data = []
#     datas = db.session.query(LinePlatform)
#     name = {}
#     for data in datas:
#         if data.line_direction.line.line_name == linka:
#             name['line_name'] = data.line_direction.line.line_name
#             if data.line_direction.id_stop == smer:
#                 name['line_direction'] = data.line_direction.stop.stop_name
#     stops = []
#     x = 1
#     for data in datas:
#         if data.line_direction.id_stop == smer and data.line_direction.line.line_name == linka:
#             x = {
#                 'stop_name': data.platform.stop.stop_name,
#                 'time': data.time_span,
#                 'request_stop': False
#             }
#             stops.append(x)
#
#     lines_data.append(name)
#     name['stops'] = stops
#
#     return jsonify(lines_data)


# @app.route('/stops/stop/<int:stop_id>', methods=['GET'])
# def stop(stop_id):
#     datas = db.session.query(LinePlatform)
#     stop_data = []
#     info = {}
#     for data in datas:
#         if data.platform.id_stop == stop_id:
#             info['stop_name'] = data.platform.stop.stop_name
#     lines = []
#     for data in datas:
#         if data.platform.id_stop == stop_id and data.line_direction.id_stop != stop_id:
#             x = {
#                 'line_name': data.line_direction.line.line_name,
#                 'line_direction': data.line_direction.stop.stop_name
#             }
#             lines.append(x)
#     stop_data.append(info)
#     info['lines'] = lines
#     return jsonify(info)


@app.route('/timetable', methods=['GET'])
def timetable():
    times = db.session.query(Timetable).filter(Timetable.platform.has(id_stop=6), Timetable.line.has(line_name='1'), Timetable.line_direction.has(id_stop=3))
    momo = {}
    koko = []
    for time in times:
        x = {
            'hour': time.departure_hour,
            'minute': time.departure_minute
        }
        koko.append(x)
    momo['stuff'] = koko
    return jsonify(momo)


@app.route('/stops/stop/<int:id_stop>', methods=['GET'])
def get_stop(id_stop):
    # stops = db.session.query(LinePlatform).join(LinePlatform.platform) \
    #     .filter(LinePlatform.platform.property.mapper.class_.id_stop == 6)
    stops = db.session.query(LinePlatform).filter(LinePlatform.platform.has(id_stop=id_stop))
    stop_info = {}
    for stop in stops:
            stop_info['selected_stop'] = stop.platform.stop.stop_name
            break
    stop_lines = []
    for stop in stops:
        x = {
            'line_name': stop.line_direction.line.line_name,
            'line_direction': stop.line_direction.stop.stop_name,
        }
        stop_lines.append(x)
    stop_info['lines'] = stop_lines
    return jsonify(stop_info)

# @app.route('/adduser', methods=['POST'])
# def add():
#     new_user = Users(id = )









