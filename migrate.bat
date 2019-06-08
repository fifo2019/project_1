python manage.py migrate
echo "start_migratin_done"
pause
python manage.py makemigrations
echo "migrations_created"
pause
python manage.py migrate
echo "migrations_done"
pause