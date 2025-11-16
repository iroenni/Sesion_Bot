#!/usr/bin/env python3
"""
Sistema de gestión de sesiones para el bot de Telegram
Manejo seguro y eficiente del proceso de generación
"""

import time
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class UserSession:
    """Estructura para almacenar el estado de generación de sesión por usuario"""
    user_id: int
    step: str = "waiting_api_id"  # waiting_api_id, waiting_api_hash, waiting_phone, waiting_code, waiting_password, processing
    api_id: Optional[int] = None
    api_hash: Optional[str] = None
    phone_number: Optional[str] = None
    phone_code_hash: Optional[str] = None
    verification_code: Optional[str] = None
    two_factor_password: Optional[str] = None
    temp_client: Optional[object] = None
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class SessionManager:
    """
    Gestor profesional de sesiones de usuario
    """
    
    def __init__(self):
        self.user_sessions: Dict[int, UserSession] = {}
        self.session_timeout = 1800  # 30 minutos en segundos
    
    def init_user_session(self, user_id: int) -> UserSession:
        """
        Inicializar una nueva sesión para el usuario
        """
        session = UserSession(user_id=user_id)
        self.user_sessions[user_id] = session
        self._cleanup_expired_sessions()
        return session
    
    def get_user_session(self, user_id: int) -> Optional[UserSession]:
        """
        Obtener la sesión del usuario si existe y no ha expirado
        """
        session = self.user_sessions.get(user_id)
        
        if session and time.time() - session.created_at > self.session_timeout:
            # Sesión expirada
            self.clear_user_session(user_id)
            return None
        
        return session
    
    def update_user_session(self, user_id: int, **kwargs) -> bool:
        """
        Actualizar los datos de una sesión existente
        """
        session = self.get_user_session(user_id)
        if not session:
            return False
        
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        return True
    
    def clear_user_session(self, user_id: int) -> bool:
        """
        Limpiar la sesión del usuario
        """
        session = self.user_sessions.pop(user_id, None)
        
        # Limpiar cliente temporal si existe
        if session and session.temp_client:
            try:
                import asyncio
                asyncio.create_task(session.temp_client.disconnect())
            except:
                pass
        
        return session is not None
    
    def get_active_sessions_count(self) -> int:
        """
        Obtener número de sesiones activas
        """
        self._cleanup_expired_sessions()
        return len(self.user_sessions)
    
    def _cleanup_expired_sessions(self):
        """
        Limpiar sesiones expiradas
        """
        current_time = time.time()
        expired_users = [
            user_id for user_id, session in self.user_sessions.items()
            if current_time - session.created_at > self.session_timeout
        ]
        
        for user_id in expired_users:
            self.clear_user_session(user_id)
    
    def get_session_stats(self) -> dict:
        """
        Obtener estadísticas de las sesiones
        """
        self._cleanup_expired_sessions()
        
        stats = {
            'total_sessions': len(self.user_sessions),
            'sessions_by_step': {}
        }
        
        for session in self.user_sessions.values():
            stats['sessions_by_step'][session.step] = stats['sessions_by_step'].get(session.step, 0) + 1
        
        return stats