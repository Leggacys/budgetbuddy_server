import asyncio
from quart import Quart
from app.jobs.token_validity import token_refresh_job
from app.database.db import init_db
from app.main_routes import routes

app = Quart(__name__)
app.register_blueprint(routes)

async def main():
    await init_db()
    asyncio.create_task(token_refresh_job())
    await app.run_task(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    asyncio.run(main())
