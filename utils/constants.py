import os

root_path = os.path.realpath(os.path.join(os.path.curdir, "logs"))

# https://automation.trendmicro.com/xdr/cookbook-v3
paths = {
    "root": root_path,                                             # Home
    "workbench": os.path.join(root_path, "Workbench"),       # Workbench/Alerts
    "audit_logs": os.path.join(root_path, "Audit-Logs"),           # Audit Logs
    "OAT": os.path.join(root_path, "Observed-Attack-Techniques"),  # OAT
    "detections": os.path.join(root_path, "Detections"),           # Detection
}

logs_ids = []
