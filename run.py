from app import app, db
from app.endpoints.rest import task_bp

app.register_blueprint(task_bp)

with app.app_context():
    db.create_all()

def run():
    app.run(debug=True, port=8000)

if __name__ == '__main__':
    run()
