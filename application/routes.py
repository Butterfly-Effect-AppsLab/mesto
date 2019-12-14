from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User, Stop, Line
from flask import jsonify


@app.route('/stops', methods=['GET'])
def stops():

    stopss = Stop.query.all()

    output = []

    for sstop in stopss:
        stop_data = {}
        stop_data['name'] = sstop.stop_name
        output.append(stop_data)

    return jsonify({'stops': output})


@app.route('/lines', methods=['GET'])
def lines():
    lines = Line.query.all()

    output = []

    for line in lines:
        line_data = {}
        line_data['name'] = line.line_name
        output.append(line_data)

    return jsonify({'lines': output})
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
