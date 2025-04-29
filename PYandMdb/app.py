from flask import Flask

from controllers.create_student_controller import create_bp
from controllers.read_student_controller import read_bp
from controllers.delete_student_controller import delete_bp
from controllers.update_student_controller import update_bp

app = Flask(__name__)

app.register_blueprint(create_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(read_bp)
app.register_blueprint(update_bp)

app.secret_key = "your-secret-key"


if __name__ == "__main__":
    app.run(debug=True)