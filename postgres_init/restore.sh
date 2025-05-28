#!/bin/bash
set -e

DUMP_FILE="/postgres_init/backup.dump"

# Verificar que las variables necesarias estén definidas
if [ -z "$POSTGRES_SCHEMA" ]; then
  echo "❌ Error: La variable POSTGRES_SCHEMA no está definida"
  exit 1
fi

# Si no existe el archivo, creamos solo el schema
if [ ! -f "$DUMP_FILE" ]; then
  echo "⚠️ No se encontró el archivo de backup ($DUMP_FILE). Se creará solo el schema."
  
  # Esperar a que PostgreSQL esté listo
  echo "⏳ Esperando que PostgreSQL esté listo..."
  until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
    sleep 2
  done
  
  echo "📝 Creando schema: $POSTGRES_SCHEMA"
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS ${POSTGRES_SCHEMA};
    GRANT ALL PRIVILEGES ON SCHEMA ${POSTGRES_SCHEMA} TO ${POSTGRES_USER};
    -- Opcional: establecer el schema como default para el usuario
    ALTER USER ${POSTGRES_USER} SET search_path = ${POSTGRES_SCHEMA}, public;
EOSQL
  
  echo "✅ Schema '$POSTGRES_SCHEMA' creado exitosamente."
  exit 0
fi

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando que PostgreSQL esté listo..."
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
  sleep 2
done

# Restaurar el dump
echo "🔁 Restaurando esquema desde $DUMP_FILE..."
pg_restore --verbose --clean --if-exists --no-owner \
  --username="$POSTGRES_USER" \
  --dbname="$POSTGRES_DB" \
  "$DUMP_FILE"

echo "✅ Restauración completada."

# Si el dump no incluía el schema, crearlo después
echo "📝 Verificando/creando schema: $POSTGRES_SCHEMA"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE SCHEMA IF NOT EXISTS ${POSTGRES_SCHEMA};
  GRANT ALL PRIVILEGES ON SCHEMA ${POSTGRES_SCHEMA} TO ${POSTGRES_USER};
EOSQL

echo "✅ Proceso completado exitosamente."