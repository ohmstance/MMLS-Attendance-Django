import json
import asyncio
from background_task import background

from .modules import mmlsattendance

@background
def update_cache():
    with open("app/modules/attendance_cache.json", "r+") as f:
        attendance_cache = json.loads(f.read())

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        attendance_cache = loop.run_until_complete(mmlsattendance.update_cache(attendance_cache))
    finally:
        loop.close()
    
    with open("app/modules/attendance_cache.json", "w") as f:
        f.write(json.dumps(attendance_cache))