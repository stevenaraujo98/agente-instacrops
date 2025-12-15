#!/usr/bin/env python3
"""
Script para configurar y gestionar la base de datos del proyecto InstaCrops
"""

import os
import sys
from database.db_init import init_db
from database.connection import get_db_connection, DB_PATH

def check_database():
    """Verifica si la base de datos existe y tiene datos"""
    if not os.path.exists(DB_PATH):
        print(f"❌ Base de datos no encontrada en: {DB_PATH}")
        return False
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT count(*) FROM sensores')
        count = cursor.fetchone()[0]
        conn.close()
        
        print(f"✅ Base de datos encontrada con {count} registros")
        return True
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {e}")
        return False

def create_database():
    """Crea la base de datos y la inicializa con datos"""
    print("🔄 Creando base de datos...")
    try:
        init_db()
        print("✅ Base de datos creada exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error al crear la base de datos: {e}")
        return False

def reset_database():
    """Elimina y recrea la base de datos"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Base de datos anterior eliminada")
    
    return create_database()

def show_sample_data():
    """Muestra algunos datos de ejemplo de la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT type, value, date, ubication, city 
            FROM sensores 
            ORDER BY date DESC 
            LIMIT 10
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        print("\n📊 Últimos 10 registros:")
        print("-" * 80)
        for row in rows:
            print(f"{row['type']:15} | {row['value']:6.2f} | {row['date']} | {row['ubication']:12} | {row['city']}")
        
    except Exception as e:
        print(f"❌ Error al mostrar datos: {e}")

def main():
    """Función principal"""
    print("🌱 Configurador de Base de Datos - InstaCrops")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "check":
            check_database()
        elif command == "create":
            create_database()
        elif command == "reset":
            reset_database()
        elif command == "show":
            show_sample_data()
        else:
            print("❌ Comando no reconocido")
            print_help()
    else:
        # Modo interactivo
        if not check_database():
            response = input("\n¿Deseas crear la base de datos? (s/n): ")
            if response.lower() in ['s', 'si', 'y', 'yes']:
                create_database()
        else:
            show_sample_data()

def print_help():
    """Muestra ayuda de comandos"""
    print("\nComandos disponibles:")
    print("  python setup_database.py check  - Verifica si la BD existe")
    print("  python setup_database.py create - Crea la base de datos")
    print("  python setup_database.py reset  - Elimina y recrea la BD")
    print("  python setup_database.py show   - Muestra datos de ejemplo")

if __name__ == "__main__":
    main()