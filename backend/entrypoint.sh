#!/bin/bash
set -e

# انتظر PostgreSQL فقط إذا كان مستخدماً (POSTGRES_HOST محدد)
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for database at $POSTGRES_HOST..."
  python - <<'END'
import os, sys, time
import psycopg2

for i in range(30):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB", "cvstudio"),
            user=os.environ.get("POSTGRES_USER", "cvstudio"),
            password=os.environ.get("POSTGRES_PASSWORD", ""),
            host=os.environ["POSTGRES_HOST"],
            port=os.environ.get("POSTGRES_PORT", "5432"),
        )
        conn.close()
        print("Database is ready!")
        break
    except psycopg2.OperationalError:
        print(f"Database not ready ({i + 1}/30)...")
        time.sleep(1)
else:
    print("ERROR: Database not ready after 30 attempts")
    sys.exit(1)
END
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
exec "$@"
