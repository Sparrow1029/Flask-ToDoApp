import os
from datetime import datetime, date

from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms_components import DateRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'cookie_crisp'
app.config['DEBUG'] = True

Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Task


class TaskForm(FlaskForm):
    task_body = TextAreaField('Enter to-do task', validators=[DataRequired()])
    dt = DateField('Due Date:',
                   format='%Y-%m-%d',
                   validators=[DataRequired(),
                   DateRange(min=date.today())]
                  )

    submit = SubmitField('Save')


# def flash_errors(form):
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(u"Error in the %s field - %s" % (
#                 getattr(form, field).label.text, error))


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    tasks = Task.query.filter_by(completed=0).all()
    form = TaskForm()
    if request.method == 'POST':

        if 'save' in request.form:
            if form.validate_on_submit():
                body = form.task_body.data
                due_date = form.dt.data

                new_task = Task(body=body, due_date=due_date)
                db.session.add(new_task)
                db.session.commit()
                flash("New task added!", category='success')
                return redirect(url_for('index'))

        elif 'complete' in request.form:
            task_id = request.form.get('complete')
            completed_task = Task.query.filter_by(id=task_id).first()
            # change boolean column for record in db
            completed_task.completed = True
            completed_task.completed_date = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('index'))

        elif 'delete' in request.form:
            task_id = request.form.get('delete')
            task_to_delete = Task.query.filter_by(id=task_id).first()
            db.session.delete(task_to_delete)
            db.session.commit()
            flash('Task deleted!', category='success')
            return redirect(url_for('index'))

    if not tasks:
        flash('Add some tasks!', category='warning')

    return render_template('tasks_grid.html', tasks=tasks, form=form)


@app.route('/completed', methods=['GET', 'POST'])
def completed_tasks():
    form = TaskForm()
    tasks = Task.query.filter_by(completed=1)\
            .order_by(Task.completed_date.desc()).all()
    if request.method == 'POST':

        if 'save' in request.form:
            if form.validate_on_submit():
                body = form.task_body.data
                due_date = form.dt.data

                new_task = Task(body=body, due_date=due_date)
                db.session.add(new_task)
                db.session.commit()
                flash("New task added!", category='success')
                return redirect(url_for('index'))

        elif 'clear' in request.form:
            return redirect(url_for('clear_tasks'))

        elif 'delete' in request.form:
            task_id = request.form.get('delete')
            task_to_delete = Task.query.filter_by(id=task_id).first()
            db.session.delete(task_to_delete)
            db.session.commit()
            flash('Task deleted!', category='success')
            return redirect(url_for('completed_tasks'))

    if tasks:
        return render_template('tasks_grid.html', tasks=tasks, form=form)
    else:
        flash('No completed tasks to show.', category='danger')

    return redirect(url_for('index'))

@app.route('/clear-completed-tasks', methods=['POST', 'GET'])
def clear_tasks():
    Task.clear_completed()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
