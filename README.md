# 🏢 HRMS Portal — Human Resource Management System

> A full-stack enterprise-grade HRMS web application built with **Flask + SQLite + JWT Auth** and a modern **dark navy UI** with purple accents.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.2-black?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=flat-square&logo=sqlite)
![JWT](https://img.shields.io/badge/JWT-Auth-purple?style=flat-square&logo=jsonwebtokens)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-CDN-38bdf8?style=flat-square&logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

| Module | Features |
|---|---|
| 🔐 **Authentication** | JWT-based login, role-based access (admin / hr_manager / employee), secure token storage |
| 👥 **Employee Management** | Add, view, search, filter, paginate and delete employees with department/role filters |
| ⏰ **Attendance Tracking** | Clock in/out system with live shift timer, duration calculation, daily summaries |
| 📅 **Leave Management** | Apply leave, approve/reject workflow, status tabs (All/Pending/Approved/Rejected) |
| 📊 **Dashboard Analytics** | Real-time stat cards, Chart.js doughnut + bar charts, animated counters |
| 📤 **CSV Export** | One-click export on Employees, Attendance and Leave pages |
| 🌙 **Dark/Light Mode** | Toggle between deep navy dark and clean light theme, saved to localStorage |
| 🍞 **Toast Notifications** | Non-blocking success/error/warning/info toasts on all actions |
| 💀 **Loading Skeletons** | Skeleton loaders while API data fetches |
| 📭 **Empty States** | Beautiful illustrated empty states on all tables |

---

## 🖥️ Screenshots

### Login Page
> Split-panel design with branding on left, clean login form on right

### Dashboard
> Real-time analytics with stat cards, department doughnut chart, and weekly attendance bar chart

### Employee Directory
> Searchable, filterable, paginated employee table with avatar initials

### Leave Requests
> Apply leave modal, status tabs, admin approve/reject workflow

---

## 🛠️ Tech Stack

**Backend**
- Python 3.11+
- Flask 3.0.2
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.6.0
- Werkzeug (password hashing)
- SQLite (database)

**Frontend**
- Vanilla HTML/CSS/JS (no frontend framework)
- Tailwind CSS (via CDN)
- Chart.js (analytics charts)
- Font Awesome 6.5 (icons)
- Google Fonts — Inter

---

## 📁 Project Structure

```
HRMS_sys/
├── app/
│   ├── __init__.py          # App factory, blueprint registration
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── employee.py      # Employee model
│   │   ├── attendance.py    # Attendance model
│   │   ├── leave.py         # Leave model
│   │   └── audit.py         # Audit log model
│   ├── routes/
│   │   ├── auth_api.py      # Login & register endpoints
│   │   ├── dashboard_api.py # Analytics metrics endpoint
│   │   ├── employee_api.py  # Employee CRUD endpoints
│   │   ├── attendance_api.py# Clock in/out endpoints
│   │   ├── leave_api.py     # Leave apply/approve endpoints
│   │   └── views.py         # HTML page routes
│   ├── templates/
│   │   ├── base.html        # Base layout with global CSS/JS
│   │   ├── sidebar.html     # Navigation sidebar component
│   │   ├── login.html       # Login page
│   │   ├── dashboard.html   # Dashboard with charts
│   │   ├── employees.html   # Employee directory
│   │   ├── attendance.html  # Attendance tracking
│   │   └── leaves.html      # Leave management
│   └── utils/
│       └── auth_decorator.py# JWT token decorator
├── run.py                   # App entry point
├── seed.py                  # Database seeder with sample data
├── requirements.txt         # Python dependencies
└── hrms.db                  # SQLite database (auto-created)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Bharathi9705/hrms-portal.git
cd hrms-portal

# 2. Create virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed the database with sample data
python seed.py

# 5. Run the application
python run.py
```

### Access the App
Open your browser and go to:
```
http://127.0.0.1:8080
```

---

## 🔑 Default Login Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `hai` | `admin` |
| Employee | `john_doe` | `Welcome2026!` |
| Employee | `jane_smith` | `Welcome2026!` |
| Employee | `raj_kumar` | `Welcome2026!` |

---

## 🔗 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/login` | Login and get JWT token |
| POST | `/api/auth/register` | Register new employee |

### Employees
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/employees` | Get all employees (with search/filter) |
| POST | `/api/employees` | Create employee |
| DELETE | `/api/employees/<id>` | Delete employee |

### Attendance
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/attendance` | Get all attendance records |
| GET | `/api/attendance/status` | Get current clock status |
| POST | `/api/attendance/clock-action` | Clock in or clock out |

### Leaves
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/leaves` | Get all leave requests |
| POST | `/api/leaves/apply` | Apply for leave |
| PUT | `/api/leaves/<id>` | Approve or reject leave |

### Dashboard
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/metrics` | Get analytics metrics |

---

## 👤 Role Permissions

| Feature | Admin | HR Manager | Employee |
|---|---|---|---|
| View Dashboard | ✅ | ✅ | ✅ |
| View Employees | ✅ | ✅ | ❌ |
| Add Employee | ✅ | ✅ | ❌ |
| Delete Employee | ✅ | ✅ | ❌ |
| View Attendance | ✅ | ✅ | Own only |
| Clock In/Out | ✅ | ✅ | ✅ |
| View Leaves | ✅ | ✅ | Own only |
| Apply Leave | ✅ | ✅ | ✅ |
| Approve/Reject Leave | ✅ | ✅ | ❌ |

---

## 🎨 UI Design System

- **Background:** `#050816` (deep navy)
- **Surface:** `#0b1120`
- **Card:** `#0f1a2e`
- **Accent:** `#7c3aed` (violet/purple)
- **Success:** `#10b981` (emerald)
- **Warning:** `#f59e0b` (amber)
- **Danger:** `#ef4444` (red)
- **Font:** Inter (Google Fonts)

---

## 📦 Requirements

```
Flask==3.0.2
Flask-SQLAlchemy==3.1.1
Flask-JWT-Extended==4.6.0
PyJWT==2.8.0
werkzeug==3.0.1
```

---

## 🙋‍♀️ Author

**Bharathi A**
- 📧 Email: bharathi20061882@gmail.com
- 🐙 GitHub: [@Bharathi9705](https://github.com/Bharathi9705)
- 💼 LinkedIn: [bharathi-a-91543b290](https://linkedin.com/in/bharathi-a-91543b290)

> B.E. Electronics & Communication Engineering — SKCET Coimbatore (2023–2027)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

⭐ **If you found this project helpful, please give it a star!**