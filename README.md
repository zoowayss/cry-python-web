# 学生管理系统 (Student Management System)

## 项目概述

这是一个基于 Flask 框架开发的学生管理系统，提供了完整的学生信息管理功能，包括学生信息的增删改查、数据统计分析和可视化展示。系统采用现代化的 Web 界面设计，支持响应式布局。

## 技术栈

### 后端技术
- **Python 3.11+**: 主要编程语言
- **Flask 2.3.3**: Web 应用框架
- **Flask-SQLAlchemy 3.0.5**: ORM 数据库操作
- **Flask-Login 0.6.3**: 用户认证和会话管理
- **Flask-WTF 1.1.1**: 表单处理和 CSRF 保护
- **PyMySQL 1.1.0**: MySQL 数据库连接器

### 前端技术
- **Bootstrap 5.1.3**: 响应式 UI 框架
- **Font Awesome 6.0.0**: 图标库
- **ECharts 5.4.0**: 数据可视化图表库
- **HTML5/CSS3/JavaScript**: 前端基础技术

### 数据库
- **MySQL**: 关系型数据库

## 项目结构

```
cry-python-web/
├── app.py                 # 主应用文件，包含所有路由和业务逻辑
├── config.py              # 配置文件，包含数据库连接等配置
├── models.py              # 数据模型定义
├── requirements.txt       # Python 依赖包列表
├── templates/             # HTML 模板文件夹
│   ├── base.html         # 基础模板
│   ├── layout.html       # 布局模板（包含侧边栏）
│   ├── login.html        # 登录页面
│   ├── register.html     # 注册页面
│   ├── dashboard.html    # 仪表板页面
│   ├── statistics.html   # 数据统计页面
│   └── students/         # 学生相关页面
│       ├── list.html     # 学生列表
│       ├── add.html      # 添加学生
│       └── edit.html     # 编辑学生
└── .venv/                # Python 虚拟环境
```

## 核心功能

### 1. 用户认证系统
- 用户登录/登出
- 用户注册
- 会话管理
- 密码加密存储

### 2. 学生信息管理
- **学生列表**: 分页显示所有学生信息
- **添加学生**: 录入新学生信息
- **编辑学生**: 修改现有学生信息
- **删除学生**: 删除学生记录
- **信息字段**: 学号、姓名、性别、年龄、联系方式、院系、班级、入学日期等

### 3. 组织架构管理
- **院系管理**: 管理学校院系信息
- **班级管理**: 管理班级信息，关联院系和年级
- **层级关系**: 院系 → 班级 → 学生

### 4. 数据统计与可视化
- **统计图表**: 
  - 各院系学生分布（饼图）
  - 性别分布（环形图）
  - 各班级学生数量（柱状图）
- **数据表格**: 详细统计数据展示
- **实时刷新**: 支持数据实时更新

### 5. 扩展功能
- **爱好管理**: 学生兴趣爱好记录
- **成绩管理**: 学生成绩信息管理
- **多对多关系**: 学生与爱好的关联

## 数据库设计

### 主要数据表

1. **users (用户表)**
   - id: 主键
   - username: 用户名（唯一）
   - email: 邮箱（唯一）
   - password_hash: 加密密码
   - created_at: 创建时间

2. **departments (院系表)**
   - id: 主键
   - name: 院系名称
   - description: 院系描述
   - created_at: 创建时间

3. **classes (班级表)**
   - id: 主键
   - name: 班级名称
   - department_id: 所属院系ID
   - grade_year: 年级
   - created_at: 创建时间

4. **students (学生表)**
   - id: 主键
   - student_id: 学号（唯一）
   - name: 姓名
   - gender: 性别
   - age: 年龄
   - phone: 联系电话
   - email: 邮箱
   - address: 地址
   - department_id: 所属院系ID
   - class_id: 所属班级ID
   - enrollment_date: 入学日期
   - created_at/updated_at: 创建/更新时间

5. **hobbies (爱好表)**
   - id: 主键
   - name: 爱好名称
   - description: 爱好描述

6. **student_hobbies (学生爱好关联表)**
   - id: 主键
   - student_id: 学生ID
   - hobby_id: 爱好ID

7. **grades (成绩表)**
   - id: 主键
   - student_id: 学生ID
   - subject: 科目
   - score: 分数
   - semester: 学期
   - academic_year: 学年

### 设计特点
- **无外键约束**: 根据用户要求，数据库设计中不使用外键约束
- **逻辑关联**: 通过应用层逻辑维护数据关系
- **索引优化**: 在关键字段上建立索引提高查询性能

## 安装和部署

### 环境要求
- Python 3.11+
- MySQL 5.7+
- pip (Python 包管理器)

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd cry-python-web
```

2. **创建虚拟环境**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置数据库**
   - 确保 MySQL 服务运行
   - 修改 `config.py` 中的数据库连接信息（如需要）

5. **初始化数据库**
```bash
python app.py
```
首次运行会自动创建数据库表和初始数据

6. **启动应用**
```bash
python app.py
```
应用将在 http://localhost:8000 启动

### 默认账户
- 用户名: `admin`
- 密码: `admin123`

## API 接口

### 统计数据接口
- **URL**: `/api/statistics`
- **方法**: GET
- **描述**: 获取学生统计数据
- **返回**: JSON 格式的统计信息

## 界面特性

### 响应式设计
- 支持桌面端和移动端访问
- Bootstrap 响应式布局
- 自适应图表和表格

### 用户体验
- 直观的侧边栏导航
- 统计卡片展示关键指标
- 交互式图表
- 表单验证和错误提示
- 确认对话框防止误操作

## 开发特点

### 代码组织
- **MVC 架构**: 模型、视图、控制器分离
- **模板继承**: 使用 Jinja2 模板引擎
- **组件化**: 可复用的 HTML 组件

### 安全特性
- 密码哈希加密
- CSRF 保护
- 用户会话管理
- 登录状态验证

### 数据处理
- 分页查询优化
- 数据验证
- 错误处理
- 事务管理

## 扩展建议

1. **功能扩展**
   - 添加课程管理模块
   - 实现成绩分析功能
   - 增加导入/导出功能
   - 添加通知系统

2. **技术优化**
   - 实现 RESTful API
   - 添加缓存机制
   - 数据库连接池
   - 日志系统

3. **界面改进**
   - 深色主题支持
   - 更多图表类型
   - 拖拽排序
   - 高级搜索功能

## 维护说明

### 数据备份
定期备份 MySQL 数据库，建议使用 mysqldump 工具。

### 日志监控
应用运行日志位于控制台输出，生产环境建议配置文件日志。

### 性能优化
- 定期清理过期会话
- 优化数据库查询
- 监控系统资源使用

## 联系信息

如有问题或建议，请联系开发团队。

---

*本文档最后更新时间: 2025年*
