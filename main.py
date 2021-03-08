import datetime
from flask import Flask, url_for, request, render_template, redirect
from forms.register import RegisterForm
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8000, host='127.0.0.1')


@app.route("/")
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        if form.password.data != form.password_again.data:
            return render_template(
                'register.html', title='Регистрация', form=form,
                message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'register.html', title='Регистрация', form=form,
                message="Такой пользователь уже есть")

        user = User()
        user.email = form.email.data
        user.set_password(form.password.data)
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        db_sess.add(user)
        db_sess.commit()

        return "Форма отправлена"

    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
