#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Health Checker
Verificador de saúde do sistema
"""

import os
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class HealthChecker:
    """Verificador de saúde do sistema"""

    def __init__(self):
        """Inicializa o verificador"""
        self.components = [
            'ai_manager',
            'database',
            'file_system',
            'environment'
        ]
        
        logger.info("🏥 Health Checker inicializado")

    def get_overall_health(self) -> Dict[str, Any]:
        """Retorna saúde geral do sistema"""
        
        health_status = {
            'overall_status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {},
            'issues': [],
            'recommendations': []
        }

        try:
            # Verifica AI Manager
            health_status['components']['ai_manager'] = self._check_ai_manager()
            
            # Verifica Database
            health_status['components']['database'] = self._check_database()
            
            # Verifica File System
            health_status['components']['file_system'] = self._check_file_system()
            
            # Verifica Environment
            health_status['components']['environment'] = self._check_environment()
            
            # Determina status geral
            unhealthy_components = [
                name for name, status in health_status['components'].items()
                if status['status'] != 'healthy'
            ]
            
            if unhealthy_components:
                health_status['overall_status'] = 'degraded'
                health_status['issues'] = [
                    f"Componente {comp} com problemas" for comp in unhealthy_components
                ]
            
            return health_status
            
        except Exception as e:
            logger.error(f"❌ Erro no health check: {e}")
            return {
                'overall_status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _check_ai_manager(self) -> Dict[str, Any]:
        """Verifica saúde do AI Manager"""
        try:
            from services.ai_manager import ai_manager
            
            if ai_manager.is_available():
                return {
                    'status': 'healthy',
                    'providers_available': len([p for p in ai_manager.providers.values() if p['available']]),
                    'total_providers': len(ai_manager.providers)
                }
            else:
                return {
                    'status': 'unhealthy',
                    'issue': 'Nenhum provedor de IA disponível'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _check_database(self) -> Dict[str, Any]:
        """Verifica saúde do banco de dados"""
        try:
            from database import db_manager
            
            if db_manager.test_connection():
                return {
                    'status': 'healthy',
                    'type': 'local_files'
                }
            else:
                return {
                    'status': 'unhealthy',
                    'issue': 'Conexão com banco falhou'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _check_file_system(self) -> Dict[str, Any]:
        """Verifica saúde do sistema de arquivos"""
        try:
            # Verifica diretórios essenciais
            required_dirs = [
                'analyses_data',
                'relatorios_intermediarios',
                'src/static',
                'src/templates'
            ]
            
            missing_dirs = []
            for dir_path in required_dirs:
                if not os.path.exists(dir_path):
                    missing_dirs.append(dir_path)
            
            if missing_dirs:
                return {
                    'status': 'unhealthy',
                    'issue': f'Diretórios ausentes: {", ".join(missing_dirs)}'
                }
            
            return {
                'status': 'healthy',
                'directories_checked': len(required_dirs)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def _check_environment(self) -> Dict[str, Any]:
        """Verifica variáveis de ambiente"""
        try:
            required_vars = ['GEMINI_API_KEY', 'SUPABASE_URL', 'SUPABASE_ANON_KEY']
            missing_vars = []
            
            for var in required_vars:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            if missing_vars:
                return {
                    'status': 'degraded',
                    'issue': f'Variáveis ausentes: {", ".join(missing_vars)}'
                }
            
            return {
                'status': 'healthy',
                'variables_checked': len(required_vars)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# Instância global
health_checker = HealthChecker()