from flask_app import app
from flask import redirect,request,render_template,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.admin import Admin


@app.route('/loginPage/admin')
def loginPageAdmin():
    if 'user_id' in session:
        return redirect('/')
    return render_template('loginAdmin.html')

@app.route('/login/admin', methods = ['POST'])
def loginAdmin():
    if 'user_id' in session:
        return redirect('/')
    if not Admin.validate_user(request.form):
        return redirect(request.referrer)
    user = Admin.get_admin_by_email(request.form)
    if not user:
        flash('This email doesnt exist', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Incorrect password', 'passwordLogin')
        return redirect(request.referrer)
    
    session['user_id']= user['id']
    return redirect('/admin')


@app.route('/admin')
def adminPage():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = Admin.get_admin_by_id(data)
    if user and user['role'] == 'admin':
        return render_template('welcomeAdmin.html', loggedUser = user)
    return redirect('/logout')
