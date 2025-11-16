#!/usr/bin/env python3
"""
Bot de elegram con generador de sesiones string integrado
Sistema profesional para despliegue en Render
"""

import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    Message
)
from pyrogram.errors import BadRequest, SessionPasswordNeeded
from session_manager import SessionManager

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración desde variables de entorno
API_ID = int(os.getenv("API_ID", 14681595))
API_HASH = os.getenv("API_HASH", "a86730aab5c59953c424abb4396d32d5")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7486499541:AAEouB0D_NwkrxC81L-7RE99jO9oTZCCcfo")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Inicializar cliente y manager
if BOT_TOKEN:
    app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
elif SESSION_STRING:
    app = Client("user_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
else:
    raise ValueError("Se requiere BOT_TOKEN o SESSION_STRING")

session_manager = SessionManager()

# ==================== SISTEMA DE MENÚS PROFESIONAL ====================

def get_main_menu():
    """Menú principal profesional"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔐 Generar Sesión", callback_data="generate_session"),
            InlineKeyboardButton("📊 Mi Información", callback_data="my_info")
        ],
        [
            InlineKeyboardButton("⚙️ Configuración", callback_data="settings"),
            InlineKeyboardButton("❓ Soporte", callback_data="support")
        ],
        [
            InlineKeyboardButton("🌐 Documentación", url="https://docs.pyrogram.org"),
            InlineKeyboardButton("⭐ Valorar", callback_data="rate_bot")
        ]
    ])

def get_session_menu():
    """Menú para generación de sesiones"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Iniciar Generación", callback_data="start_session_generation"),
            InlineKeyboardButton("📚 Guía Paso a Paso", callback_data="session_guide")
        ],
        [
            InlineKeyboardButton("⚠️ Seguridad", callback_data="security_info"),
            InlineKeyboardButton("🔙 Menú Principal", callback_data="main_menu")
        ]
    ])

def get_cancel_button():
    """Botón para cancelar operaciones"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel_operation")]
    ])

def get_back_to_main():
    """Botón para volver al menú principal"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Menú Principal", callback_data="main_menu")]
    ])

# ==================== MANEJADORES DE COMANDOS ====================

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    """Comando /start - Bienvenida profesional"""
    welcome_text = """
🎯 **Bienvenido al Sistema de Gestión de Sesiones de Telegram**

**Servicios Disponibles:**
• 🔐 **Generación Segura** de Sesiones String
• 📊 **Gestión de Cuentas** y Información
• ⚡ **Proceso Automatizado** paso a paso
• 🔒 **Almacenamiento Seguro** de credenciales

**¿Qué deseas hacer?**
    """
    
    await message.reply_text(
        welcome_text,
        reply_markup=get_main_menu(),
        disable_web_page_preview=True
    )

@app.on_message(filters.command("menu") & filters.private)
async def menu_command(client, message: Message):
    """Comando /menu - Navegación principal"""
    await message.reply_text(
        "**Panel de Control Principal**\nSelecciona una opción:",
        reply_markup=get_main_menu()
    )

@app.on_message(filters.command("session") & filters.private)
async def session_command(client, message: Message):
    """Comando directo para generación de sesiones"""
    session_text = """
🔐 **Sistema de Generación de Sesiones String**

**Características de Seguridad:**
• ✅ Proceso completamente seguro
• 🔒 Datos encriptados en memoria
• 🚫 Sin almacenamiento permanente
• ⚡ Generación rápida y confiable

**¿Estás listo para comenzar?**
    """
    
    await message.reply_text(
        session_text,
        reply_markup=get_session_menu()
    )

# ==================== SISTEMA DE GENERACIÓN DE SESIONES ====================

