DEBUG = True
BCRYPT_LEVEL = 12 # Configuration for the Flask-Bcrypt extension
MAIL_FROM_EMAIL = "robert@example.com" # For use in application emails

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/kyan'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_TYPE = 'filesystem'
SECRET_KEY = 'super secret key'