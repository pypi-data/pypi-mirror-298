from flask import Blueprint, redirect, session, url_for, request
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from app.config.permission import VALUE_ALL_PERMISSIONS

login_manager = LoginManager()

exclude_blueprints=[
"auth"
]
exclude_endpoints=[
# "auth.login",
]

def preRegisterBlueprint(blueprint:Blueprint):    
    
    @blueprint.before_request
    def require_login():
        # Excluye el endpoint
        if request.endpoint in exclude_endpoints:
            session['last_endpoint'] = request.endpoint
            return  # Permitir acceso a estas rutas sin autenticación
        # Excluye el blueprint completo si está en exclude_blueprints
        if request.blueprint in exclude_blueprints:
            session['last_endpoint'] = request.endpoint
            return  # Permitir acceso sin autenticación a todo el blueprint
        if not current_user.is_authenticated:
            session['last_endpoint'] = request.endpoint
            return redirect(url_for('auth.login'))
        else:
            print("JJJJJJJJJJJJJJJJ CURRENT USER jjjjjjjjjjjjjj")
            print(current_user)
            endpoints = current_user.permissions.get("endpoints")
            endpoints = endpoints if endpoints else [] 
            if request.endpoint!= session.get('last_endpoint', '') and (request.endpoint in endpoints or endpoints==VALUE_ALL_PERMISSIONS):
                session['last_endpoint'] = request.endpoint
                return

