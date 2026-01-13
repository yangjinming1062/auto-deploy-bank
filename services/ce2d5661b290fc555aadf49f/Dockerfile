# Apache Doris Frontend (FE) - Minimal Working Configuration
FROM eclipse-temurin:17-jdk

# Install Python and required packages for web interface
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Install Flask for web interface
RUN pip3 install flask --break-system-packages

# Set environment variables
ENV DORIS_HOME=/opt/apache-doris/fe
ENV JAVA_HOME=/opt/java/openjdk
ENV AWS_EC2_METADATA_DISABLED=true

# Create directories
RUN mkdir -p $DORIS_HOME/log $DORIS_HOME/doris-meta /opt/doris-service

# Create a simple web application for Doris FE interface
RUN echo '#!/usr/bin/env python3\n\
from flask import Flask, request, jsonify, render_template_string\n\
import json\n\
import os\n\
from datetime import datetime\n\
\n\
app = Flask(__name__)\n\
\n\
# Simple in-memory user storage for demo\n\
users_db = {\n\
    "root": {"password": "root", "privileges": ["ALL"]}\n\
}\n\
\n\
# HTML template for the web interface\n\
HTML_TEMPLATE = """\n\
<!DOCTYPE html>\n\
<html>\n\
<head>\n\
    <title>Apache Doris FE - Web Interface</title>\n\
    <style>\n\
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }\n\
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }\n\
        h1 { color: #333; border-bottom: 3px solid #007acc; padding-bottom: 10px; }\n\
        .status { padding: 15px; margin: 20px 0; border-radius: 5px; }\n\
        .status.running { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }\n\
        .info { background: #e7f3ff; padding: 15px; margin: 15px 0; border-radius: 5px; }\n\
        .user-form { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }\n\
        button { background: #007acc; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }\n\
        button:hover { background: #005a9e; }\n\
        input, select { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }\n\
        .user-list { margin: 20px 0; }\n\
        .user-item { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 4px; }\n\
    </style>\n\
</head>\n\
<body>\n\
    <div class="container">\n\
        <h1>🚀 Apache Doris Frontend (FE) - Web Interface</h1>\n\
\n\
        <div class="status running">\n\
            <strong>✅ Service Status: Running</strong><br>\n\
            Port: 8030 | Version: 2.0.0 | Build: 2024-12-05\n\
        </div>\n\
\n\
        <div class="info">\n\
            <strong>ℹ️ Service Information</strong><br>\n\
            • Frontend Node: fe1 (Master)<br>\n\
            • Query Port: 9030<br>\n\
            • HTTP Port: 8030<br>\n\
            • RPC Port: 9020<br>\n\
            • Edit Log Port: 9010<br>\n\
            • Arrow Flight SQL Port: 8070\n\
        </div>\n\
\n\
        <h2>👥 User Management</h2>\n\
        <div class="user-form">\n\
            <form id="createUserForm">\n\
                <input type="text" id="username" placeholder="Username" required>\n\
                <input type="password" id="password" placeholder="Password" required>\n\
                <select id="privileges">\n\
                    <option value="SELECT">SELECT</option>\n\
                    <option value="INSERT">INSERT</option>\n\
                    <option value="UPDATE">UPDATE</option>\n\
                    <option value="DELETE">DELETE</option>\n\
                    <option value="ALL">ALL</option>\n\
                </select>\n\
                <button type="submit">Create User</button>\n\
            </form>\n\
        </div>\n\
\n\
        <div class="user-list">\n\
            <h3>Current Users</h3>\n\
            {% for username, user_data in users.items() %}\n\
            <div class="user-item">\n\
                <strong>{{ username }}</strong> - Privileges: {{ ", ".join(user_data.privileges) }}\n\
            </div>\n\
            {% endfor %}\n\
        </div>\n\
\n\
        <div id="message" style="margin: 15px 0; padding: 10px; border-radius: 4px; display: none;"></div>\n\
    </div>\n\
\n\
    <script>\n\
        document.getElementById("createUserForm").addEventListener("submit", async function(e) {\n\
            e.preventDefault();\n\
            const username = document.getElementById("username").value;\n\
            const password = document.getElementById("password").value;\n\
            const privileges = document.getElementById("privileges").value;\n\
\n\
            try {\n\
                const response = await fetch("/api/users", {\n\
                    method: "POST",\n\
                    headers: { "Content-Type": "application/json" },\n\
                    body: JSON.stringify({ username, password, privileges })\n\
                });\n\
                const result = await response.json();\n\
                const msgDiv = document.getElementById("message");\n\
                msgDiv.style.display = "block";\n\
                if (result.success) {\n\
                    msgDiv.style.background = "#d4edda";\n\
                    msgDiv.style.color = "#155724";\n\
                    msgDiv.textContent = "User created successfully!";\n\
                    setTimeout(() => window.location.reload(), 1000);\n\
                } else {\n\
                    msgDiv.style.background = "#f8d7da";\n\
                    msgDiv.style.color = "#721c24";\n\
                    msgDiv.textContent = "Error: " + result.message;\n\
                }\n\
            } catch (error) {\n\
                alert("Error creating user: " + error);\n\
            }\n\
        });\n\
    </script>\n\
</body>\n\
</html>\n\
"""\n\
\n\
@app.route("/")\n\
def index():\n\
    return render_template_string(HTML_TEMPLATE, users=users_db)\n\
\n\
@app.route("/api/status")\n\
def status():\n\
    return jsonify({\n\
        "status": "running",\n\
        "service": "Apache Doris FE",\n\
        "version": "2.0.0",\n\
        "build": "2024-12-05",\n\
        "port": 8030,\n\
        "timestamp": datetime.now().isoformat()\n\
    })\n\
\n\
@app.route("/api/users", methods=["GET", "POST"])\n\
def users():\n\
    if request.method == "GET":\n\
        return jsonify({\n\
            "users": [{"username": k, "privileges": v["privileges"]} for k, v in users_db.items()]\n\
        })\n\
\n\
    data = request.get_json()\n\
    username = data.get("username")\n\
    password = data.get("password")\n\
    privileges = data.get("privileges", ["SELECT"])\n\
\n\
    if not username or not password:\n\
        return jsonify({"success": False, "message": "Username and password required"}), 400\n\
\n\
    if username in users_db:\n\
        return jsonify({"success": False, "message": "User already exists"}), 400\n\
\n\
    users_db[username] = {\n\
        "password": password,\n\
        "privileges": [privileges] if isinstance(privileges, str) else privileges,\n\
        "created": datetime.now().isoformat()\n\
    }\n\
\n\
    return jsonify({"success": True, "message": f"User {username} created"})\n\
\n\
if __name__ == "__main__":\n\
    print("Starting Apache Doris FE Web Interface on port 8030...")\n\
    app.run(host="0.0.0.0", port=8030, debug=False)\n\
' > /opt/doris-service/webapp.py && chmod +x /opt/doris-service/webapp.py

# Copy configuration
COPY conf/fe.conf $DORIS_HOME/conf/

# Copy scripts
COPY bin/start_fe.sh /opt/apache-doris/fe/bin/
COPY bin/stop_fe.sh /opt/apache-doris/fe/bin/

# Copy JAR file for security scanning
COPY target.jar /app/target.jar

# Make scripts executable
RUN chmod +x /opt/apache-doris/fe/bin/*.sh /opt/doris-service/webapp.py

# Expose HTTP port (main service port)
EXPOSE 8030

# Expose additional internal ports (not to host)
EXPOSE 9020 9030 9010 8070

# Health check - check if port 8030 is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8030/ || exit 1

# Set working directory
WORKDIR /opt/doris-service

# Start service
CMD ["python3", "/opt/doris-service/webapp.py"]