web: python mmls_attendance_grabber/manage.py collectstatic --noinput; cd mmls_attendance_grabber && python -m daphne -b 0.0.0.0 -p $PORT mmls_attendance_grabber.asgi:application
worker: cd mmls_attendance_grabber && python manage.py process_tasks
