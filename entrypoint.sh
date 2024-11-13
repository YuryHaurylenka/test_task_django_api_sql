set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
email = 'admin@example.com'; \
password = 'adminpassword'; \
if not User.objects.filter(email=email).exists(): \
    User.objects.create_superuser(email=email, password=password); \
    print('Superuser created.'); \
else: \
    print('Superuser already exists.')"

echo "Starting server..."
exec "$@"