@app.on_callback_query(filters.regex("^generate_session$"))
async def generate_session_callback(client, callback_query):
    """Iniciar proceso de generación de sesión"""
    guide_text = """
📋 **Proceso de Generación de Sesión**

**Requisitos Previos:**
1. **API_ID** y **API_HASH** de [my.telegram.org](https://my.telegram.org)
2. Número de teléfono con código de país
3. Código de verificación de Telegram
4. Contraseña 2FA (si está activada)

**Pasos del Proceso:**
1. Ingreso de credenciales API
2. Autenticación con número telefónico
3. Verificación con código
4. Generación de sesión string
5. Entrega segura de resultados

**¿Deseas continuar?**
    """
    
    await callback_query.edit_message_text(
        guide_text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Comenzar", callback_data="start_session_generation"),
                InlineKeyboardButton("📖 Ver Guía", callback_data="detailed_guide")
            ],
            [InlineKeyboardButton("🔙 Menú Principal", callback_data="main_menu")]
        ]),
        disable_web_page_preview=True
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex("^start_session_generation$"))
async def start_session_generation(client, callback_query):
    """Iniciar el proceso de generación paso a paso"""
    user_id = callback_query.from_user.id
    
    # Inicializar estado de sesión para el usuario
    session_manager.init_user_session(user_id)
    
    # Paso 1: Solicitar API_ID
    await callback_query.edit_message_text(
        """
🔑 **Paso 1 de 4: Configuración API**

Por favor, envía tu **API_ID**:

1. Ve a [my.telegram.org](https://my.telegram.org)
2. Inicia sesión con tu cuenta
3. Ve a **API Development Tools**
4. Copia tu **API_ID** y envíalo aquí

**Formato:** Solo números
        """,
        reply_markup=get_cancel_button(),
        disable_web_page_preview=True
    )
    await callback_query.answer()

@app.on_message(filters.private & filters.text & ~filters.command(["start", "menu", "cancel"]))
async def handle_session_data(client, message: Message):
    """Manejar los datos ingresados durante la generación de sesión"""
    user_id = message.from_user.id
    user_session = session_manager.get_user_session(user_id)
    
    if not user_session:
        return
    
    text = message.text.strip()
    
    try:
        if user_session.step == "waiting_api_id":
            # Validar API_ID
            if not text.isdigit():
                await message.reply_text(
                    "❌ **API_ID debe contener solo números.**\nPor favor, envía tu API_ID nuevamente:",
                    reply_markup=get_cancel_button()
                )
                return
            
            user_session.api_id = int(text)
            user_session.step = "waiting_api_hash"
            
            await message.reply_text(
                """
🔐 **Paso 2 de 4: API Hash**

Ahora envía tu **API_HASH**:

1. En [my.telegram.org](https://my.telegram.org)
2. En la misma sección **API Development Tools**
3. Copia el **API_HASH** (cadena de texto)
4. Envíalo aquí

**Formato:** Cadena alfanumérica
                """,
                reply_markup=get_cancel_button(),
                disable_web_page_preview=True
            )
        
        elif user_session.step == "waiting_api_hash":
            # Validar API_HASH
            if len(text) < 10:
                await message.reply_text(
                    "❌ **API_HASH parece inválido.**\nPor favor, envía tu API_HASH nuevamente:",
                    reply_markup=get_cancel_button()
                )
                return
            
            user_session.api_hash = text
            user_session.step = "waiting_phone"
            
            await message.reply_text(
                """
📱 **Paso 3 de 4: Número de Teléfono**

Ahora envía tu **número de teléfono**:

**Formato internacional requerido:**
• **Ejemplo:** +34123456789
• Código de país (+34, +52, +1, etc.)
• Número completo sin espacios

**Tu número:**
                """,
                reply_markup=get_cancel_button()
            )
        
        elif user_session.step == "waiting_phone":
            # Validar número de teléfono
            if not text.startswith('+'):
                await message.reply_text(
                    "❌ **Formato incorrecto.**\nDebe empezar con '+' y código de país.\nEjemplo: +34123456789\n\nEnvía tu número nuevamente:",
                    reply_markup=get_cancel_button()
                )
                return
            
            user_session.phone_number = text
            user_session.step = "processing"
            
            # Iniciar proceso de autenticación
            await process_authentication(client, message, user_session)
        
        elif user_session.step == "waiting_code":
            # Procesar código de verificación
            user_session.verification_code = text
            await process_verification_code(client, message, user_session)
        
        elif user_session.step == "waiting_password":
            # Procesar contraseña 2FA
            user_session.two_factor_password = text
            await process_two_factor(client, message, user_session)
    
    except Exception as e:
        logger.error(f"Error en proceso de sesión: {e}")
        await message.reply_text(
            "❌ **Error en el proceso.**\nPor favor, usa /menu para reiniciar.",
            reply_markup=get_back_to_main()
        )
        session_manager.clear_user_session(user_id)

