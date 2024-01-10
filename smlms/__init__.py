from flask import Flask
from flask_mysqldb import MySQL
from smlms.config import Config
  
app = Flask(__name__)
app.secret_key = '78fe2c0421ba6c56cc3bb575b7046451'

app.config.from_object(Config)  # Load configurations

mysql = MySQL(app)

from smlms import routes