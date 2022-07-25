from app import app, db
from flask import render_template, flash, redirect,url_for
from app.forms import EntryForm,LoginForm,RegistrationForm
from flask_login import current_user, login_user,logout_user, login_required
from app.models import User, Entry


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/entryform')   
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        return redirect(url_for('entryform'))        
    return render_template('login.html', form=form)


@app.route('/entryform', methods=['GET', 'POST'])
@login_required
def entryform():
    form= EntryForm()
    if form.validate_on_submit():
        entry = Entry(quantity=form.quantity.data,date = form.date.data,user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()
        flash('Entry Updated')
        return redirect(url_for('entryform'))
    return render_template('entry.html', form=form)


@app.route('/history')
@login_required
def history():
    person = User.query.get(current_user.id)
    query=person.entrys.all()
    gt = 0
    for no in query:
        gt += no.quantity 
      
    return render_template('history.html',query=query,total=gt)

@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unique id and
    # redirects to history
    data = Entry.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash('Entry Deleted')
    return redirect(url_for('history'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('entryform'))
    form= RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registerred user!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form) 

@app.route('/logout')
def logout(): 
    logout_user()
    flash('Logged out')
    return redirect(url_for('login'))      



