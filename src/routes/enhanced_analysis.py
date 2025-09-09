#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced Analysis Routes
Rotas de análise aprimoradas e corrigidas
"""

import logging
import time
import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from services.ai_manager import ai_manager
from services.massive_data_collector import massive_data_collector
from services.auto_save_manager import salvar_etapa

logger = logging.getLogger(__name__)

enhanced_analysis_bp = Blueprint('enhanced_analysis', __name__)

@enhanced_analysis_bp.route('/execute_analysis', methods=['POST'])
def execute_enhanced_analysis():
    """Executa análise aprimorada"""
    try:
        # Recebe dados da requisição
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados da requisição são obrigatórios"}), 400
        
        # Gera session_id único
        session_id = f"session_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"
        
        # Extrai parâmetros
        segmento = data.get('segmento', '').strip()
        produto = data.get('produto', '').strip()
        publico = data.get('publico', '').strip()
        
        # Validação básica
        if not segmento:
            return jsonify({"error": "Segmento é obrigatório"}), 400
        
        logger.info(f"🚀 Iniciando análise aprimorada - Sessão: {session_id}")
        
        # ETAPA 1: Coleta de dados
        logger.info("📊 ETAPA 1: Coleta de dados")
        collection_result = massive_data_collector.collect_comprehensive_data(
            produto=produto,
            nicho=segmento,
            publico=publico,
            session_id=session_id
        )
        
        # ETAPA 2: Análise com IA
        logger.info("🤖 ETAPA 2: Análise com IA")
        analysis_prompt = f"""
        Analise os dados coletados para o segmento {segmento}.
        
        DADOS COLETADOS:
        - Produto: {produto}
        - Público: {publico}
        - Fontes analisadas: {collection_result['statistics']['total_sources']}
        
        Crie uma análise estruturada com:
        1. Insights principais do mercado
        2. Oportunidades identificadas
        3. Público-alvo refinado
        4. Estratégias recomendadas
        5. Pontos de atenção
        
        Retorne em formato JSON estruturado.
        """
        
        ai_analysis = ai_manager.generate_analysis(analysis_prompt, max_tokens=4000)
        
        # ETAPA 3: Compilação final
        logger.info("📋 ETAPA 3: Compilação final")
        final_result = {
            'session_id': session_id,
            'collection_data': collection_result,
            'ai_analysis': ai_analysis,
            'execution_summary': {
                'total_sources': collection_result['statistics']['total_sources'],
                'collection_time': collection_result['statistics']['collection_time'],
                'analysis_completed': True
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Salva resultado final
        salvar_etapa("analise_aprimorada_final", final_result, categoria="analise_completa", session_id=session_id)
        
        logger.info(f"✅ Análise aprimorada concluída: {session_id}")
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Análise aprimorada concluída com sucesso",
            "execution_summary": final_result['execution_summary'],
            "data_quality": "REAL_DATA_COLLECTED",
            "access_info": {
                "session_directory": f"analyses_data/{session_id}",
                "report_available": True
            }
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erro na análise aprimorada: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Erro interno do servidor"
        }), 500

@enhanced_analysis_bp.route('/status/<session_id>', methods=['GET'])
def get_analysis_status(session_id):
    """Obtém status da análise"""
    try:
        # Verifica se existe diretório da sessão
        import os
        session_dir = f"analyses_data/{session_id}"
        
        if os.path.exists(session_dir):
            # Lista arquivos da sessão
            files = os.listdir(session_dir)
            
            return jsonify({
                'session_id': session_id,
                'status': 'completed' if 'relatorio_coleta.md' in files else 'in_progress',
                'files_available': len(files),
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'session_id': session_id,
                'status': 'not_found',
                'message': 'Sessão não encontrada'
            }), 404
            
    except Exception as e:
        logger.error(f"❌ Erro ao obter status: {e}")
        return jsonify({
            'session_id': session_id,
            'error': str(e),
            'status': 'error'
        }), 500