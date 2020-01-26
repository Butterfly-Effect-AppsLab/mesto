from flask import request, render_template, make_response, Response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Users, Stop, Line, Platform, LineDirection, LinePlatform, Timetable, TimetableType, LineType, Calendar
from flask import jsonify
from datetime import datetime
from sqlalchemy import and_, desc, text, distinct
import json


@app.route("/")
def home():
    routes_info = {
        '/lines': 'lines with their directions',
        '/stops': 'all stops (general)',
        '/lines/line/{lineid}': 'one line in both directions',
        '/lines/line/{lineid}/{idstop}': 'one line in one direction',
        '/stops/stop/{idstop}': 'one stop and its lines',
        '/departures/{idstop}': '3 nearest departures from one stop',
        '/stops/stop/{idstop}/lines': 'all lines on one stop',
        '/timetable/{idline}/{iddirection}/{idstop}/{daytype}': 'all departure times for one line',
        '/line_departures/{id_line}/{id_direction}/{id_stop}': '3 nearest departures for one line',
        '/platform/directions': 'all individual stops with GPS coordinates',
        '/platform/directions/{id_platform}': '3 nearest line departures in one direction'
    }
    response = make_response(jsonify(routes_info))
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

    response = make_response(jsonify({'stops': output}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# @app.route('/user/add', methods=['POST'])
# def add_user():
#     id = request.json['id1']
#     id2 = request.json['id2']
#     onboard = request.json['on_type']
#     os_type = request.json['os_type']
#
#     new_user = Users(id, id2, onboard, os_type, datetime.now())
#     db.session.add(new_user)
#     db.session.commit()
#
#     return 'User added to DB', 201


# @app.route('/favourites/line', methods=['POST'])
# def favourite_lines():
#     id_user = request.json['id_user']
#     id_platform = request.json['id_platform']
#     id_line = request.json['id_line']
#     id_direction = request.json['id_direction']
#
#     new_f_line = Favourite_line(id_user, id_platform, id_line, id_direction)
#     db.session.add(new_f_line)
#     db.session.commit()
#     return "Line has been added to favourites", 201


# @app.route('/favourites/stop', methods=['POST'])
# def favourite_stops():
#     id_user = request.json['id_user']
#     id_platform = request.json['id_platform']
#     id_line = request.json['id_line']
#     id_direction = request.json['id_direction']
#
#     new_f_line = Favourite_line(id_user, id_platform, id_line, id_direction)
#     db.session.add(new_f_line)
#     db.session.commit()
#     return "Stop has been added to favourites", 201


@app.route('/lines/line/<line_name>/<int:line_direction>', methods=['GET'])
def test(line_name, line_direction):
    line_info = []
    line, direction = (db.session.query(Line, LineDirection)
                       .join(Line.directions)
                       .filter(
        Line.line_name == line_name,
        LineDirection.id_stop == line_direction)
                       .one())
    line_data = {
        'name': line.line_name,
        'direction': direction.stop.stop_name,
        'line_type': line.id_line_type
    }

    stops = []
    for platform in direction.platforms:
        stop = {
            'stop_name': platform.platform.stop.stop_name,
            'request_stop': platform.request_stop,
            #'time': platform.time_span,
            'id_stop': platform.platform.id_stop
        }
        stops.append(stop)

    line_data['stops'] = stops
    line_info.append(line_data)
    # return jsonify(line_data)
    response = make_response(jsonify(line_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


####funguje len na dva smery
@app.route('/lines/line/<int:id_line>', methods=['GET'])
def line_detail(id_line):
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
            #'time': stop.time_span
        }
        stops.append(stop)
    direction_tam['stops_list'] = stops
    line_stops.append(direction_tam)

    line = db.session.query(LineDirection).filter(LineDirection.id_line == id_line).order_by(LineDirection.id.desc()).first()
    direction_spat = {}
    direction_spat['direction'] = line.stop.stop_name
    direction_spat['id_direction'] = line.id_stop
    stops2 = []
    for stop in line.platforms:
        stop = {
            'stop_name': stop.platform.stop.stop_name,
            'request_stop': stop.request_stop,
            #'time': stop.time_span
        }
        stops2.append(stop)
    direction_spat['stops_list'] = stops
    line_stops.append(direction_spat)

    # return jsonify(line_stops)
    response = make_response(jsonify(line_stops))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/timetable/<int:id_line>/<int:id_direction>/<int:id_stop>/<weekday>', methods=['GET'])
def timetable(id_line, id_direction, id_stop, weekday):
    if weekday == 'work':
        day_type = 1
    if weekday == 'holiday':
        day_type = 2
    if weekday == 'offDays':
        day_type = 3

    times = db.session.query(Timetable).filter(Timetable.id_line == id_line,
                                               Timetable.line_direction.has(id_stop=id_direction),
                                               Timetable.platform.has(id_stop=id_stop),
                                               Timetable.type == day_type)
    time_info = {}
    timetable = {}

    for time in times:
        str_hour = str(time.departure_hour).zfill(2)
        str_minute = str(time.departure_minute).zfill(2)
        if (str_hour) not in timetable:
            timetable[str_hour] = []
        timetable[str_hour].append(str_minute)
    timetable = [{'hour': hour, 'minutes': minutes} for hour, minutes in timetable.items()]

    time_info[weekday] = timetable

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
            'line_name': d.line.line_name,
            'line_id': d.line.id
        }
        if not any(dict['line_name'] == d.line.line_name for dict in stop_lines):
            stop_lines.append(line)
    stop_info['lines'] = stop_lines

    response = make_response(jsonify(stop_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/departures/<int:stop_id>', methods=['GET'])
def departures(stop_id):

    stop = db.session.query(Stop).filter_by(id=stop_id).one()

    stop_info = {
        'stop_name': stop.stop_name,
        'stop_id': stop.id
    }

    hour = datetime.now().hour
    min = datetime.now().minute
    daytype = get_daytype()

    def get_schedule(hour, min):
        times = db.session.query(Timetable).filter(
                                            Timetable.platform.has(id_stop=stop_id),
                                            Timetable.type == daytype).order_by(text(
                '(departure_hour =:hour and departure_minute >=:min) desc, departure_hour >:hour desc, departure_hour, departure_minute'))\
                                            .params(hour=hour,min=min).limit(5)
        return times
    times = get_schedule(hour, min)
    nearest = []

    for time in times:
        y = {
            # 'hour': str(time.departure_hour).zfill(2),
            # 'minute': str(time.departure_minute).zfill(2),
            'low_rise': time.low_rise,
            'line_name': time.line.line_name,
            'line_direction': time.line_direction.stop.stop_name,
            'arrival_time': time_until(time.departure_hour, time.departure_minute)
        }
        nearest.append(y)
    stop_info['lines'] = nearest

    response = make_response(jsonify(stop_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/departures/<int:stop_id>/<int:line_limit>', methods=['GET'])
def departures_limit(stop_id, line_limit):

    stop = db.session.query(Stop).filter_by(id=stop_id).one()

    stop_info = {
        'stop_name': stop.stop_name,
        'stop_id': stop.id
    }

    hour = datetime.now().hour
    min = datetime.now().minute
    daytype = get_daytype()

    def get_schedule(hour, min):
        times = db.session.query(Timetable).filter(
                                            Timetable.platform.has(id_stop=stop_id),
                                            Timetable.type == daytype).order_by(text(
                '(departure_hour =:hour and departure_minute >=:min) desc, departure_hour >:hour desc, departure_hour, departure_minute'))\
                                            .params(hour=hour,min=min).limit(line_limit)
        return times
    times = get_schedule(hour, min)
    nearest = []

    for time in times:
        y = {
            # 'hour': str(time.departure_hour).zfill(2),
            # 'minute': str(time.departure_minute).zfill(2),
            'low_rise': time.low_rise,
            'line_name': time.line.line_name,
            'line_direction': time.line_direction.stop.stop_name,
            'arrival_time': time_until(time.departure_hour, time.departure_minute)
        }
        nearest.append(y)
    stop_info['lines'] = nearest

    response = make_response(jsonify(stop_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/line_departures/<id_line>/<id_direction>/<id_stop>', methods=['GET'])
def closest(id_line, id_direction, id_stop):

    selected_stop = db.session.query(Stop).filter(Stop.id==id_stop).one()
    line = db.session.query(LineDirection).filter_by(id_line= id_line, id_stop = id_direction).one()

    day_type = get_daytype()

    line_nearest = {}
    line_nearest['selected_stop'] = selected_stop.stop_name
    line_nearest['line_id'] = line.id_line
    line_nearest['line_direction'] = line.stop.stop_name
    hour = datetime.now().hour
    min = datetime.now().minute

    times = db.session.query(Timetable).filter(Timetable.id_line == id_line,
                                               Timetable.line_direction.has(id_stop=id_direction),
                                               Timetable.platform.has(id_stop=id_stop),
                                               Timetable.type == day_type).order_by(text(
                '(departure_hour =:hour and departure_minute >=:min) desc, departure_hour >:hour desc, departure_hour, departure_minute'))\
                                            .params(hour=hour,min=min).limit(3)
    departures = []

    for time in times:
           departures.append(str(time.departure_hour).zfill(2) + ':' + str(time.departure_minute).zfill(2))
    line_nearest['closest_departures'] = departures
    line_nearest['delays'] = []

    response = make_response(jsonify(line_nearest))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/platform/directions', methods=['GET'])
def directions():
    platforms = db.session.query(Platform)
    platform_info = {}
    platform_list = []
    for platform in platforms:
        plat = {
            'platform_id': platform.id,
            'platform_lat': str(platform.lat),
            'platform_long': str(platform.long),
            'platform_name': platform.platform_name
        }
        if platform.lat is not None and platform.long is not None:
            platform_list.append(plat)
    platform_info['platforms'] = platform_list
    response = make_response(jsonify(platform_info))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/platform/directions/<int:platform_id>')
def directions_arrivals(platform_id):

    platform = db.session.query(Platform).filter(Platform.id==platform_id).one()

    platform_detail = {}
    platform_detail['platform_id'] = platform.id
    platform_detail['platform_name'] = platform.platform_name

    hour = datetime.now().hour
    min = datetime.now().minute
    daytype = get_daytype()

    times = db.session.query(Timetable).filter(
        Timetable.id_platform==platform_id,
        Timetable.type == daytype).order_by(text(
        '(departure_hour =:hour and departure_minute >=:min) desc, departure_hour >:hour desc, departure_hour, departure_minute')) \
        .params(hour=hour, min=min).limit(5)

    nearest = []

    for time in times:
        y = {
            'low_rise': time.low_rise,
            'line_name': time.line.line_name,
            'line_direction': time.line_direction.stop.stop_name,
            #'arrival_time': str(time.departure_hour).zfill(2) + ':' + str(time.departure_minute).zfill(2),
            'arrival_time': time_until(time.departure_hour, time.departure_minute)
        }
        nearest.append(y)
    platform_detail['departures'] = nearest

    response = make_response(jsonify(platform_detail))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/platform/directions/<int:platform_id>/<int:line_limit>')
def directions_arrivals_limit(platform_id, line_limit):

    platform = db.session.query(Platform).filter(Platform.id==platform_id).one()

    platform_detail = {}
    platform_detail['platform_id'] = platform.id
    platform_detail['platform_name'] = platform.platform_name

    hour = datetime.now().hour
    min = datetime.now().minute
    daytype = get_daytype()

    times = db.session.query(Timetable).filter(
        Timetable.id_platform==platform_id,
        Timetable.type == daytype).order_by(text(
        '(departure_hour =:hour and departure_minute >=:min) desc, departure_hour >:hour desc, departure_hour, departure_minute')) \
        .params(hour=hour, min=min).limit(line_limit)

    nearest = []

    for time in times:
        y = {
            'low_rise': time.low_rise,
            'line_name': time.line.line_name,
            'line_direction': time.line_direction.stop.stop_name,
            #'arrival_time': str(time.departure_hour).zfill(2) + ':' + str(time.departure_minute).zfill(2),
            'arrival_time': time_until(time.departure_hour, time.departure_minute)
        }
        nearest.append(y)
    platform_detail['departures'] = nearest

    response = make_response(jsonify(platform_detail))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def time_until(dep_hour, dep_min):
    dep_time = datetime.now().replace(hour=dep_hour, minute=dep_min)
    time_diff = datetime.now() - dep_time
    return abs(int(time_diff.total_seconds() / 60))

def get_daytype():
    date = datetime.now()
    date_type = 1
    dates = db.session.query(Calendar)
    for d in dates:
        date_from = datetime.utcfromtimestamp(d.time_from)
        date_to = datetime.utcfromtimestamp(d.time_to)
        if date_from <= date <= date_to:
            date_type = d.type
    return date_type


























