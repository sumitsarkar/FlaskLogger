import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'secret_key'



# Storage Server Configuration

# STORAGE_HOSTNAME = 'storage.local'
# STORAGE_USERNAME = 'root'
# STORAGE_PASSWORD = 'password'

# KVM Server Configuration

# KVM_HOSTNAME = 'storage.local'
# KVM_USERNAME = 'root'
# KVM_PASSWORD = 'password'