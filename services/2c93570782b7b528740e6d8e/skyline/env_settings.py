# Skyline Environment Configuration
# This file contains all configurable settings that can be set via environment variables
# or by modifying this file directly.
import os

# Database Configuration (MySQL)
PANORAMA_DBHOST = os.environ.get('PANORAMA_DBHOST', 'localhost')
PANORAMA_DBPORT = os.environ.get('PANORAMA_DBPORT', '3306')
PANORAMA_DBUSER = os.environ.get('PANORAMA_DBUSER', 'root')
PANORAMA_DBUSERPASS = os.environ.get('PANORAMA_DBUSERPASS', '')
PANORAMA_DATABASE = os.environ.get('PANORAMA_DATABASE', 'skyline')

# Redis Configuration
REDIS_SOCKET_PATH = os.environ.get('REDIS_SOCKET_PATH', '/tmp/redis.sock')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

# Memcached Configuration
MEMCACHE_ENABLED = os.environ.get('MEMCACHE_ENABLED', 'True').lower() == 'true'
MEMCACHED_SERVER_IP = os.environ.get('MEMCACHED_SERVER_IP', 'localhost')
MEMCACHED_SERVER_PORT = os.environ.get('MEMCACHED_SERVER_PORT', '11211')

# Graphite Configuration
GRAPHITE_HOST = os.environ.get('GRAPHITE_HOST', 'localhost')
GRAPHITE_PORT = os.environ.get('GRAPHITE_PORT', '80')
GRAPHITE_PROTOCOL = os.environ.get('GRAPHITE_PROTOCOL', 'http')

# Webapp Configuration
WEBAPP_AUTH_ENABLED = os.environ.get('WEBAPP_AUTH_ENABLED', 'True').lower() == 'true'
WEBAPP_AUTH_USER = os.environ.get('WEBAPP_AUTH_USER', 'admin')
WEBAPP_AUTH_USER_PASSWORD = os.environ.get('WEBAPP_AUTH_USER_PASSWORD', 'admin123')
WEBAPP_IP = os.environ.get('WEBAPP_IP', '0.0.0.0')
WEBAPP_PORT = os.environ.get('WEBAPP_PORT', '1500')

# Security
WEBAPP_IP_RESTRICTED = os.environ.get('WEBAPP_IP_RESTRICTED', 'True').lower() == 'true'
WEBAPP_ALLOWED_IPS = os.environ.get('WEBAPP_ALLOWED_IPS', '127.0.0.1').split(',')

# Directory Configuration
LOG_PATH = os.environ.get('LOG_PATH', '/var/log/skyline')
PID_PATH = os.environ.get('PID_PATH', '/var/run/skyline')
SKYLINE_TMP_DIR = os.environ.get('SKYLINE_TMP_DIR', '/tmp/skyline')