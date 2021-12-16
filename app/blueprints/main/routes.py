from flask import render_template, request, redirect, url_for, flash
import requests
from app.models import MyTask, User, Task
from flask_login import login_required, login_user, current_user, logout_user
from .import bp as main
from wtforms import RadioField


@main.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/mytasks', methods = ['GET'])
@login_required
def mytasks():
    t = Task.query.filter_by(user_id = current_user.id).all()
    print(t)
    return render_template('mytasks.html.j2', tasks=t)

@main.route('/deletetask/<int:id>', methods=['GET'])
@login_required
def deletetask(id):
    task_to_delete = Task.query.get(id)
    if current_user.id==current_user.id:
        task_to_delete.delete_task()
        flash('Your task has been deleted','info')
    else:
        flash('You do not have access to do that')
    return redirect(url_for('main.mytasks'))
    
@main.route('/newtask', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        type = request.form.get('type')
        url = f'http://www.boredapi.com/api/activity?type={type}'
        response = requests.get(url)
        if response.ok:
            if not response.json()["activity"]:
                 error_string="We had an error loading your data likely the year or round is not in the database"
                 return render_template('newtask.html.j2', error = error_string)
            data = response.json()
            new_activity=[]
            
            activity_dict={
                'activity':data['activity'],
                'accessibility':data['accessibility'],
                'type':type,
                'participants':data['participants'],
                'price':data['price'],
                'link':data['link'],
                'key':data['key'],
            }
            new_activity.append(activity_dict)
            new_task = Task(user_id = current_user.id, task_name=activity_dict['activity'], task_type = activity_dict['type'],task_key=activity_dict['key'])
            new_task.add_task()
            flash(f'You have added {activity_dict["activity"]}, congratulations', 'success')
        print(new_activity)
        return render_template('newtask.html.j2', activities=new_activity)
    else:
        error_string = "Houston We had a problem"
        return render_template('newtask.html.j2', error = error_string)

        

