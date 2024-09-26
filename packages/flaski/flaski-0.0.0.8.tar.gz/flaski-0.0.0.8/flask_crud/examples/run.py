from app.main import create_app 
from app.config.authconfig import login_manager

app = create_app()
# Aministrador de sesiones de usuario
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

if __name__=="__main__":
    app.run(debug=True)