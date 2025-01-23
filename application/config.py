class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    SECRET_KEY = "I_I_T_M_B_S"                      # For signed session cookies
    SECURITY_LOGIN_URL = "/#/"                      # Redirecting Flask-Security login to application login
    WTF_CSRF_ENABLED = False                                
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_JOIN_USER_ROLES = 'RolesUsers'