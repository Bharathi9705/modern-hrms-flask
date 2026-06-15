from flask import Blueprint, jsonify

# Ensure this matches the blueprint registration inside your app/__init__.py
dashboard_bp = Blueprint('dashboard_api', __name__)

@dashboard_bp.route('/metrics', methods=['GET'])
def get_dashboard_metrics():
    # This matches the analytical keys parsed by your frontend script
    payload = {
        "total_employees": 42,
        "present_today": 38,
        "pending_leaves": 5,
        "department_distribution": {
            "Engineering": 18,
            "HR": 4,
            "Core Systems": 8,
            "Marketing": 5,
            "Finance": 7
        },
        "attendance_trends": [
            {"date": "Mon", "count": 35},
            {"date": "Tue", "count": 37},
            {"date": "Wed", "count": 38},
            {"date": "Thu", "count": 36},
            {"date": "Fri", "count": 38}
        ]
    }
    return jsonify(payload), 200