import os
import uvicorn
import asyncio

from malevich_app.export.processes.main import logs_streaming_restart
from malevich_app.export.secondary.const import IS_EXTERNAL, MOUNT_PATH, LOGS_STREAMING, MOUNT_PATH_OBJ

if __name__ == "__main__":
    if IS_EXTERNAL:
        os.makedirs(MOUNT_PATH, exist_ok=True)
        os.makedirs(MOUNT_PATH_OBJ, exist_ok=True)
    if LOGS_STREAMING:
        asyncio.run(logs_streaming_restart(wait=False))
    uvicorn.run("malevich_app.export.api.api:app", host="0.0.0.0", port=int(os.environ["PORT"]), loop="asyncio", reload=False, workers=1)
