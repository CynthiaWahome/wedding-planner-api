#!/bin/bash

# Wedding Planner API Database Setup Script
# Automatically creates database if it doesn't exist

set -e  # Exit on any error

echo "🎯 Setting up PostgreSQL database for Wedding Planner API..."

# Load environment variables
if [ -f .env ]; then
    echo "✅ Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found! Please copy example.env to .env and configure it."
    exit 1
fi

# Set defaults if not provided
DBNAME=${DBNAME:-wedding_planner_dev}
DBUSER=${DBUSER:-postgres}
DBHOST=${DBHOST:-localhost}
DBPORT=${DBPORT:-5432}

echo "📋 Database Configuration:"
echo "   Host: $DBHOST:$DBPORT"
echo "   Database: $DBNAME"
echo "   User: $DBUSER"

# Check if PostgreSQL is running
if ! pg_isready -h "$DBHOST" -p "$DBPORT" > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running on $DBHOST:$DBPORT"
    echo "💡 Please start PostgreSQL first:"
    echo "   macOS: brew services start postgresql"
    echo "   Ubuntu: sudo systemctl start postgresql"
    echo "   Windows: net start postgresql-x64-[version]"
    exit 1
fi

echo "✅ PostgreSQL is running"

# Check if database exists, create if it doesn't
DB_EXISTS=$(PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -p "$DBPORT" -U "$DBUSER" -lqt | cut -d \| -f 1 | grep -w "$DBNAME" | wc -l)

if [ "$DB_EXISTS" -eq "0" ]; then
    echo "🔨 Creating database '$DBNAME'..."
    PGPASSWORD="$DBPASSWORD" createdb -h "$DBHOST" -p "$DBPORT" -U "$DBUSER" "$DBNAME"
    echo "✅ Database '$DBNAME' created successfully!"
else
    echo "✅ Database '$DBNAME' already exists"
fi

# Test connection
echo "🔍 Testing database connection..."
if PGPASSWORD="$DBPASSWORD" psql -h "$DBHOST" -p "$DBPORT" -U "$DBUSER" -d "$DBNAME" -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Database connection successful!"
else
    echo "❌ Failed to connect to database"
    echo "💡 Please check your database credentials in .env file"
    exit 1
fi

echo ""
echo "🎉 Database setup completed successfully!"
echo "💡 Next steps:"
echo "   1. python manage.py migrate"
echo "   2. python manage.py runserver"
echo ""
