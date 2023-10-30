from app import app, db
from app.endpoints.tasks import task_bp
from app.endpoints.users import user_bp
from app.controllers.users import first_user

app.register_blueprint(task_bp)
app.register_blueprint(user_bp)

with app.app_context():
    db.create_all()
    first_user()


def run():
    app.run(debug=True, port=8000)


if __name__ == '__main__':
    run()
