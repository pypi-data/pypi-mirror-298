#!/bin/sh

# Run Django management commands
echo "Applying database migrations..."
python manage.py makemigrations --merge
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Compiling messages..."
python manage.py compilemessages

echo "Starting server..."
exec "$@"
