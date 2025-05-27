#!/bin/bash
set -e

DUMP_FILE="/postgres_init/backup.dump"

# Si no existe el archivo, no hacemos nada
if [ ! -f "$DUMP_FILE" ]; then
  echo "⚠️ No se encontró el archivo de backup ($DUMP_FILE). Se dejará la base vacía."
  exit 0
fi

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando que PostgreSQL esté listo..."
until pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; do
  sleep 2
done

# Restaurar el esquema
echo "🔁 Restaurando esquema desde $DUMP_FILE..."
pg_restore --verbose --clean --if-exists --no-owner \
  --username="$POSTGRES_USER" \
  --dbname="$POSTGRES_DB" \
  "$DUMP_FILE"

echo "✅ Restauración completada."