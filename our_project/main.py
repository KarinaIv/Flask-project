from flask import Flask, request, make_response, session, render_template, redirect, abort
from data import db_session
from forms.login import LoginForm
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from forms.user import RegisterForm
from forms.products import ProductsForm

from data.users import User
from data.products import Products
import datetime

from flask_login import LoginManager


app = Flask(__name__)


app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    products = db_sess.query(Products)
    return render_template("index.html", products=products)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/products',  methods=['GET', 'POST'])
@login_required
def add_products():
    form = ProductsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        products = Products()
        products.title = form.title.data
        products.content = form.content.data
        products.price = form.price.data
        current_user.products.append(products)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('products.html', title='Добавление товара',
                           form=form)


@app.route('/products/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_products(id):
    form = ProductsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        products = db_sess.query(Products).filter(Products.id == id,
                                          Products.user == current_user
                                          ).first()
        if products:
            form.title.data = products.title
            form.content.data = products.content
            form.price.data = products.price
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        products = db_sess.query(Products).filter(Products.id == id,
                                          Products.user == current_user
                                          ).first()
        if products:
            products.title = form.title.data
            products.content = form.content.data
            products.price = form.price.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('products.html',
                           title='Редактирование товара',
                           form=form
                           )

@app.route('/products_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def products_delete(id):
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.id == id,
                                      Products.user == current_user
                                      ).first()
    if products:
        db_sess.delete(products)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/likes', methods=['GET', 'POST'])
def likes():
    pass

@app.route('/shop_cart', methods=['GET', 'POST'])
def shop_cart():
    pass


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()