async def process_authentication(client, message: Message, user_session):
    """Procesar la autenticación con los datos proporcionados"""
    user_id = message.from_user.id
    
    try:
        # Crear cliente temporal
        temp_client = Client(
            name=f"session_{user_id}",
            api_id=user_session.api_id,
            api_hash=user_session.api_hash,
            in_memory=True
        )
        
        await temp_client.connect()
        
        # Solicitar código de verificación
        sent_code = await temp_client.send_code(user_session.phone_number)
        user_session.phone_code_hash = sent_code.phone_code_hash
        user_session.temp_client = temp_client
        user_session.step = "waiting_code"
        
        await message.reply_text(
            """
📨 **Paso 4 de 4: Código de Verificación**

Se ha enviado un código de verificación a tu cuenta de Telegram.

**Por favor, envía el código que recibiste:**

• El código tiene 5 dígitos
• Si no lo recibes, puedes solicitar uno por llamada
• El código expira en unos minutos
            """,
            reply_markup=get_cancel_button()
        )
        
    except Exception as e:
        logger.error(f"Error en autenticación: {e}")
        await message.reply_text(
            f"❌ **Error de autenticación:** {str(e)}\n\nPor favor, verifica tus datos y usa /menu para reintentar.",
            reply_markup=get_back_to_main()
        )
        session_manager.clear_user_session(user_id)

async def process_verification_code(client, message: Message, user_session):
    """Procesar el código de verificación"""
    user_id = message.from_user.id
    
    try:
        # Verificar el código
        await user_session.temp_client.sign_in(
            phone_number=user_session.phone_number,
            phone_code_hash=user_session.phone_code_hash,
            phone_code=user_session.verification_code
        )
        
        # Generar sesión string
        session_string = await user_session.temp_client.export_session_string()
        await user_session.temp_client.disconnect()
        
        # Obtener información del usuario
        user_client = Client(
            name=f"user_{user_id}",
            api_id=user_session.api_id,
            api_hash=user_session.api_hash,
            session_string=session_string,
            in_memory=True
        )
        
        await user_client.start()
        me = await user_client.get_me()
        await user_client.stop()
        
        # Mostrar resultados
        result_text = f"""
✅ **¡Sesión Generada Exitosamente!**

**📋 Información de la Cuenta:**
👤 **Nombre:** {me.first_name or ''} {me.last_name or ''}
📱 **Teléfono:** {me.phone_number}
🆔 **User ID:** `{me.id}`
🔗 **Username:** @{me.username if me.username else 'No disponible'}

**🔐 Tu Sesión String:**
`{session_string}`

**⚠️ IMPORTANTE:**
• Guarda esta sesión en un lugar SEGURO
• NO la compartas con nadie
• Puedes usarla en Render como variable de entorno
        """
        
        await message.reply_text(
            result_text,
            reply_markup=get_back_to_main(),
            disable_web_page_preview=True
        )
        
        # Limpiar sesión
        session_manager.clear_user_session(user_id)
        
    except SessionPasswordNeeded:
        user_session.step = "waiting_password"
        await message.reply_text(
            """
🔒 **Verificación en Dos Pasos Activada**

Tu cuenta tiene **2FA (Two-Factor Authentication)** habilitada.

**Por favor, envía tu contraseña de verificación en dos pasos:**
            """,
            reply_markup=get_cancel_button()
        )
    
    except Exception as e:
        logger.error(f"Error en verificación: {e}")
        await message.reply_text(
            f"❌ **Error de verificación:** {str(e)}\n\nPor favor, verifica el código e intenta nuevamente con /menu.",
            reply_markup=get_back_to_main()
        )
        session_manager.clear_user_session(user_id)

async def process_two_factor(client, message: Message, user_session):
    """Procesar la contraseña 2FA"""
    user_id = message.from_user.id
    
    try:
        # Verificar con 2FA
        await user_session.temp_client.check_password(user_session.two_factor_password)
        
        # Generar sesión string
        session_string = await user_session.temp_client.export_session_string()
        await user_session.temp_client.disconnect()
        
        # Obtener información del usuario
        user_client = Client(
            name=f"user_{user_id}",
            api_id=user_session.api_id,
            api_hash=user_session.api_hash,
            session_string=session_string,
            in_memory=True
        )
        
        await user_client.start()
        me = await user_client.get_me()
        await user_client.stop()
        
        # Mostrar resultados
        result_text = f"""
✅ **¡Sesión Generada Exitosamente!**

**🔒 Cuenta con 2FA Protegida**

**📋 Información de la Cuenta:**
👤 **Nombre:** {me.first_name or ''} {me.last_name or ''}
📱 **Teléfono:** {me.phone_number}
🆔 **User ID:** `{me.id}`
🔗 **Username:** @{me.username if me.username else 'No disponible'}

**🔐 Tu Sesión String:**
`{session_string}`

**⚠️ IMPORTANTE:**
• Esta sesión INCLUYE protección 2FA
• Guardala en un lugar SEGURO
• NO la compartas con nadie
        """
        
        await message.reply_text(
            result_text,
            reply_markup=get_back_to_main(),
            disable_web_page_preview=True
        )
        
        # Limpiar sesión
        session_manager.clear_user_session(user_id)
        
    except Exception as e:
        logger.error(f"Error en 2FA: {e}")
        await message.reply_text(
            f"❌ **Error en verificación 2FA:** {str(e)}\n\nPor favor, verifica la contraseña e intenta nuevamente con /menu.",
            reply_markup=get_back_to_main()
        )
        session_manager.clear_user_session(user_id)

