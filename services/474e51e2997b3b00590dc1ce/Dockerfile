# Use python:3.9-slim as the base image, meeting the project's Python version requirements.
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Install curl for healthchecks and build dependencies for psycopg2
RUN apt-get update && apt-get install -y curl libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a new Django project to serve the API
RUN django-admin startproject myproject .

# Modify settings.py to include 'rest_framework' and the REST_FRAMEWORK configuration
# Also, allow all hosts since we're in a container
RUN sed -i "/'django.contrib.staticfiles',/a \ \ \ \ 'rest_framework'," myproject/settings.py
RUN echo "REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly']}" >> myproject/settings.py
RUN sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = ['*']/g" myproject/settings.py

# Overwrite urls.py with the example from the README
RUN echo 'from django.contrib.auth.models import User' > myproject/urls.py && \
    echo 'from django.urls import include, path' >> myproject/urls.py && \
    echo 'from rest_framework import routers, serializers, viewsets' >> myproject/urls.py && \
    echo '' >> myproject/urls.py && \
    echo 'class UserSerializer(serializers.HyperlinkedModelSerializer):' >> myproject/urls.py && \
    echo '    class Meta:' >> myproject/urls.py && \
    echo '        model = User' >> myproject/urls.py && \
    echo '        fields = ["url", "username", "email", "is_staff"]' >> myproject/urls.py && \
    echo '' >> myproject/urls.py && \
    echo 'class UserViewSet(viewsets.ModelViewSet):' >> myproject/urls.py && \
    echo '    queryset = User.objects.all()' >> myproject/urls.py && \
    echo '    serializer_class = UserSerializer' >> myproject/urls.py && \
    echo '' >> myproject/urls.py && \
    echo 'router = routers.DefaultRouter()' >> myproject/urls.py && \
    echo "router.register(r'users', UserViewSet)" >> myproject/urls.py && \
    echo '' >> myproject/urls.py && \
    echo 'urlpatterns = [' >> myproject/urls.py && \
    echo "    path('', include(router.urls))," >> myproject/urls.py && \
    echo "    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))," >> myproject/urls.py && \
    echo ']' >> myproject/urls.py

# Run database migrations
RUN python manage.py migrate

# Create a superuser using the provided script
RUN python create_user_script.py

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
