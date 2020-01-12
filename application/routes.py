from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Users, Stop, Line, Platform, LineDirection, LinePlatform, Timetable, TimetableType
from flask import jsonify
from datetime import datetime
import json


@app.route('/stops', methods=['GET'])
def stops():
    stops = Stop.query.all()

    output = []

    for stop in stops:
        x = {
            'stop_name': stop.stop_name,
            'stop_id': stop.id
        }
        output.append(x)
    return jsonify({'stops': output}), 200


@app.route('/lines', methods=['GET'])
def lines():
    lines = Line.query.all()

    output = []

    for line in lines:
        x = {
            'name': line.line_name,
            'line_id': line.id
        }
        output.append(x)

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
    ########################
    # here date and time implementation,
    # determining if holidays or weekend
    #
    # for now, everything is workday -> Timetable.type == 1
    ########################
    # hour = datetime.datetime.now().hour
    # min = datetime.datetime.now().minute
    times = db.session.query(Timetable).filter(Timetable.id_line == '1',
                                        Timetable.line_direction.has(id_stop=16),
                                        Timetable.type == 1
                                        )
    time_info = {}
    timetable = []
    for time in times:
        y = {
            'hour': str(time.departure_hour).zfill(2),
            'minute': str(time.departure_minute).zfill(2),
            'low_rise': time.low_rise,
            'line': time.line.line_name
        }
        timetable.append(y)
    time_info['weekday'] = timetable
    line_now = db.session.query(Line).filter_by(id=1).one()
    stop_now = db.session.query(Stop).filter_by(id=3).one()
    line_direction = db.session.query(LineDirection).filter_by(id_stop=16).one()
    time_info['line_direction'] = line_direction.stop.stop_name
    time_info['selected_line'] = line_now.line_name
    time_info['selected_stop'] = stop_now.stop_name
    return jsonify(time_info)


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


fav_lines_dummy = {
    'id': 1,
    'id_user': 12,
    'id_platform': 99,
    'id_direction': 1
}









