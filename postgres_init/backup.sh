#!/bin/bash
set -e

# Cargar variables del entorno
source .env

# Verificación rápida
if [[ -z "$DBName" || -z "$DBUser" || -z "$DBHost" ]]; then
  echo "Faltan variables de entorno requeridas. Revisá el archivo .env"
  exit 1
fi

# Exportar contraseña para que pg_dump no la pida
export PGPASSWORD="$DBPassword"

# Crear el backup en formato personalizado
pg_dump -h "$DBHost" \
        -p "${DBPort:-5432}" \
        -U "$DBUser" \
        -d "$DBName" \
        -n "$DBSchema" \
        -x \
        -Fc \
        -f "backup.dump"

echo "✅ Backup creado: backup.dump"