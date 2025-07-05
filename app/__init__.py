"""
BudgetBuddy Server Application Package

This package contains the main application components for the BudgetBuddy server,
including API endpoints, database models, and Nordigen integration.
"""

from quart import Quart
from app.database.db import init_db
from app.main_routes import routes
from app.jobs.token_validity import token_refresh_job
import asyncio

__version__ = "1.0.0"

def create_app():
    """
    Application factory function that creates and configures the Quart app.
    
    Returns:
        Quart: Configured application instance
    """
    app = Quart(__name__)
    
    # Register blueprints
    app.register_blueprint(routes)
    
    return app

async def setup_app():
    """
    Setup function that initializes database and background tasks.
    """
    await init_db()
    asyncio.create_task(token_refresh_job())
