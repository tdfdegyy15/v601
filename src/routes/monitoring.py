#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Monitoring Routes
Rotas de monitoramento do sistema
"""

import logging
import psutil
from datetime import datetime
from flask import Blueprint, jsonify
from services.health_checker import health_checker

logger = logging.getLogger(__name__)

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/health', methods=['GET'])
def system_health():
    """Verifica saúde geral do sistema"""
    try:
        health_status = health_checker.get_overall_health()
        return jsonify(health_status), 200
        
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/metrics', methods=['GET'])
def system_metrics():
    """Retorna métricas do sistema"""
    try:
        # Métricas básicas do sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': round(memory.available / (1024**3), 2),
                'disk_percent': disk.percent,
                'disk_free_gb': round(disk.free / (1024**3), 2)
            },
            'application': {
                'status': 'running',
                'uptime': 'N/A'  # Seria calculado em produção
            }
        }
        
        return jsonify(metrics), 200
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter métricas: {e}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@monitoring_bp.route('/status', methods=['GET'])
def service_status():
    """Status dos serviços"""
    try:
        from services.ai_manager import ai_manager
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'services': {
                'ai_manager': {
                    'status': 'healthy' if ai_manager.is_available() else 'unhealthy',
                    'providers': ai_manager.get_status()
                },
                'database': {
                    'status': 'healthy',
                    'type': 'local_files'
                },
                'file_system': {
                    'status': 'healthy'
                }
            }
        }
        
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f"❌ Erro no status: {e}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500