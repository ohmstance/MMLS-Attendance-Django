from django.apps import AppConfig

import logging
import datetime

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Import within or exception AppRegistryNotReady happens
        from background_task.models import Task
        from . import views, tasks
        try:
            if not Task.objects.filter(verbose_name="cache_attendance").exists():
                # Schedule a day later from now at 8am
                tz = datetime.timezone(datetime.timedelta(hours=8))
                datetime_later = datetime.datetime.now(tz).replace(hour=8, minute=0, second=0, microsecond=0)

                while datetime.datetime.now(tz) > datetime_later:
                    datetime_later += datetime.timedelta(days=1)

                tasks.update_cache(schedule=datetime_later, repeat=Task.DAILY, verbose_name="cache_attendance")
        except django.db.utils.ProgrammingError as e:
            # Error during migration, ignore.
            logging.info(f"Ignoring exception: {repr(e)}")
            pass
