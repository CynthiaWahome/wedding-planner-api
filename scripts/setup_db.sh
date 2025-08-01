#!/bin/bash
set -euo pipefail

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

run_psql_super() {
    PGPASSWORD="${POSTGRES_PASSWORD:-}" psql -U postgres -h "$DBHOST" -p "$DBPORT" -d postgres -c "$1"
}

run_psql_db() {
    PGPASSWORD="$DBPASSWORD" psql -U "$DBUSER" -h "$DBHOST" -p "$DBPORT" -d "$DBNAME" -c "$1"
}

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

ENV_PATH="$(dirname "$0")/../.env"
if [ -f "$ENV_PATH" ]; then
    set -a
    source "$ENV_PATH"
    set +a
    log "Loaded environment variables from .env"
else
    log "ERROR: .env file not found. Please create one based on .env.example"
    exit 1
fi

for var in DBNAME DBUSER DBPASSWORD DBHOST DBPORT; do
    if [ -z "${!var:-}" ]; then
        log "ERROR: Missing required environment variable: $var"
        exit 1
    fi
done

# =============================================================================
# DATABASE SETUP PROCESS
# =============================================================================

log "Dropping database '$DBNAME' if it exists..."
run_psql_super "DROP DATABASE IF EXISTS \"$DBNAME\";"

log "Checking if user '$DBUSER' exists..."
if run_psql_super "SELECT 1 FROM pg_roles WHERE rolname='$DBUSER';" | grep -q "1"; then
    log "User '$DBUSER' already exists. Updating password..."
    run_psql_super "ALTER USER \"$DBUSER\" WITH PASSWORD '$DBPASSWORD';"
else
    log "Creating user '$DBUSER'..."
    run_psql_super "CREATE USER \"$DBUSER\" WITH PASSWORD '$DBPASSWORD';"
fi

log "Creating database '$DBNAME' owned by '$DBUSER'..."
run_psql_super "CREATE DATABASE \"$DBNAME\" OWNER \"$DBUSER\";"

log "Granting privileges..."
run_psql_super "GRANT ALL PRIVILEGES ON DATABASE \"$DBNAME\" TO \"$DBUSER\";"

# =============================================================================
# VERIFICATION
# =============================================================================

log "Testing database connection..."
PGPASSWORD="$DBPASSWORD" psql -U "$DBUSER" -h "$DBHOST" -p "$DBPORT" -d "$DBNAME" -c '\q'

log "✅ Database setup completed successfully!"

echo ""
echo "Next steps:"
echo "1. Log into the database to confirm setup:"
echo "   psql -U $DBUSER -h $DBHOST -p $DBPORT -d $DBNAME"
echo ""
echo "2. Run Django migrations:"
echo "   python3 manage.py makemigrations"
echo "   python3 manage.py migrate"
echo ""
echo "3. Start the development server:"
echo "   python3 manage.py runserver"
echo ""
