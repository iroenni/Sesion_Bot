#!/usr/bin/env python3
"""
Script para generar sesión string de Pyrogram
Versión mejorada para integración con bot
"""

import asyncio
import os
from pyrogram import Client

async def generate_session_string():
    print("🚀 Generador de Sesión String para Pyrogram")
    print("=" * 60)
    
    # Solicitar datos al usuario
    print("\n📝 Por favor, ingresa los siguientes datos:")
    
    api_id = input("1. Ingresa tu API ID: ").strip()
    api_hash = input("2. Ingresa tu API HASH: ").strip()
    
    # Validar que los campos no estén vacíos
    if not api_id or not api_hash:
        print("❌ Error: API ID y API HASH son obligatorios")
        return
    
    if not api_id.isdigit():
        print("❌ Error: API ID debe ser numérico")
        return
    
    print("\n📱 Ahora necesitarás iniciar sesión en tu cuenta de Telegram")
    print("💡 Se te pedirá:")
    print("   - Tu número de teléfono (con código de país, ej: +34123456789)")
    print("   - El código de verificación que recibas")
    print("   - Contraseña de 2FA (si está activada)")
    print("\n⏳ Iniciando proceso de autenticación...")
    
    try:
        # Crear cliente temporal
        client = Client(
            name="session_generator",
            api_id=int(api_id),
            api_hash=api_hash,
            in_memory=True  # No guardar archivo de sesión
        )
        
        # Iniciar cliente
        await client.start()
        
        # Obtener la sesión string
        session_string = await client.export_session_string()
        
        # Obtener información del usuario
        me = await client.get_me()
        
        print("\n" + "=" * 60)
        print("✅ SESIÓN STRING GENERADA EXITOSAMENTE")
        print("=" * 60)
        
        print(f"\n👤 Información de la cuenta:")
        print(f"   Nombre: {me.first_name or ''} {me.last_name or ''}".strip())
        print(f"   Username: @{me.username}" if me.username else "   Username: No disponible")
        print(f"   ID: {me.id}")
        print(f"   Número: {me.phone_number}")
        
        print(f"\n📋 Tu sesión string es:\n")
        print(session_string)
        print("\n" + "=" * 60)
        
        # Opción para guardar en archivo
        save_file = input("\n💾 ¿Quieres guardar la sesión en un archivo? (s/n): ").strip().lower()
        if save_file in ['s', 'si', 'sí', 'y', 'yes']:
            filename = input("📁 Nombre del archivo (sin extensión): ").strip()
            if not filename:
                filename = "telegram_session"
            
            with open(f"{filename}.txt", "w", encoding="utf-8") as f:
                f.write(f"API_ID = {api_id}\n")
                f.write(f"API_HASH = {api_hash}\n")
                f.write(f"SESSION_STRING = {session_string}\n")
                f.write(f"\n# Información de la cuenta:\n")
                f.write(f"# Nombre: {me.first_name or ''} {me.last_name or ''}\n".strip())
                f.write(f"# Username: @{me.username}\n" if me.username else "# Username: No disponible\n")
                f.write(f"# User ID: {me.id}\n")
                f.write(f"# Número: {me.phone_number}\n")
            
            print(f"✅ Sesión guardada en: {filename}.txt")
        
        print("\n🔧 **Para usar en Render:**")
        print("1. Ve a tu dashboard de Render")
        print("2. Selecciona tu servicio")
        print("3. Ve a la sección 'Environment'")
        print("4. Agrega estas variables:")
        print(f"   API_ID = {api_id}")
        print(f"   API_HASH = {api_hash}")
        print(f"   SESSION_STRING = {session_string}")
        
        print("\n🎯 **Para usar en el bot:**")
        print("\nfrom pyrogram import Client")
        print("import asyncio")
        print("\nasync def main():")
        print("    async with Client(")
        print("        name=\"my_account\",")
        print(f"        api_id={api_id},")
        print(f"        api_hash=\"{api_hash}\",")
        print(f"        session_string=\"{session_string}\"")
        print("    ) as app:")
        print("        me = await app.get_me()")
        print("        print(f\"Conectado como: {me.first_name}\")")
        print("\nasyncio.run(main())")
        
        print("\n⚠️  **ADVERTENCIA DE SEGURIDAD:**")
        print("   • Guarda esta sesión string de forma SEGURA")
        print("   • NO la compartas con nadie")
        print("   • Quien tenga esta sesión puede acceder a tu cuenta")
        
        # Detener el cliente
        await client.stop()
        
    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
        print("\n🔧 Posibles soluciones:")
        print("   - Verifica tu API ID y API HASH")
        print("   - Asegúrate de tener conexión a internet")
        print("   - Verifica que el número de teléfono sea correcto")
        print("   - Si usas VPN, intenta desactivarla temporalmente")

def main():
    """Función principal"""
    print("🔧 Verificando dependencias...")
    
    try:
        import pyrogram
        print("✅ Pyrogram está instalado")
    except ImportError:
        print("❌ Pyrogram no está instalado.")
        print("   Instálalo con: pip install pyrogram")
        return
    
    try:
        asyncio.run(generate_session_string())
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()