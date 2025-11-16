#!/usr/bin/env python3
"""
Bot de Telegram con menús de navegación y botones
Desplegable en Render
"""

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    Message
)
from pyrogram.errors import BadRequest
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración desde variables de entorno
API_ID = int(os.getenv("API_ID", 14681595))
API_HASH = os.getenv("API_HASH", "a86730aab5c59953c424abb4396d32d5")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Inicializar cliente
if BOT_TOKEN:
    app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
elif SESSION_STRING:
    app = Client("my_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
else:
    raise ValueError("Se requiere BOT_TOKEN o SESSION_STRING")

# ==================== DEFINICIÓN DE MENÚS ====================

def get_main_menu():
    """Menú principal con botones inline"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Información", callback_data="menu_info"),
            InlineKeyboardButton("⚙️ Configuración", callback_data="menu_config")
        ],
        [
            InlineKeyboardButton("🔧 Herramientas", callback_data="menu_tools"),
            InlineKeyboardButton("❓ Ayuda", callback_data="menu_help")
        ],
        [
            InlineKeyboardButton("🌐 Sitio Web", url="https://docs.pyrogram.org"),
            InlineKeyboardButton("⭐ Calificar", callback_data="menu_rating")
        ]
    ])
    return keyboard

def get_info_menu():
    """Submenú de información"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 Mi Info", callback_data="info_my"),
            InlineKeyboardButton("🤖 Bot Info", callback_data="info_bot")
        ],
        [
            InlineKeyboardButton("📊 Estadísticas", callback_data="info_stats"),
            InlineKeyboardButton("🔙 Volver", callback_data="menu_main")
        ]
    ])
    return keyboard

def get_config_menu():
    """Submenú de configuración"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌐 Idioma", callback_data="config_lang"),
            InlineKeyboardButton("🔔 Notificaciones", callback_data="config_notify")
        ],
        [
            InlineKeyboardButton("🎨 Tema", callback_data="config_theme"),
            InlineKeyboardButton("🔙 Volver", callback_data="menu_main")
        ]
    ])
    return keyboard

def get_tools_menu():
    """Submenú de herramientas"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Generar Sesión", callback_data="tools_session"),
            InlineKeyboardButton("📁 Archivos", callback_data="tools_files")
        ],
        [
            InlineKeyboardButton("🔍 Buscar", callback_data="tools_search"),
            InlineKeyboardButton("🔙 Volver", callback_data="menu_main")
        ]
    ])
    return keyboard

def get_rating_menu():
    """Menú de calificación"""
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⭐", callback_data="rate_1"),
            InlineKeyboardButton("⭐⭐", callback_data="rate_2"),
            InlineKeyboardButton("⭐⭐⭐", callback_data="rate_3")
        ],
        [
            InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rate_4"),
            InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rate_5")
        ],
        [
            InlineKeyboardButton("🔙 Volver", callback_data="menu_main")
        ]
    ])
    return keyboard

def get_back_button():
    """Botón simple para volver al menú principal"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Volver al Inicio", callback_data="menu_main")]
    ])

# ==================== MANEJADORES DE COMANDOS ====================

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    """Comando /start - Menú principal"""
    welcome_text = """
🤖 **Bienvenido al Bot de Telegram**

¡Hola! Soy un bot creado con Pyrogram que ofrece:

• 📊 **Menús interactivos** con navegación completa
• ⚙️ **Sistema de configuración** modular
• 🔧 **Herramientas útiles** incluido generador de sesiones
• 🌐 **Navegación fluida** entre diferentes secciones

Selecciona una opción del menú para comenzar:
    """
    
    await message.reply_text(
        welcome_text,
        reply_markup=get_main_menu(),
        disable_web_page_preview=True
    )

@app.on_message(filters.command("menu") & filters.private)
async def menu_command(client, message: Message):
    """Comando /menu - Mostrar menú principal"""
    await message.reply_text(
        "🎯 **Menú Principal**\nSelecciona una opción:",
        reply_markup=get_main_menu()
    )

@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message: Message):
    """Comando /help - Mostrar ayuda"""
    help_text = """
🆘 **Guía de Ayuda**

**Comandos disponibles:**
/start - Iniciar el bot y mostrar menú principal
/menu - Mostrar menú de navegación
/help - Mostrar esta ayuda
/session - Generar una nueva sesión string

**Características:**
• Navegación completa con menús interactivos
• Generación segura de sesiones string
• Interfaz amigable con botones
• Compatible con despliegue en Render

Si necesitas ayuda específica, usa los botones del menú ❓ Ayuda.
    """
    
    await message.reply_text(
        help_text,
        reply_markup=get_back_button(),
        disable_web_page_preview=True
    )

# ==================== MANEJADORES DE CALLBACKS ====================

@app.on_callback_query()
async def handle_callbacks(client, callback_query):
    """Manejar todos los callbacks de los botones"""
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.id
    
    try:
        # Navegación principal
        if data == "menu_main":
            await client.edit_message_text(
                chat_id, message_id,
                "🎯 **Menú Principal**\nSelecciona una opción:",
                reply_markup=get_main_menu()
            )
        
        elif data == "menu_info":
            await client.edit_message_text(
                chat_id, message_id,
                "📊 **Menú de Información**\n¿Qué información deseas ver?",
                reply_markup=get_info_menu()
            )
        
        elif data == "menu_config":
            await client.edit_message_text(
                chat_id, message_id,
                "⚙️ **Menú de Configuración**\nConfigura tus preferencias:",
                reply_markup=get_config_menu()
            )
        
        elif data == "menu_tools":
            await client.edit_message_text(
                chat_id, message_id,
                "🔧 **Menú de Herramientas**\nSelecciona una herramienta:",
                reply_markup=get_tools_menu()
            )
        
        elif data == "menu_help":
            help_text = """
