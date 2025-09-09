#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced Module Processor
Processador de módulos aprimorado e corrigido
"""

import os
import logging
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
from services.ai_manager import ai_manager

logger = logging.getLogger(__name__)

class EnhancedModuleProcessor:
    """Processador de módulos aprimorado"""

    def __init__(self):
        """Inicializa o processador"""
        self.modules = [
            'avatars',
            'drivers_mentais',
            'anti_objecao',
            'provas_visuais',
            'pre_pitch',
            'predicoes_futuro',
            'posicionamento',
            'concorrencia',
            'palavras_chave',
            'funil_vendas',
            'insights_mercado',
            'plano_acao',
            'metricas_conversao',
            'estrategia_preco',
            'canais_aquisicao',
            'cronograma_lancamento'
        ]
        
        logger.info("🔧 Enhanced Module Processor inicializado")

    async def generate_all_modules(self, session_id: str) -> Dict[str, Any]:
        """Gera todos os módulos para uma sessão"""
        
        logger.info(f"🔧 Gerando módulos para sessão: {session_id}")
        
        processing_result = {
            'session_id': session_id,
            'processing_started': datetime.now().isoformat(),
            'modules_processed': [],
            'modules_failed': [],
            'processing_summary': {
                'total_modules': len(self.modules),
                'successful_modules': 0,
                'failed_modules': 0,
                'success_rate': 0.0
            }
        }

        try:
            # Carrega dados da sessão
            session_data = await self._load_session_data(session_id)
            
            # Cria diretório de módulos
            modules_dir = Path(f"analyses_data/{session_id}/modules")
            modules_dir.mkdir(parents=True, exist_ok=True)
            
            # Processa cada módulo
            for module_name in self.modules:
                try:
                    logger.info(f"🔧 Processando módulo: {module_name}")
                    
                    module_content = await self._generate_module(module_name, session_data, session_id)
                    
                    if module_content:
                        # Salva módulo
                        module_file = modules_dir / f"{module_name}.md"
                        with open(module_file, 'w', encoding='utf-8') as f:
                            f.write(module_content)
                        
                        processing_result['modules_processed'].append({
                            'name': module_name,
                            'file': str(module_file),
                            'size': len(module_content),
                            'generated_at': datetime.now().isoformat()
                        })
                        
                        processing_result['processing_summary']['successful_modules'] += 1
                        logger.info(f"✅ Módulo {module_name} gerado")
                    else:
                        raise Exception("Conteúdo vazio gerado")
                        
                except Exception as e:
                    logger.error(f"❌ Erro no módulo {module_name}: {e}")
                    processing_result['modules_failed'].append({
                        'name': module_name,
                        'error': str(e),
                        'failed_at': datetime.now().isoformat()
                    })
                    processing_result['processing_summary']['failed_modules'] += 1
            
            # Calcula taxa de sucesso
            total = processing_result['processing_summary']['total_modules']
            successful = processing_result['processing_summary']['successful_modules']
            processing_result['processing_summary']['success_rate'] = (successful / total) * 100 if total > 0 else 0
            
            logger.info(f"✅ Processamento concluído: {successful}/{total} módulos")
            return processing_result
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento de módulos: {e}")
            processing_result['processing_summary']['failed_modules'] = len(self.modules)
            return processing_result

    async def _load_session_data(self, session_id: str) -> Dict[str, Any]:
        """Carrega dados da sessão"""
        try:
            session_dir = Path(f"analyses_data/{session_id}")
            
            # Tenta carregar dados coletados
            data_file = session_dir / "dados_coletados.json"
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # Fallback para dados básicos
            return {
                'session_id': session_id,
                'context': {
                    'produto': 'Produto não especificado',
                    'nicho': 'Nicho não especificado',
                    'publico': 'Público não especificado'
                },
                'web_data': [],
                'social_data': []
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar dados da sessão: {e}")
            return {'session_id': session_id, 'context': {}}

    async def _generate_module(self, module_name: str, session_data: Dict[str, Any], session_id: str) -> str:
        """Gera conteúdo de um módulo específico"""
        
        try:
            context = session_data.get('context', {})
            produto = context.get('produto', 'Produto')
            nicho = context.get('nicho', 'Nicho')
            publico = context.get('publico', 'Público')
            
            # Prompts específicos por módulo
            module_prompts = {
                'avatars': f"""
                Crie um avatar detalhado para o público-alvo de {produto} no nicho {nicho}.
                
                Inclua:
                - Demografia detalhada
                - Psicografia
                - Dores e necessidades
                - Comportamentos de compra
                - Canais de comunicação preferidos
                
                Formato: Markdown estruturado
                """,
                
                'drivers_mentais': f"""
                Desenvolva 5 drivers mentais específicos para {produto} direcionado a {publico}.
                
                Para cada driver:
                - Nome impactante
                - Gatilho psicológico
                - Script de ativação
                - Momento ideal de uso
                
                Formato: Markdown estruturado
                """,
                
                'anti_objecao': f"""
                Crie um sistema anti-objeção para {produto} no nicho {nicho}.
                
                Inclua:
                - 10 principais objeções esperadas
                - Resposta para cada objeção
                - Scripts de neutralização
                - Técnicas de reframe
                
                Formato: Markdown estruturado
                """,
                
                'concorrencia': f"""
                Analise a concorrência para {produto} no mercado de {nicho}.
                
                Inclua:
                - Principais concorrentes
                - Análise SWOT
                - Oportunidades de diferenciação
                - Estratégias competitivas
                
                Formato: Markdown estruturado
                """,
                
                'funil_vendas': f"""
                Desenvolva um funil de vendas para {produto} direcionado a {publico}.
                
                Inclua:
                - Etapas do funil
                - Conteúdo para cada etapa
                - Métricas de conversão
                - Pontos de otimização
                
                Formato: Markdown estruturado
                """
            }
            
            # Prompt padrão para módulos não especificados
            default_prompt = f"""
            Crie conteúdo detalhado para o módulo {module_name} relacionado a {produto} no nicho {nicho} para o público {publico}.
            
            Seja específico, prático e acionável.
            
            Formato: Markdown estruturado
            """
            
            prompt = module_prompts.get(module_name, default_prompt)
            
            # Gera conteúdo usando IA
            content = ai_manager.generate_analysis(prompt, max_tokens=3000)
            
            if not content or len(content) < 100:
                # Fallback para conteúdo básico
                content = self._generate_fallback_module(module_name, context)
            
            return content
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar módulo {module_name}: {e}")
            return self._generate_fallback_module(module_name, session_data.get('context', {}))

    def _generate_fallback_module(self, module_name: str, context: Dict[str, Any]) -> str:
        """Gera conteúdo de fallback para um módulo"""
        
        produto = context.get('produto', 'Produto')
        nicho = context.get('nicho', 'Nicho')
        publico = context.get('publico', 'Público')
        
        return f"""# {module_name.replace('_', ' ').title()}

## Análise para {produto}

**Nicho:** {nicho}  
**Público-alvo:** {publico}  
**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

### Resumo

Este módulo foi gerado automaticamente para {produto} no nicho {nicho}.

### Principais Pontos

1. **Análise específica** para o segmento {nicho}
2. **Foco no público** {publico}
3. **Estratégias personalizadas** para {produto}
4. **Implementação prática** baseada em dados coletados

### Recomendações

- Implementar estratégias específicas para {nicho}
- Focar nas necessidades de {publico}
- Monitorar métricas relevantes
- Ajustar abordagem conforme resultados

### Próximos Passos

1. Revisar análise detalhada
2. Implementar recomendações
3. Monitorar resultados
4. Otimizar baseado em feedback

---

*Módulo gerado automaticamente pelo ARQV30 Enhanced v3.0*
"""

# Instância global
enhanced_module_processor = EnhancedModuleProcessor()