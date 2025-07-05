#!/bin/bash

# Create or update .env file with sandbox configuration
echo "Creating .env file with sandbox configuration..."

cat > .env << EOF
# Environment Settings
ENVIRONMENT=sandbox

# Nordigen API Credentials (replace with your actual credentials)
NORDIGEN_SECRET_ID=your_nordigen_secret_id_here
NORDIGEN_SECRET_KEY=your_nordigen_secret_key_here

# Redirect URI for bank authentication callback
REDIRECT_URI=http://localhost:3000/callback

# Database URL (if using external database)
# DATABASE_URL=your_database_url_here
EOF

echo "✅ .env file created with sandbox configuration"
echo "📝 Please update the following values in .env:"
echo "   - NORDIGEN_SECRET_ID"
echo "   - NORDIGEN_SECRET_KEY"
echo "   - REDIRECT_URI (if different from localhost:3000/callback)"
echo ""
echo "🏖️ Your application is now configured for sandbox mode!"