❓ **Centro de Ayuda**

**Problemas comunes:**
• ¿Problemas con sesiones? Usa la herramienta Generar Sesión
• ¿No responden los botones? Prueba /menu para refrescar
• ¿Error de conexión? Verifica tu internet

**Soporte:**
Para asistencia técnica, contacta al desarrollador o revisa la documentación oficial.
            """
            await client.edit_message_text(
                chat_id, message_id,
                help_text,
                reply_markup=get_back_button()
            )
        
        elif data == "menu_rating":
            await client.edit_message_text(
                chat_id, message_id,
                "⭐ **Sistema de Calificación**\n¿Cómo calificarías este bot?",
                reply_markup=get_rating_menu()
            )
        
        # Submenús de información
        elif data == "info_my":
            user = callback_query.from_user
            user_info = f"""
👤 **Tu Información:**

**ID:** `{user.id}`
**Nombre:** {user.first_name}
**Username:** @{user.username if user.username else "No disponible"}
**Es bot:** {user.is_bot}
            """
            await client.edit_message_text(
                chat_id, message_id,
                user_info,
                reply_markup=get_info_menu()
            )
        
        elif data == "info_bot":
            me = await client.get_me()
            bot_info = f"""
🤖 **Información del Bot:**

**ID:** `{me.id}`
**Nombre:** {me.first_name}
**Username:** @{me.username}
**Premium:** {getattr(me, 'is_premium', False)}
            """
            await client.edit_message_text(
                chat_id, message_id,
                bot_info,
                reply_markup=get_info_menu()
            )
        
        # Herramientas
        elif data == "tools_session":
            session_info = """
🔄 **Generador de Sesiones**

Para generar una sesión string segura, necesitas:

1. **API_ID** y **API_HASH** de [my.telegram.org](https://my.telegram.org)
2. Tu número de teléfono con código de país
3. Código de verificación que recibirás por Telegram

**Usa el comando:** `/session` para iniciar el proceso de generación.

⚠️ **Importante:** La sesión string da acceso completo a tu cuenta. ¡Guárdala de forma segura!
            """
            await client.edit_message_text(
                chat_id, message_id,
                session_info,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Generar Sesión", callback_data="tools_generate_session")],
                    [InlineKeyboardButton("🔙 Volver", callback_data="menu_tools")]
                ]),
                disable_web_page_preview=True
            )
        
        elif data == "tools_generate_session":
            await client.edit_message_text(
                chat_id, message_id,
                "🔄 **Generar Sesión**\n\nPor favor, usa el comando `/session` en este chat para generar una nueva sesión string de forma segura.",
                reply_markup=get_back_button()
            )
        
        # Sistema de calificación
        elif data.startswith("rate_"):
            rating = data.split("_")[1]
            stars = "⭐" * int(rating)
            await client.edit_message_text(
                chat_id, message_id,
                f"✅ **¡Gracias por tu calificación!**\n\nHas calificado con: {stars}\n\nTu feedback es muy importante para mejorar el bot.",
                reply_markup=get_back_button()
            )
        
        # Configuración
        elif data == "config_lang":
            await client.edit_message_text(
                chat_id, message_id,
                "🌐 **Selección de Idioma**\n\nIdiomas disponibles:\n• Español\n• English\n• Português\n\n*Funcionalidad en desarrollo*",
                reply_markup=get_config_menu()
            )
        
        else:
            await client.answer_callback_query(
                callback_query.id,
                "⚠️ Función en desarrollo",
                show_alert=False
            )
    
    except BadRequest as e:
        # Ignorar error de mismo contenido
        if "MESSAGE_NOT_MODIFIED" not in str(e):
            logger.error(f"Error editing message: {e}")
    except Exception as e:
        logger.error(f"Error in callback: {e}")
        await client.answer_callback_query(
            callback_query.id,
            "❌ Error al procesar la solicitud",
            show_alert=False
        )
    
    # Confirmar que se recibió el callback
    await client.answer_callback_query(callback_query.id)

# ==================== COMANDO DE GENERACIÓN DE SESIÓN ====================

@app.on_message(filters.command("session") & filters.private)
async def session_command(client, message: Message):
    """Comando para generar sesión string"""
    session_info = """
🔐 **Generación de Sesión String**

Para generar una sesión string, necesitas ejecutar el script de generación por separado.

**Instrucciones:**

1. Descarga el archivo `session_generator.py`
2. Ejecuta: `python session_generator.py`
3. Sigue las instrucciones en pantalla
4. Guarda tu sesión string de forma segura

**Para usar en Render:** Agrega estas variables de entorno:
- `API_ID`: Tu API ID de Telegram
- `API_HASH`: Tu API Hash de Telegram  
- `SESSION_STRING`: La sesión string generada

⚠️ **Advertencia de seguridad:** Nunca compartas tu sesión string con nadie.
    """
    
    await message.reply_text(
        session_info,
        reply_markup=get_back_button(),
        disable_web_page_preview=True
    )

# ==================== INICIALIZACIÓN ====================

async def main():
    """Función principal"""
    logger.info("Iniciando bot de Telegram...")
    await app.start()
    
    me = await app.get_me()
    logger.info(f"Bot iniciado como: {me.first_name} (@{me.username})")
    
    # Mantener el bot corriendo
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Verificar configuración mínima
    if not API_ID or not API_HASH:
        logger.error("Faltan API_ID o API_HASH en las variables de entorno")
        exit(1)
    
    if not BOT_TOKEN and not SESSION_STRING:
        logger.error("Se requiere BOT_TOKEN o SESSION_STRING")
        exit(1)
    
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}")