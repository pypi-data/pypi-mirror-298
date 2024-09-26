from flask import flash, redirect, render_template, url_for, Blueprint, request
from flask_crud.dbutil import DBController
from flask_crud.routeutil import Route
from flask_login import UserMixin, login_required, login_user, logout_user, current_user
from app.config.authconfig import login_manager
from app.config.permission import roles


class User(UserMixin):
    def __init__(self, id=0,  username="unknow", role_name="", permissions=[]):
        self.id = id
        self.username = username
        self.role_name = role_name
        self.permissions = permissions
    
    def toStr(self):
        return str(vars(self))
    
    def __str__(self) -> str:
        return self.toStr()
    
    @staticmethod
    def fromDict(user_dict:dict):
        if user_dict and "id" in user_dict:            
            user = User()
            uservars = vars(user)  
            uservars.pop("permissions")      
            for field in uservars:
                setattr(user, field, user_dict.get(field))
            user.permissions = roles.get(user.role_name) if roles.get(user.role_name) else {}
            return user
        return None

@login_manager.user_loader
def load_user(user_id):
    user_dict = DBController.queryOne("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    return User.fromDict(user_dict)

class AuthRoute(Route):    
    blueprint = Blueprint("auth", __name__)
    
    @blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            #hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user_dict = DBController.queryOne("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password))
            if user_dict:
                login_user(User.fromDict(user_dict))                
                return redirect(url_for('index.dashboard'))
            else:
                flash('Invalid credentials', 'danger')
        return render_template('login.html')
    
    @blueprint.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('auth.login'))
