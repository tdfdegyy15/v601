#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - PDF Generator Routes
Rotas para geração de PDFs
"""

import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
import os
from pathlib import Path

logger = logging.getLogger(__name__)

pdf_bp = Blueprint('pdf_generator', __name__)

@pdf_bp.route('/generate/<session_id>', methods=['POST'])
def generate_pdf_report(session_id):
    """Gera relatório PDF"""
    try:
        # Verifica se existe relatório da sessão
        session_dir = Path(f"analyses_data/{session_id}")
        report_file = session_dir / "relatorio_coleta.md"
        
        if not report_file.exists():
            return jsonify({
                'success': False,
                'error': 'Relatório não encontrado'
            }), 404
        
        # Lê conteúdo do relatório
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simula geração de PDF (em produção usaria reportlab ou weasyprint)
        pdf_path = session_dir / "relatorio.pdf"
        
        # Cria arquivo PDF simples (placeholder)
        with open(pdf_path, 'w', encoding='utf-8') as f:
            f.write(f"PDF Report for session {session_id}\n\n{content}")
        
        return jsonify({
            'success': True,
            'pdf_path': str(pdf_path),
            'session_id': session_id,
            'generated_at': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar PDF: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@pdf_bp.route('/download/<session_id>', methods=['GET'])
def download_pdf(session_id):
    """Download do PDF gerado"""
    try:
        pdf_path = Path(f"analyses_data/{session_id}/relatorio.pdf")
        
        if not pdf_path.exists():
            return jsonify({
                'error': 'PDF não encontrado'
            }), 404
        
        return send_file(
            str(pdf_path),
            as_attachment=True,
            download_name=f"relatorio_{session_id}.pdf"
        )
        
    except Exception as e:
        logger.error(f"❌ Erro no download: {e}")
        return jsonify({
            'error': str(e)
        }), 500