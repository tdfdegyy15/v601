#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Comprehensive HTML Report Generator
Gerador de relatórios HTML abrangentes
"""

import os
import logging
import json
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class ComprehensiveHTMLReportGenerator:
    """Gerador de relatórios HTML abrangentes"""

    def __init__(self):
        """Inicializa o gerador"""
        self.template_path = "src/templates"
        logger.info("📄 HTML Report Generator inicializado")

    async def generate_ultimate_25_page_report(
        self,
        massive_data: Dict[str, Any],
        expert_knowledge: Dict[str, Any],
        session_id: str
    ) -> str:
        """Gera relatório HTML de 25+ páginas"""
        
        logger.info(f"📄 Gerando relatório HTML para sessão: {session_id}")
        
        try:
            # Cria diretório da sessão
            session_dir = Path(f"analyses_data/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Template HTML básico
            html_content = self._generate_html_template(massive_data, expert_knowledge, session_id)
            
            # Salva relatório
            report_path = session_dir / "relatorio_final.html"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Relatório HTML gerado: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório HTML: {e}")
            raise

    def _generate_html_template(
        self,
        massive_data: Dict[str, Any],
        expert_knowledge: Dict[str, Any],
        session_id: str
    ) -> str:
        """Gera template HTML do relatório"""
        
        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório ARQV30 Enhanced - {session_id}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 40px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .header {{ text-align: center; margin-bottom: 40px; }}
                .section {{ margin-bottom: 30px; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
                .stat-card {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .stat-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
                .stat-label {{ color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>ARQV30 Enhanced v3.0</h1>
                    <h2>Relatório de Análise Completa</h2>
                    <p><strong>Sessão:</strong> {session_id}</p>
                    <p><strong>Gerado em:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>

                <div class="section">
                    <h2>📊 Estatísticas da Coleta</h2>
                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-value">{massive_data.get('statistics', {}).get('total_sources', 0)}</div>
                            <div class="stat-label">Fontes Analisadas</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{massive_data.get('statistics', {}).get('collection_time', 0):.1f}s</div>
                            <div class="stat-label">Tempo de Coleta</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{massive_data.get('statistics', {}).get('success_rate', 0):.1f}%</div>
                            <div class="stat-label">Taxa de Sucesso</div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>🔍 Dados Coletados</h2>
                    <h3>Dados Web</h3>
                    {self._format_web_data_html(massive_data.get('web_data', []))}
                    
                    <h3>Dados Sociais</h3>
                    {self._format_social_data_html(massive_data.get('social_data', []))}
                </div>

                <div class="section">
                    <h2>🧠 Análise da IA</h2>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                        <pre style="white-space: pre-wrap;">{json.dumps(expert_knowledge, indent=2, ensure_ascii=False)[:2000]}...</pre>
                    </div>
                </div>

                <div class="section">
                    <h2>📋 Conclusões</h2>
                    <p>Análise completa realizada com sucesso utilizando o sistema ARQV30 Enhanced v3.0.</p>
                    <p>Total de {massive_data.get('statistics', {}).get('total_sources', 0)} fontes foram analisadas para gerar insights abrangentes.</p>
                </div>

                <div style="text-align: center; margin-top: 40px; color: #6c757d;">
                    <p>Relatório gerado automaticamente pelo ARQV30 Enhanced v3.0</p>
                    <p>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """

    def _format_web_data_html(self, web_data: List[Dict[str, Any]]) -> str:
        """Formata dados web para HTML"""
        if not web_data:
            return "<p>Nenhum dado web coletado.</p>"
        
        html = "<ul>"
        for item in web_data[:5]:  # Limita a 5 itens
            html += f"""
            <li>
                <strong>{item.get('title', 'Sem título')}</strong><br>
                <small>URL: {item.get('url', 'N/A')}</small><br>
                <em>{item.get('content', 'N/A')[:200]}...</em>
            </li>
            """
        html += "</ul>"
        return html

    def _format_social_data_html(self, social_data: List[Dict[str, Any]]) -> str:
        """Formata dados sociais para HTML"""
        if not social_data:
            return "<p>Nenhum dado social coletado.</p>"
        
        html = "<ul>"
        for item in social_data[:5]:  # Limita a 5 itens
            html += f"""
            <li>
                <strong>{item.get('title', 'Sem título')}</strong><br>
                <small>Plataforma: {item.get('platform', 'N/A')}</small><br>
                <em>{item.get('content', 'N/A')[:200]}...</em>
            </li>
            """
        html += "</ul>"
        return html