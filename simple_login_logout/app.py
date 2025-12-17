from flask import flask,render_template,request,redirect,url_for
import mysql.connector
app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host ="localhost",
        