#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Aplicação Principal Aprimorada
Servidor Flask para análise de mercado ultra-detalhada
"""

import os
import sys
import time
import logging
from typing import Dict, List, Any, Optional
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Adiciona src ao path se necessário - VERSÃO ROBUSTA
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Adiciona também o diretório pai se necessário
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_app():
    """Cria e configura a aplicação Flask"""

    # Carrega variáveis de ambiente - IMPORTAÇÃO ROBUSTA
    try:
        from services.environment_loader import environment_loader
        logger.info("✅ Environment loader importado com sucesso")
    except ImportError as e:
        logger.error(f"❌ Erro ao importar environment_loader: {e}")
        logger.error(f"📁 Diretório atual: {os.getcwd()}")
        logger.error(f"🐍 Python path: {sys.path}")
        
        # Tenta importação alternativa
        try:
            sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
            from services.environment_loader import environment_loader
            logger.info("✅ Environment loader importado com path alternativo")
        except ImportError as e2:
            logger.critical(f"❌ Falha crítica na importação: {e2}")
            raise

    app = Flask(__name__)

    # CONFIGURAÇÃO CRÍTICA DE PRODUÇÃO
    # Força ambiente de produção - NUNCA debug em produção
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    debug = False  # SEMPRE False em produção
    app.config['DEBUG'] = debug
    app.config['TESTING'] = False

    # Configuração de logging para produção
    if FLASK_ENV == 'production':
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )
    else:
        logging.basicConfig(level=logging.DEBUG)

    # Configuração CORS para produção
    cors_origins = os.getenv('CORS_ORIGINS', '*')
    if FLASK_ENV == 'production' and cors_origins == '*':
        # Em produção, CORS deve ser restritivo
        cors_origins = ['https://yourdomain.com']  # Configurar domínio real

    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins.split(',') if isinstance(cors_origins, str) else cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Chave secreta segura carregada do ambiente
    app.secret_key = os.getenv('SECRET_KEY', 'arqv30-enhanced-ultra-secure-key-2024')
    if not os.getenv('SECRET_KEY') and FLASK_ENV == 'production':
        raise ValueError("SECRET_KEY deve ser definida em produção")

    # Registra blueprints
    from routes.analysis import analysis_bp
    from routes.enhanced_analysis import enhanced_analysis_bp
    from routes.forensic_analysis import forensic_bp
    from routes.files import files_bp
    from routes.progress import progress_bp
    from routes.user import user_bp
    from routes.monitoring import monitoring_bp
    from routes.pdf_generator import pdf_bp
    from routes.html_report_generator import html_report_bp
    from routes.mcp import mcp_bp
    from routes.session_management import session_bp

    app.register_blueprint(analysis_bp, url_prefix='/api')
    app.register_blueprint(enhanced_analysis_bp, url_prefix='/enhanced')
    app.register_blueprint(forensic_bp, url_prefix='/forensic')
    app.register_blueprint(files_bp, url_prefix='/files')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(monitoring_bp, url_prefix='/monitoring')
    app.register_blueprint(pdf_bp, url_prefix='/pdf')
    app.register_blueprint(html_report_bp, url_prefix='/html_report')
    app.register_blueprint(mcp_bp, url_prefix='/mcp')
    app.register_blueprint(session_bp, url_prefix='/api')

    @app.route('/')
    def index():
        """Página principal"""
        try:
            return render_template('enhanced_interface_v3.html')
        except Exception as e:
            logger.error(f"❌ Erro ao carregar template: {e}")
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ARQV30 Enhanced v3.0</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .container {{ max-width: 800px; margin: 0 auto; }}
                    .error {{ color: #d32f2f; background: #ffebee; padding: 20px; border-radius: 8px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>ARQV30 Enhanced v3.0</h1>
                    <div class="error">
                        <h3>Template não encontrado</h3>
                        <p>O template enhanced_interface_v3.html não foi encontrado.</p>
                        <p>Sistema funcionando em modo básico.</p>
                    </div>
                    <h2>API Endpoints Disponíveis:</h2>
                    <ul>
                        <li><a href="/api/app_status">/api/app_status</a> - Status da aplicação</li>
                        <li><a href="/monitoring/health">/monitoring/health</a> - Saúde do sistema</li>
                        <li><a href="/enhanced/execute_analysis">/enhanced/execute_analysis</a> - Análise aprimorada</li>
                    </ul>
                </div>
            </body>
            </html>
            """

    @app.route('/archaeological')
    def archaeological():
        """Interface arqueológica"""
        try:
            return render_template('enhanced_interface.html')
        except:
            return "Interface arqueológica não disponível"

    @app.route('/forensic')
    def forensic():
        """Interface forense"""
        try:
            return render_template('forensic_interface.html')
        except:
            return "Interface forense não disponível"

    @app.route('/unified')
    def unified():
        """Interface unificada"""
        try:
            return render_template('enhanced_interface_v3.html')
        except:
            return "Interface unificada não disponível"
    
    @app.route('/v3')
    def interface_v3():
        """Interface v3.0 aprimorada"""
        try:
            return render_template('enhanced_interface_v3.html')
        except:
            return "Interface v3.0 não disponível"

    @app.route('/api/app_status')
    def app_status():
        """Status da aplicação"""
        try:
            # Status dos serviços principais
            services_status = {
                'ai_manager': ai_manager.is_available(),
                'database': True,
                'file_system': True
            }

            # Verifica saúde dos componentes - tratamento seguro
            try:
                from services.health_checker import health_checker
                health_check = health_checker.get_overall_health()
            except Exception as health_error:
                health_check = {'status': 'error', 'message': str(health_error)}

            status = {
                'status': 'healthy',
                'services': services_status,
                'health': health_check,
                'timestamp': datetime.now().isoformat(),
                'version': 'ARQV30 Enhanced v3.0',
                'features': {
                    'ai_analysis': ai_manager.is_available(),
                    'data_collection': True,
                    'module_processing': True,
                    'report_generation': True
                }
            }

            return jsonify(status)

        except Exception as e:
            logger.error(f"Error in app_status: {e}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint não encontrado'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

    return app

def main():
    """Função principal"""

    print("🚀 ARQV30 Enhanced v3.0 - Iniciando aplicação...")

    try:
        # Cria aplicação
        app = create_app()

        # Configurações do servidor
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV', 'production') == 'development' # This line is kept for clarity in main, but app.config['DEBUG'] is set in create_app

        print(f"🌐 Servidor: http://{host}:{port}")
        print(f"🔧 Modo: {'Desenvolvimento' if debug else 'Produção'}")
        print(f"📊 Interface: Análise Ultra-Detalhada de Mercado")
        print(f"🤖 IA: Gemini + OpenAI + Groq")
        print(f"🔍 Pesquisa: Sistema de coleta de dados")
        print(f"💾 Banco: Supabase + Arquivos Locais")
        print(f"🛡️ Sistema: ARQV30 Enhanced v3.0")

        print("\n" + "=" * 60)
        print("✅ ARQV30 Enhanced v3.0 PRONTO!")
        print("=" * 60)
        print("Pressione Ctrl+C para parar o servidor")
        print("=" * 60)

        print("\n🔥 RECURSOS ATIVADOS:")
        print("- Sistema de IA Multi-Provedor")
        print("- Coleta de Dados Massiva")
        print("- Processamento de Módulos")
        print("- Geração de Relatórios")
        print("- Sistema de Monitoramento")
        print("- Persistência de Sessões")

        # Inicia servidor
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )

    except KeyboardInterrupt:
        print("\n\n✅ Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        logger.critical(f"Critical error during server startup: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
