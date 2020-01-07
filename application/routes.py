from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Users, Stop, Line, Platform, LineDirection, LinePlatform
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


@app.route('/lines/line/<line_name>', methods=['GET'])
def get_one_line(line_name):

    line = Line.query.filter_by(line_name=line_name).first()

    line_data = {}
    line_data['id'] = line.id
    line_data['line_name'] = line.line_name
    line_data['id_line_type'] = line.id_line_type

    return jsonify({'line': line_data})


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


@app.route('/test', methods=['GET'])
def test():
    ########################################################
    # SQL Query i wish to execute:
    # SELECT
    #     st.stop_name,
    #     lp.id_direction,
    #     ld.id,
    #     plat.platform_name,
    #     l.line_name
    # FROM Line_platforms lp
    # JOIN Line_directions ld ON lp.id_direction = ld.id
    # JOIN Platforms plat ON lp.id_platform = plat.id
    # JOIN Lines l ON l.id = ld.id_line
    # JOIN Stops st ON st.id = ld.id_stop
    # WHERE l.line_name = '1'
    # ;

    ###############################
    # this is what i have so far:
    test_query = db.session.query(Line, LineDirection, Stop, Platform, LinePlatform)\
        .filter(LineDirection.id == LinePlatform.id_direction)\
        .filter(LinePlatform.id_platform == Platform.id)\
        .filter(Line.id == LineDirection.id_line)\
        .filter(Stop.id == LineDirection.id_stop).all()

    ###############################
    # here i want a JSON output like
    #
    # {
    #     "line": {
    #         "line_name": "39",
    #         "direction" : "xyz",
    #         "stops" : [
    #             {
    #                 "stop_name" : "zahradnicka",
    #                 "stop_order" : 1
    #             },
    #             {
    #                 "stop_name" : "asdf",
    #                 "stop_order" : 2
    #             }
    #         ]
    #     }
    # }
    print(test_query)

