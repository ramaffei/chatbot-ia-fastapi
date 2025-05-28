#!/bin/bash
set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes con colores
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [opciones]"
    echo ""
    echo "Opciones:"
    echo "  -h, --help          Mostrar esta ayuda"
    echo "  -o, --output DIR    Directorio de salida (default: ./backups)"
    echo "  -f, --format FORMAT Formato del backup (c=custom, t=tar, p=plain) (default: c)"
    echo "  --no-date          No incluir fecha en el nombre del archivo"
    echo "  --compress LEVEL   Nivel de compresión 0-9 (default: 6)"
    echo ""
    echo "Variables de entorno requeridas (desde .env):"
    echo "  DBName, DBUser, DBPassword, DBHost, DBPort, DBSchema"
}

# Valores por defecto
OUTPUT_DIR="./backups"
FORMAT="c"
INCLUDE_DATE=true
COMPRESSION_LEVEL=6

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        --no-date)
            INCLUDE_DATE=false
            shift
            ;;
        --compress)
            COMPRESSION_LEVEL="$2"
            shift 2
            ;;
        *)
            print_message $RED "❌ Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

print_message $BLUE "🔄 Iniciando proceso de backup..."

# Cargar variables del entorno
if [ -f .env ]; then
    source .env
    print_message $GREEN "✅ Variables cargadas desde .env"
else
    print_message $YELLOW "⚠️  No se encontró archivo .env, usando variables del sistema"
fi

# Verificación de variables requeridas
REQUIRED_VARS=("DBName" "DBUser" "DBHost")
missing_vars=()

for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!var}" ]]; then
        missing_vars+=("$var")
    fi
done

if [[ ${#missing_vars[@]} -gt 0 ]]; then
    print_message $RED "❌ Faltan variables de entorno requeridas:"
    printf '%s\n' "${missing_vars[@]}"
    print_message $YELLOW "💡 Revisá el archivo .env o las variables del sistema"
    exit 1
fi

# Verificar si DBPassword está definida
if [[ -z "$DBPassword" ]]; then
    print_message $YELLOW "⚠️  DBPassword no está definida. Se solicitará interactivamente."
else
    export PGPASSWORD="$DBPassword"
fi

# Crear directorio de salida si no existe
mkdir -p "$OUTPUT_DIR"

# Generar nombre del archivo dinámico
TIMESTAMP=""
if [[ "$INCLUDE_DATE" == true ]]; then
    TIMESTAMP="_$(date +%Y%m%d_%H%M%S)"
fi

# Determinar extensión según formato
case $FORMAT in
    c|custom)
        EXTENSION="dump"
        FORMAT_FLAG="-Fc"
        ;;
    t|tar)
        EXTENSION="tar"
        FORMAT_FLAG="-Ft"
        ;;
    p|plain)
        EXTENSION="sql"
        FORMAT_FLAG="-Fp"
        ;;
    *)
        print_message $RED "❌ Formato no válido: $FORMAT. Use: c, t, o p"
        exit 1
        ;;
esac

# Construir nombre del archivo
FILENAME="${DBName}"
if [[ -n "$DBSchema" ]]; then
    FILENAME="${FILENAME}_${DBSchema}"
fi
FILENAME="${FILENAME}${TIMESTAMP}.${EXTENSION}"
FILEPATH="${OUTPUT_DIR}/${FILENAME}"

print_message $BLUE "📋 Configuración del backup:"
print_message $NC "   • Host: $DBHost:${DBPort:-5432}"
print_message $NC "   • Base de datos: $DBName"
print_message $NC "   • Usuario: $DBUser"
print_message $NC "   • Schema: ${DBSchema:-'todos los schemas'}"
print_message $NC "   • Formato: $FORMAT"
print_message $NC "   • Archivo: $FILEPATH"

# Verificar conectividad antes del backup
print_message $BLUE "🔍 Verificando conectividad..."
if ! pg_isready -h "$DBHost" -p "${DBPort:-5432}" -U "$DBUser" > /dev/null 2>&1; then
    print_message $RED "❌ No se puede conectar a la base de datos"
    print_message $YELLOW "💡 Verificá la conectividad y las credenciales"
    exit 1
fi
print_message $GREEN "✅ Conectividad verificada"

# Construir comando pg_dump
PG_DUMP_CMD="pg_dump -h $DBHost -p ${DBPort:-5432} -U $DBUser -d $DBName"

# Agregar schema si está especificado
if [[ -n "$DBSchema" ]]; then
    PG_DUMP_CMD="$PG_DUMP_CMD -n $DBSchema"
fi

# Agregar opciones adicionales
PG_DUMP_CMD="$PG_DUMP_CMD -x $FORMAT_FLAG"

# Agregar compresión si es formato custom o tar
if [[ "$FORMAT" == "c" || "$FORMAT" == "t" ]]; then
    PG_DUMP_CMD="$PG_DUMP_CMD -Z $COMPRESSION_LEVEL"
fi

PG_DUMP_CMD="$PG_DUMP_CMD -f '$FILEPATH'"

# Ejecutar backup
print_message $BLUE "🔄 Creando backup..."
print_message $NC "Ejecutando: $PG_DUMP_CMD"

if eval $PG_DUMP_CMD; then
    # Obtener tamaño del archivo
    FILE_SIZE=$(du -h "$FILEPATH" | cut -f1)
    print_message $GREEN "✅ Backup creado exitosamente!"
    print_message $GREEN "📁 Archivo: $FILEPATH"
    print_message $GREEN "📊 Tamaño: $FILE_SIZE"
    
    # Mostrar información adicional
    if [[ "$FORMAT" == "c" ]]; then
        print_message $BLUE "💡 Para restaurar usa:"
        print_message $NC "   pg_restore -h HOST -p PORT -U USER -d DATABASE '$FILEPATH'"
    else
        print_message $BLUE "💡 Para restaurar usa:"
        print_message $NC "   psql -h HOST -p PORT -U USER -d DATABASE < '$FILEPATH'"
    fi
else
    print_message $RED "❌ Error al crear el backup"
    exit 1
fi

# Limpiar variable de contraseña
unset PGPASSWORD

print_message $GREEN "🎉 Proceso completado!"