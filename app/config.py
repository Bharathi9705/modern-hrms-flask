import os

class EnterpriseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', '0c326d96ff6d2ab20a8e3f43b67e8c12fae2e5033c41efbd')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '../hrms.db')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///../hrms.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '9f7d2f9d8a1c4e6b3f5d7a8b9c2d1e0f')
    JWT_EXPIRY_HOURS = 8