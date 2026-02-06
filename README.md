Markdown
# 💻 Quansh Tech Computer Shop
### *Full-Stack Enterprise E-Commerce Platform*

![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Vercel](https://img.shields.io/badge/vercel-%23000000.svg?style=for-the-badge&logo=vercel&logoColor=white)

**Live Demo:** [qt-site.vercel.app](https://qt-site.vercel.app/)

## 🚀 Overview 
**Quansh Tech (Public Sample)** is a professional reference implementation of the **QTSite** e-commerce ecosystem. While the full internal version serves as a private enterprise tool, this public repository demonstrates the core architecture, security protocols, and cloud integrations used in the production environment.

The project is engineered to handle the complexities of computer hardware retail, showcasing a complete Software Development Life Cycle (SDLC) approach. It features a decoupled media architecture using **AWS S3**, a relational **PostgreSQL** backend, and a secure **Role-Based Access Control (RBAC)** system designed for high-integrity business operations.


## 🛠️ Key Technical Features
* **Relational Schema Design:** Custom PostgreSQL schemas managing complex relationships between Users, Product Categories, and Multi-tier Orders.
* **Cloud Asset Management:** Integrated `django-storages` and `boto3` to offload static and media files to **AWS S3**, ensuring stateless scalability.
* **Security & RBAC:** Implemented custom decorators and Django’s Permission system to create a "Classified" staff portal for inventory management.
* **Search Optimization:** Full-text product search capabilities implemented via Django QuerySets for high-speed hardware lookups.
* **Asynchronous Readiness:** Configured for background task processing using **Celery** and **AMQP** to handle high-latency operations like email notifications.

## 🏗️ Technical Stack
* **Backend:** Python 3.x, Django 4.2, Django REST Framework
* **Frontend:** JavaScript (ES6+), HTML5, CSS3, Bootstrap 5
* **Database:** PostgreSQL (Production), SQLite (Development)
* **Infrastructure:** AWS (S3, IAM), Vercel, Gunicorn, Whitenoise
* **Integrations:** PayPal SDK, Django-Import-Export (ETL tools)

---



## 🔧 Installation & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Jaycuppp/Sample-Django-Website-For-Computer-Shop.git
cd Sample-Django-Website-For-Computer-Shop
```

### 2. Virtual Environment Setup
   
```Bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate
```

### 3. Dependency Installation
This project relies on several enterprise-grade libraries for cloud storage and database communication.

```Bash
pip install -r requirements.txt
```

### 4. Configuration
Create a .env file in the project root to manage your environment variables securely:

```
SECRET_KEY=your_django_key
DEBUG=True
DATABASE_URL=your_postgres_connection_string
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

### 5. Database Initialization

Inside CMD DIR for manage.py
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 🧬 Architectural Design
The application follows the Model-View-Template (MVT) pattern, optimized for clean separation of concerns:

Models: Standardized data structures with Pillow for image processing and django-resized for frontend optimization.

Middleware: Utilizes Whitenoise for efficient static file serving in production environments.

Database Layer: Managed through psycopg-binary for high-performance Python-to-PostgreSQL communication.

### 👤 Author
Hakob Keshishyan

Portfolio: qt-site.vercel.app

GitHub: @Jaycuppp

💡 Developer Note
If you are testing the Staff Portal, ensure your user account has is_staff and is_superuser flags set to True in the Django Admin panel to access the protected business logic routes.