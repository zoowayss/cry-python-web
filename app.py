from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Student, Department, Class, Hobby, StudentHobby, Grade
from config import Config
from datetime import datetime, date
from sqlalchemy import text
import pymysql

app = Flask(__name__)
app.config.from_object(Config)

# 初始化扩展
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 首页
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误')

    return render_template('login.html')

# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册')
            return render_template('register.html')

        # 创建新用户
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('注册成功，请登录')
        return redirect(url_for('login'))

    return render_template('register.html')

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 主页面
@app.route('/dashboard')
@login_required
def dashboard():
    # 获取统计数据
    total_students = Student.query.count()
    total_departments = Department.query.count()
    total_classes = Class.query.count()

    return render_template('dashboard.html',
                         total_students=total_students,
                         total_departments=total_departments,
                         total_classes=total_classes)

# 学生列表
@app.route('/students')
@login_required
def students_list():
    page = request.args.get('page', 1, type=int)
    students = Student.query.paginate(
        page=page, per_page=10, error_out=False)

    # 获取部门和班级信息用于显示
    departments = {d.id: d.name for d in Department.query.all()}
    classes = {c.id: c.name for c in Class.query.all()}

    return render_template('students/list.html',
                         students=students,
                         departments=departments,
                         classes=classes)

# 添加学生
@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        student = Student(
            student_id=request.form['student_id'],
            name=request.form['name'],
            gender=request.form['gender'],
            age=int(request.form['age']),
            phone=request.form['phone'],
            email=request.form['email'],
            address=request.form['address'],
            department_id=int(request.form['department_id']),
            class_id=int(request.form['class_id']),
            enrollment_date=datetime.strptime(request.form['enrollment_date'], '%Y-%m-%d').date()
        )

        db.session.add(student)
        db.session.commit()
        flash('学生添加成功')
        return redirect(url_for('students_list'))

    departments = Department.query.all()
    classes = Class.query.all()
    return render_template('students/add.html', departments=departments, classes=classes)

# 编辑学生
@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.student_id = request.form['student_id']
        student.name = request.form['name']
        student.gender = request.form['gender']
        student.age = int(request.form['age'])
        student.phone = request.form['phone']
        student.email = request.form['email']
        student.address = request.form['address']
        student.department_id = int(request.form['department_id'])
        student.class_id = int(request.form['class_id'])
        student.enrollment_date = datetime.strptime(request.form['enrollment_date'], '%Y-%m-%d').date()
        student.updated_at = datetime.utcnow()

        db.session.commit()
        flash('学生信息更新成功')
        return redirect(url_for('students_list'))

    departments = Department.query.all()
    classes = Class.query.all()
    return render_template('students/edit.html', student=student, departments=departments, classes=classes)

# 删除学生
@app.route('/students/delete/<int:id>')
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('学生删除成功')
    return redirect(url_for('students_list'))

# 数据统计页面
@app.route('/statistics')
@login_required
def statistics():
    return render_template('statistics.html')

# API: 获取统计数据
@app.route('/api/statistics')
@login_required
def api_statistics():
    # 按部门统计学生数量
    dept_stats = db.session.execute(text("""
        SELECT d.name, COUNT(s.id) as count
        FROM departments d
        LEFT JOIN students s ON d.id = s.department_id
        GROUP BY d.id, d.name
    """)).fetchall()

    # 按班级统计学生数量
    class_stats = db.session.execute(text("""
        SELECT c.name, COUNT(s.id) as count
        FROM classes c
        LEFT JOIN students s ON c.id = s.class_id
        GROUP BY c.id, c.name
    """)).fetchall()

    # 按性别统计
    gender_stats = db.session.execute(text("""
        SELECT gender, COUNT(*) as count
        FROM students
        GROUP BY gender
    """)).fetchall()

    return jsonify({
        'departments': [{'name': row[0], 'count': row[1]} for row in dept_stats],
        'classes': [{'name': row[0], 'count': row[1]} for row in class_stats],
        'genders': [{'name': row[0], 'count': row[1]} for row in gender_stats]
    })

def init_database():
    """初始化数据库和测试数据"""
    with app.app_context():
        db.create_all()

        # 检查是否已有数据
        if Department.query.count() == 0:
            # 创建院系
            departments = [
                Department(name='计算机科学与技术学院', description='计算机相关专业'),
                Department(name='电子信息工程学院', description='电子信息相关专业'),
                Department(name='机械工程学院', description='机械工程相关专业')
            ]
            for dept in departments:
                db.session.add(dept)
            db.session.commit()

            # 创建班级
            classes = [
                Class(name='计科2021-1班', department_id=1, grade_year=2021),
                Class(name='计科2021-2班', department_id=1, grade_year=2021),
                Class(name='电信2021-1班', department_id=2, grade_year=2021),
                Class(name='机械2021-1班', department_id=3, grade_year=2021)
            ]
            for cls in classes:
                db.session.add(cls)
            db.session.commit()

            # 创建兴趣爱好
            hobbies = [
                Hobby(name='编程', description='喜欢编程开发'),
                Hobby(name='篮球', description='喜欢打篮球'),
                Hobby(name='音乐', description='喜欢听音乐'),
                Hobby(name='阅读', description='喜欢读书')
            ]
            for hobby in hobbies:
                db.session.add(hobby)
            db.session.commit()

            # 创建测试学生数据
            students = [
                Student(
                    student_id='2021001',
                    name='迟茹月',
                    gender='女',
                    age=20,
                    phone='13800138001',
                    email='chiruyue@example.com',
                    address='北京市朝阳区',
                    department_id=1,
                    class_id=1,
                    enrollment_date=date(2021, 9, 1)
                ),
                Student(
                    student_id='2021002',
                    name='钢铁侠',
                    gender='男',
                    age=21,
                    phone='13800138002',
                    email='ironman@example.com',
                    address='纽约市曼哈顿',
                    department_id=1,
                    class_id=1,
                    enrollment_date=date(2021, 9, 1)
                ),
                Student(
                    student_id='2021003',
                    name='卡皮巴拉',
                    gender='男',
                    age=19,
                    phone='13800138003',
                    email='capybara@example.com',
                    address='南美洲',
                    department_id=2,
                    class_id=3,
                    enrollment_date=date(2021, 9, 1)
                )
            ]
            for student in students:
                db.session.add(student)
            db.session.commit()

            # 创建默认管理员用户
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('123123')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=8000)
