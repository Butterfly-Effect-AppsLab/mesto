from flask import request, render_template, make_response, Response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Users, Stop, Line, Platform, LineDirection, LinePlatform, Timetable, TimetableType
from flask import jsonify
from datetime import datetime
from sqlalchemy import and_, desc, text, distinct
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
    # return jsonify({'stops': output}), 200
    response = make_response(jsonify({'stops': output}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/lines', methods=['GET'])
def lines():
    linky = db.session.query(Line)
    data = []
    for linka in linky:
        smer = []
        x = {
            'id': linka.id,
            'name': linka.line_name
        }
        for d in linka.directions:
                smer.append(d.stop.stop_name)
        x['directions'] = smer
        data.append(x)
    response = make_response(jsonify(data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# @app.route('/asdf', methods=['GET'])
# def asdf():
#     linky = db.session.query(Line)
#     data = []
#     for linka in linky:
#         smer = []
#         current_line = linka.id
#         x = {
#             'id': linka.id,
#             'name': linka.line_name
#         }
#         # data.append(x)
#         for l in linka.directions:
#             if l.id_line == current_line:
#                 y = l.stop.stop_name
#                 smer.append(y)
#         x['smer'] = smer
#         data.append(x)
#     return jsonify(data)




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

    # return jsonify(line_data)
    response = make_response(jsonify(line_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


####funguje len na dva smery
@app.route('/lines/line/<int:id_line>', methods=['GET'])
def momo(id_line):
    line = db.session.query(LineDirection).filter(LineDirection.id_line == id_line).first()
    line_stops = []
    line_info = {
        'line_id': line.id_line,
        'line_name': line.line.line_name
    }
    line_stops.append(line_info)
    direction_tam = {}
    direction_tam['direction'] = line.stop.stop_name
    direction_tam['id_direction'] = line.id_stop
    stops = []
    for stop in line.platforms:
        stop = {
            'stop_name': stop.platform.stop.stop_name,
            'request_stop': stop.request_stop,
            'time': stop.time_span
        }
        stops.append(stop)
    direction_tam['stops_list'] = stops
    line_stops.append(direction_tam)

    line = db.session.query(LineDirection).filter(LineDirection.id_line == id_line).order_by(LineDirection.id.desc()).first()
    direction_spat = {}
    direction_spat['direction'] = line.stop.stop_name
    direction_spat['direction_id'] = line.id_stop
    stops2 = []
    for stop in line.platforms:
        stop = {
            'stop_name': stop.platform.stop.stop_name,
            'request_stop': stop.request_stop,
            'time': stop.time_span
        }
        stops2.append(stop)
    direction_spat['stops_list'] = stops
    line_stops.append(direction_spat)

    # return jsonify(line_stops)
    response = make_response(jsonify(line_stops))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route("/")
def home():
    routes_info = {
        '/lines': 'lines with their directions',
        '/stops': 'all stops',
        '/lines/line/{lineid}': 'one line in both directions',
        '/lines/line/{lineid}/{idstop}': 'one line in one direction',
        '/stops/stop/{idstop}': 'one stop and its lines',
        '/departures/{idstop}': 'nearest departures from one stop'
    }
    resp = make_response(jsonify(routes_info))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/timetable', methods=['GET'])
def timetable():

    ###############################################
    #### daytype determination is missing #########
    ###############################################

    times = db.session.query(Timetable).filter(Timetable.id_line == '1',
                                               Timetable.line_direction.has(id_stop=16),
                                               Timetable.platform.has(id_stop=3),
                                               Timetable.type == 1)
    time_info = {}
    timetable = {}
    for time in times:
        str_hour = str(time.departure_hour).zfill(2)
        str_minute = str(time.departure_minute).zfill(2)
        if (str_hour) not in timetable:
            timetable[str_hour] = []
        timetable[str_hour].append(str_minute)
    timetable = [{'hour': hour, 'minutes': minutes} for hour, minutes in timetable.items()]
    time_info['weekday'] = timetable
    # line_now = db.session.query(Line).filter_by(id=1).one()
    # stop_now = db.session.query(Stop).filter_by(id=3).one()
    # line_direction = db.session.query(LineDirection).filter_by(id_stop=16).one()
    # time_info['line_direction'] = line_direction.stop.stop_name
    # time_info['selected_line'] = line_now.line_name
    # time_info['selected_stop'] = stop_now.stop_name
    # return jsonify(time_info)
    response = make_response(jsonify(time_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/stops/stop/<int:id_stop>', methods=['GET'])
def get_stop(id_stop):
    line_platforms = db.session.query(LinePlatform).filter(LinePlatform.platform.has(id_stop=id_stop))
    stop_info = {}
    for stop in line_platforms:
            stop_info['selected_stop'] = stop.platform.stop.stop_name
            break
    stop_lines = []
    for stop in line_platforms:
        x = {
            'line_name': stop.line_direction.line.line_name,
            'line_direction': stop.line_direction.stop.stop_name,
        }
        stop_lines.append(x)
    stop_info['lines'] = stop_lines
    # return jsonify(stop_info)
    response = make_response(jsonify(stop_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/stops/stop/<int:stop_id>/lines')
def stop_lines(stop_id):
    stop = db.session.query(Stop).filter_by(id=stop_id).one()
    stop_info = {
        'selected_stop': stop.stop_name
    }
    stop_lines = []
    directions = (db.session.query(LineDirection)
                  .join(LineDirection.platforms)
                  .join(LinePlatform.platform)
                  .filter(Platform.id_stop == stop_id))
    for d in directions:
        line = {
            'line_name': d.line.line_name
        }
        stop_lines.append(line)
    stop_info['lines'] = stop_lines
    return jsonify(stop_info)



@app.route('/departures/<int:stop_id>', methods=['GET'])
def departures(stop_id):
    stop = db.session.query(Stop).filter_by(id=stop_id).one()
    stop_info = {
        'selected_stop': stop.stop_name
    }
    stop_lines = []
    directions = (db.session.query(LineDirection)
                  .join(LineDirection.platforms)
                  .join(LinePlatform.platform)
                  .filter(Platform.id_stop == stop_id))
    for d in directions:
        line = {
            'line_name': d.line.line_name
        }
        stop_lines.append(line)
    stop_info['lines'] = stop_lines

    hour = datetime.now().hour
    min = datetime.now().minute

    def get_schedule(hour, min):
        times = db.session.query(Timetable).filter(
                                            Timetable.platform.has(id_stop=stop_id),
                                            Timetable.type == 1).order_by(text(
                '(departure_hour =:hour and departure_minute >=:min) desc, departure_hour >:hour desc, departure_hour, departure_minute'))\
                                            .params(hour=hour,min=min).limit(5)
        return times
    times = get_schedule(hour, min)
    nearest = []
    for time in times:
        y = {
            'hour': str(time.departure_hour).zfill(2),
            'minute': str(time.departure_minute).zfill(2),
            'low_rise': time.low_rise,
            'line': time.line.line_name,
            'line_direction': time.line_direction.stop.stop_name
        }
        nearest.append(y)
    #get nearest departures from stop
    stop_info['departures'] = nearest
    # return jsonify(stop_info)
    response = make_response(jsonify(stop_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response










