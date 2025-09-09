
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - AI Manager Corrigido
Gerenciador de IA com fallback robusto e tratamento de erros
"""

import os
import logging
import time
import json
import asyncio
from typing import Dict, List, Optional, Any, Union
import requests
from datetime import datetime, timedelta

# Imports condicionais para os clientes de IA
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

logger = logging.getLogger(__name__)

class AIManager:
    """Gerenciador de IA com fallback automático corrigido"""

    def __init__(self):
        """Inicializa o gerenciador de IA"""
        self.providers = {}
        self.last_used_provider = None
        self.error_counts = {}
        
        self._initialize_providers()
        logger.info(f"✅ AI Manager inicializado com {len(self.providers)} provedores")

    def _initialize_providers(self):
        """Inicializa todos os provedores de IA disponíveis"""
        
        # Inicializa Gemini
        if HAS_GEMINI:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.providers['gemini'] = {
                        'client': genai,
                        'available': True,
                        'model': 'gemini-2.0-flash-exp',
                        'priority': 1,
                        'error_count': 0
                    }
                    logger.info("✅ Gemini inicializado")
                except Exception as e:
                    logger.error(f"❌ Erro ao inicializar Gemini: {e}")
            else:
                logger.warning("⚠️ GEMINI_API_KEY não configurada")

        # Inicializa OpenAI
        if HAS_OPENAI:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                try:
                    self.providers['openai'] = {
                        'client': OpenAI(api_key=api_key),
                        'available': True,
                        'model': 'gpt-4o',
                        'priority': 2,
                        'error_count': 0
                    }
                    logger.info("✅ OpenAI inicializado")
                except Exception as e:
                    logger.error(f"❌ Erro ao inicializar OpenAI: {e}")
            else:
                logger.warning("⚠️ OPENAI_API_KEY não configurada")

        # Inicializa Groq
        if HAS_GROQ:
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                try:
                    self.providers['groq'] = {
                        'client': Groq(api_key=api_key),
                        'available': True,
                        'model': 'llama3-70b-8192',
                        'priority': 3,
                        'error_count': 0
                    }
                    logger.info("✅ Groq inicializado")
                except Exception as e:
                    logger.error(f"❌ Erro ao inicializar Groq: {e}")
            else:
                logger.warning("⚠️ GROQ_API_KEY não configurada")

    def _get_available_provider(self, require_tools: bool = False) -> Optional[str]:
        """Seleciona o melhor provedor disponível"""
        available_providers = []
        
        for name, provider in self.providers.items():
            if not provider['available']:
                continue
            
            available_providers.append((name, provider['priority']))
        
        if not available_providers:
            return None
            
        # Ordena por prioridade (menor número = maior prioridade)
        available_providers.sort(key=lambda x: x[1])
        return available_providers[0][0]

    def generate_text(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """Gera texto usando o melhor provedor disponível"""
        provider_name = self._get_available_provider()
        
        if not provider_name:
            raise Exception("Nenhum provedor de IA disponível")
        
        provider = self.providers[provider_name]
        
        try:
            if provider_name == 'gemini':
                result = self._generate_gemini(prompt, max_tokens, temperature)
            elif provider_name == 'openai':
                result = self._generate_openai(prompt, max_tokens, temperature)
            elif provider_name == 'groq':
                result = self._generate_groq(prompt, max_tokens, temperature)
            else:
                raise Exception(f"Provedor {provider_name} não implementado")
            
            # Registra sucesso
            provider['error_count'] = 0
            
            logger.info(f"✅ {provider_name} gerou {len(result)} caracteres")
            return result
            
        except Exception as e:
            # Registra falha
            provider['error_count'] += 1
            
            logger.error(f"❌ Erro no {provider_name}: {e}")
            
            # Desabilita provedor se muitos erros
            if provider['error_count'] >= 3:
                provider['available'] = False
                logger.warning(f"⚠️ {provider_name} desabilitado temporariamente")
                return self.generate_text(prompt, max_tokens, temperature)
            
            raise

    def _generate_gemini(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Gera texto usando Gemini"""
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            )
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        except Exception as e:
            logger.error(f"❌ Erro no Gemini: {e}")
            raise

    def _generate_openai(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Gera texto usando OpenAI"""
        try:
            client = self.providers['openai']['client']
            response = client.chat.completions.create(
                model=self.providers['openai']['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ Erro no OpenAI: {e}")
            raise

    def _generate_groq(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Gera texto usando Groq"""
        try:
            client = self.providers['groq']['client']
            response = client.chat.completions.create(
                model=self.providers['groq']['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ Erro no Groq: {e}")
            raise

    def generate_analysis(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """Gera análise usando o melhor provedor disponível - método compatível"""
        try:
            return self.generate_text(prompt, max_tokens, temperature)
        except Exception as e:
            logger.error(f"❌ Erro na geração de análise: {e}")
            return f"Análise não pôde ser gerada devido a erro técnico: {str(e)}"

    def generate_content(self, prompt: str, max_tokens: int = 4000) -> str:
        """Método de compatibilidade para generate_content"""
        return self.generate_analysis(prompt, max_tokens)

    def is_available(self) -> bool:
        """Verifica se há pelo menos um provedor disponível"""
        return any(provider['available'] for provider in self.providers.values())

    def get_status(self) -> Dict[str, Any]:
        """Retorna status dos provedores"""
        status = {
            'total_providers': len(self.providers),
            'available_providers': sum(1 for p in self.providers.values() if p['available']),
            'providers': {}
        }
        
        for name, provider in self.providers.items():
            status['providers'][name] = {
                'available': provider['available'],
                'model': provider['model'],
                'error_count': provider['error_count']
            }
        
        return status

# Instância global
ai_manager = AIManager()

            
        except Exception as e:
            logger.error(f"❌ Erro no OpenAI com ferramentas: {e}")
            raise

    def _format_search_results(self, search_result: Dict[str, Any]) -> str:
        """Formata resultados de busca para contexto da IA"""
        if 'error' in search_result:
            return f"Erro na busca: {search_result['error']}"
        
        formatted = f"Busca: {search_result.get('query', '')}\n"
        formatted += f"Total encontrado: {search_result.get('total_found', 0)} resultados\n\n"
        
        for i, result in enumerate(search_result.get('results', []), 1):
            formatted += f"{i}. {result.get('title', 'Sem título')}\n"
            formatted += f"   URL: {result.get('url', '')}\n"
            formatted += f"   Resumo: {result.get('snippet', 'Sem descrição')}\n\n"
        
        return formatted

    async def generate_text(self, prompt: str, max_tokens: int = 8192, temperature: float = 0.7) -> str:
        """Gera texto usando o melhor provedor disponível"""
        provider_name = self._get_available_provider()
        
        if not provider_name:
            raise Exception("Nenhum provedor de IA disponível")
        
        provider = self.providers[provider_name]
        
        try:
            start_time = time.time()
            
            if provider_name == 'gemini':
                result = await self._generate_gemini(prompt, max_tokens, temperature)
            elif provider_name == 'openai':
                result = await self._generate_openai(prompt, max_tokens, temperature)
            elif provider_name == 'groq':
                result = provider['client'].generate(prompt, max_tokens)
            else:
                raise Exception(f"Provedor {provider_name} não implementado")
            
            # Registra sucesso
            provider['last_success'] = datetime.now()
            provider['consecutive_failures'] = 0
            
            processing_time = time.time() - start_time
            logger.info(f"✅ {provider_name} gerou {len(result)} caracteres em {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            # Registra falha
            provider['error_count'] += 1
            provider['consecutive_failures'] += 1
            
            logger.error(f"❌ Erro no {provider_name}: {e}")
            
            # Tenta próximo provedor se houver falhas consecutivas
            if provider['consecutive_failures'] >= provider['max_errors']:
                provider['available'] = False
                logger.warning(f"⚠️ {provider_name} desabilitado temporariamente")
                return await self.generate_text(prompt, max_tokens, temperature)
            
            raise

    async def _generate_gemini(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Gera texto usando Gemini"""
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response.text

    async def _generate_openai(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Gera texto usando OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content

    def generate_analysis(self, prompt: str, max_tokens: int = 8192, temperature: float = 0.7) -> str:
        """Gera análise usando o melhor provedor disponível - método compatível com módulos"""
        try:
            # Executa de forma síncrona usando asyncio
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Se já há um loop rodando, cria uma nova task
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self.generate_text(prompt, max_tokens, temperature))
                        return future.result(timeout=60)
                else:
                    return loop.run_until_complete(self.generate_text(prompt, max_tokens, temperature))
            except RuntimeError:
                # Se não há loop, cria um novo
                return asyncio.run(self.generate_text(prompt, max_tokens, temperature))
        except Exception as e:
            logger.error(f"❌ Erro na geração de análise: {e}")
            # Retorna resposta de fallback em caso de erro
            return f"Análise não pôde ser gerada devido a erro técnico: {str(e)}"

    def get_status(self) -> Dict[str, Any]:
        """Retorna status dos provedores"""
        status = {
            'total_providers': len(self.providers),
            'available_providers': sum(1 for p in self.providers.values() if p['available']),
            'providers': {}
        }
        
        for name, provider in self.providers.items():
            status['providers'][name] = {
                'available': provider['available'],
                'model': provider['model'],
                'error_count': provider['error_count'],
                'consecutive_failures': provider['consecutive_failures'],
                'last_success': provider['last_success'].isoformat() if provider['last_success'] else None,
                'supports_tools': provider.get('supports_tools', False)
            }
        
        return status

# Instância global
ai_manager = AIManager()
