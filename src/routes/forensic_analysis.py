#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Forensic Analysis Routes
Rotas de análise forense corrigidas
"""

import logging
import time
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from services.ai_manager import ai_manager

logger = logging.getLogger(__name__)

forensic_bp = Blueprint('forensic_analysis', __name__)

@forensic_bp.route('/analyze', methods=['POST'])
def execute_forensic_analysis():
    """Executa análise forense"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        session_id = f"forensic_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        # Análise forense básica
        forensic_prompt = f"""
        Execute uma análise forense detalhada dos dados fornecidos:
        
        DADOS: {json.dumps(data, ensure_ascii=False)[:2000]}
        
        Analise:
        1. Padrões identificados
        2. Pontos críticos
        3. Oportunidades
        4. Riscos
        5. Recomendações
        
        Retorne análise estruturada.
        """
        
        analysis_result = ai_manager.generate_analysis(forensic_prompt)
        
        result = {
            'session_id': session_id,
            'forensic_analysis': analysis_result,
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "analysis": result,
            "message": "Análise forense concluída"
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erro na análise forense: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@forensic_bp.route('/health', methods=['GET'])
def forensic_health():
    """Verifica saúde do sistema forense"""
    try:
        return jsonify({
            'status': 'healthy',
            'ai_available': ai_manager.is_available(),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500