from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import the model files in the right order. This fixes issues with class dependencies
# Ignore Pep 8 this time in order to have the db instance initialized
from . import roles
from . import blog_post
from . import token
from . import user
