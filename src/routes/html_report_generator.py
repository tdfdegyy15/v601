#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - HTML Report Generator Routes
Rotas para geração de relatórios HTML
"""

import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template_string
from pathlib import Path

logger = logging.getLogger(__name__)

html_report_bp = Blueprint('html_report_generator', __name__)

@html_report_bp.route('/generate/<session_id>', methods=['POST'])
def generate_html_report(session_id):
    """Gera relatório HTML"""
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
        
        # Template HTML básico
        html_template = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório ARQV30 - {{ session_id }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1, h2, h3 { color: #333; }
                .header { border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }
                .content { white-space: pre-wrap; }
                .footer { margin-top: 50px; padding-top: 20px; border-top: 1px solid #ccc; color: #666; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>ARQV30 Enhanced v3.0 - Relatório de Análise</h1>
                <p><strong>Sessão:</strong> {{ session_id }}</p>
                <p><strong>Gerado em:</strong> {{ timestamp }}</p>
            </div>
            <div class="content">{{ content }}</div>
            <div class="footer">
                <p>Relatório gerado automaticamente pelo ARQV30 Enhanced v3.0</p>
            </div>
        </body>
        </html>
        """
        
        # Renderiza HTML
        html_content = render_template_string(
            html_template,
            session_id=session_id,
            content=content,
            timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        )
        
        # Salva arquivo HTML
        html_path = session_dir / "relatorio.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return jsonify({
            'success': True,
            'html_path': str(html_path),
            'session_id': session_id,
            'generated_at': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erro ao gerar HTML: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500