# BudgetBuddy Server

A Flask/Quart-based API server for the BudgetBuddy application that integrates with Nordigen (GoCardless) for Open Banking functionality.

## Project Structure

```
budgetbuddy_server/
├── app/
│   ├── config.py              # Configuration settings
│   ├── env_loader.py          # Environment variable loader
│   ├── main_routes.py         # Route registration
│   ├── database/              # Database models and methods
│   ├── jobs/                  # Background tasks
│   ├── neutral_end_points/    # Generic API endpoints
│   └── nordingen/             # Nordigen-specific functionality
├── requirements.txt           # Python dependencies
├── run.py                     # Application entry point
└── setup_sandbox.sh          # Sandbox setup script
```

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`

3. Run the server:
   ```bash
   python run.py
   ```

## API Endpoints

### Nordigen Integration

- `POST /create-requisition` - Create bank connection requisition
- `POST /nordigen-add-requisition` - Save requisition after user authentication
- `GET /get_transactions` - Fetch user transactions
- `GET /list-of-banks-from-country` - Get available banks

### User Management

- `POST /login-user` - User authentication
