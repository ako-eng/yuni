from flask import Flask
from flask_cors import CORS
from app.api import auth, health, notice, course, grade, exam, award, search

def create_app():
    """应用工厂函数"""
    app = Flask(__name__)
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(auth.bp, url_prefix='/api')
    app.register_blueprint(health.bp, url_prefix='/api')
    app.register_blueprint(notice.bp, url_prefix='/api')
    app.register_blueprint(course.bp, url_prefix='/api')
    app.register_blueprint(grade.bp, url_prefix='/api')
    app.register_blueprint(exam.bp, url_prefix='/api')
    app.register_blueprint(award.bp, url_prefix='/api')
    app.register_blueprint(search.bp, url_prefix='/api')
    
    return app
