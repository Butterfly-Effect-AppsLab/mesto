from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User, Stop

# class HelloWorld(Resource):
#     def get(self):
#         return {'hello' : 'world'}
#
# api.add_resource(HelloWorld, '/')
#
# @app.route('/', methods=['GET'])
# def create_user():
#     """Create a user."""
#     username = request.args.get('user')
#     email = request.args.get('email')
#     if username and email:
#         existing_user = User.query.filter(User.username == username or User.email == email).first()
#         if existing_user:
#             return make_response(f'{username} ({email}) already created!')
#         new_user = User(username=username,
#                         email=email,
#                         created=dt.now(),
#                         bio="In West Philadelphia born and raised, on the playground is where I spent most of my days",
#                         admin=False)  # Create an instance of the User class
#         db.session.add(new_user)  # Adds new User record to database
#         db.session.commit()  # Commits all changes
#     return render_template('users.html',
#                            users=User.query.all(),
#                            title="Show Users")


@app.route('/stop', methods=['GET'])
def stop():
    wer = Stop.query.first()
    return wer.stop_name