# ==================== MANEJADORES ADICIONALES ====================

@app.on_callback_query(filters.regex("^cancel_operation$"))
async def cancel_operation(client, callback_query):
    """Cancelar operación en curso"""
    user_id = callback_query.from_user.id
    session_manager.clear_user_session(user_id)
    
    await callback_query.edit_message_text(
        "❌ **Operación cancelada.**\nPuedes iniciar una nueva cuando lo desees.",
        reply_markup=get_back_to_main()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex("^main_menu$"))
async def main_menu_callback(client, callback_query):
    """Volver al menú principal"""
    await callback_query.edit_message_text(
        "**Panel de Control Principal**\nSelecciona una opción:",
        reply_markup=get_main_menu()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex("^my_info$"))
async def my_info_callback(client, callback_query):
    """Mostrar información del usuario"""
    user = callback_query.from_user
    info_text = f"""
👤 **Tu Información de Telegram:**

**🆔 ID:** `{user.id}`
**👤 Nombre:** {user.first_name}
**📝 Apellido:** {user.last_name or 'No disponible'}
**🔗 Username:** @{user.username if user.username else 'No disponible'}
**🤖 Es Bot:** {user.is_bot}
**⭐ Premium:** {getattr(user, 'is_premium', False)}

**💬 Idioma:** {user.language_code or 'No disponible'}
    """
    
    await callback_query.edit_message_text(
        info_text,
        reply_markup=get_back_to_main()
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex("^session_guide$"))
async def session_guide_callback(client, callback_query):
    """Mostrar guía detallada"""
    guide_text = """
📚 **Guía Completa: Generación de Sesiones**

**¿Qué es una Sesión String?**
Es una cadena de texto que permite autenticarte en Telegram sin necesidad de ingresar tu número y código cada vez.

**¿Para qué sirve?**
• 🤖 Crear bots de usuario
• 🔄 Automatizar tareas
• 📊 Monitorear cuentas
• 🚀 Desplegar en servicios como Render

**Proceso Seguro:**
1. Los datos se procesan en memoria
2. No se almacenan permanentemente
3. Solo tú ves la sesión generada
4. Proceso completamente encriptado

**Requisitos:**
• Cuenta en [my.telegram.org](https://my.telegram.org)
• API_ID y API_HASH
• Acceso a tu número telefónico
    """
    
    await callback_query.edit_message_text(
        guide_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Comenzar Generación", callback_data="start_session_generation")],
            [InlineKeyboardButton("🔙 Menú Principal", callback_data="main_menu")]
        ]),
        disable_web_page_preview=True
    )
    await callback_query.answer()

# ==================== INICIALIZACIÓN ====================

async def main():
    """Función principal de inicialización"""
    logger.info("🚀 Iniciando Sistema de Gestión de Sesiones...")
    
    await app.start()
    me = await app.get_me()
    
    logger.info(f"✅ Sistema iniciado como: {me.first_name} (@{me.username})")
    logger.info("📊 Session Manager inicializado correctamente")
    
    # Mantener la aplicación corriendo
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Validar configuración mínima
    if not API_ID or not API_HASH:
        logger.error("❌ Faltan API_ID o API_HASH en las variables de entorno")
        exit(1)
    
    if not BOT_TOKEN and not SESSION_STRING:
        logger.error("❌ Se requiere BOT_TOKEN o SESSION_STRING")
        exit(1)
    
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("⏹️  Sistema detenido por el usuario")
    except Exception as e:
        logger.error(f"💥 Error fatal: {e}")
        exit(1)