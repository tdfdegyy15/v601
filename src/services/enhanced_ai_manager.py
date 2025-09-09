#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v3.0 - Enhanced AI Manager
Gerenciador de IA com suporte a ferramentas e busca ativa
"""

import os
import logging
import asyncio
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

# Imports condicionais
try:
    import google.generativeai as genai
    from google.generativeai.types import FunctionDeclaration, Tool
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

# Adicionando suporte ao OpenRouter
try:
    import openai as openrouter_openai
    HAS_OPENROUTER = True
except ImportError:
    HAS_OPENROUTER = False

logger = logging.getLogger(__name__)

class EnhancedAIManager:
    """Gerenciador de IA aprimorado com ferramentas de busca ativa"""

    def __init__(self):
        """Inicializa o gerenciador aprimorado"""
        self.providers = {}
        self.current_provider = None
        self.search_orchestrator = None

        self._initialize_providers()
        self._initialize_search_tools()

        logger.info(f"🤖 Enhanced AI Manager inicializado com {len(self.providers)} provedores")

    def _initialize_providers(self):
        """Inicializa todos os provedores de IA"""

        # Qwen via OpenRouter (Prioridade 1 - mais confiável)
        if HAS_OPENROUTER:
            api_key = os.getenv("OPENROUTER_API_KEY")
            if api_key:
                try:
                    openrouter_client = openrouter_openai.OpenAI(
                        api_key=api_key,
                        base_url="https://openrouter.ai/api/v1"
                    )
                    self.providers["openrouter"] = {
                        "client": openrouter_client,
                        "model": "qwen/qwen2.5-vl-32b-instruct:free",
                        "available": True,
                        "supports_tools": False, # Ajuste se o modelo suportar tools
                        "priority": 1
                    }
                    logger.info("✅ Qwen via OpenRouter configurado")
                except Exception as e:
                    logger.error(f"❌ Erro ao configurar Qwen/OpenRouter: {e}")

        # Gemini (Prioridade 2)
        if HAS_GEMINI:
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.providers["gemini"] = {
                        "client": genai,
                        "model": "gemini-2.0-flash-exp",
                        "available": True,
                        "supports_tools": True,
                        "priority": 2
                    }
                    logger.info("✅ Gemini 2.0 Flash configurado")
                except Exception as e:
                    logger.error(f"❌ Erro ao configurar Gemini: {e}")

        # Groq (Prioridade 3 - fallback confiável) - ATUALIZADO PARA MODELO SUPORTADO
        if HAS_GROQ:
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                try:
                    self.providers["groq"] = {
                        "client": Groq(api_key=api_key),
                        "model": "llama3-70b-8192", # Modelo atualizado - veja a tabela de depreciações
                        "available": True,
                        "supports_tools": False,
                        "priority": 3
                    }
                    logger.info("✅ Groq Llama configurado")
                except Exception as e:
                    logger.error(f"❌ Erro ao configurar Groq: {e}")

        # OpenAI (Prioridade 4)
        if HAS_OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                try:
                    self.providers["openai"] = {
                        "client": openai.OpenAI(api_key=api_key),
                        "model": "gpt-4o",
                        "available": True, # Habilitado
                        "supports_tools": True,
                        "priority": 4
                    }
                    logger.info("✅ OpenAI GPT-4o configurado")
                except Exception as e:
                    logger.error(f"❌ Erro ao configurar OpenAI: {e}")

    def _initialize_search_tools(self):
        """Inicializa ferramentas de busca"""
        self.search_orchestrator = None
        logger.info("✅ Search tools inicializadas (placeholder)")

    def _get_best_provider(self, require_tools: bool = False) -> Optional[str]:
        """Seleciona o melhor provedor disponível"""
        available = []

        for name, provider in self.providers.items():
            if not provider["available"]:
                continue

            available.append((name, provider["priority"]))

        if available:
            # Ordena pela prioridade (menor número = maior prioridade)
            available.sort(key=lambda x: x[1])
            return available[0][0]

        return None

    async def generate_text(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """Gera texto usando o melhor provedor disponível"""
        provider_name = self._get_best_provider()

        if not provider_name:
            logger.warning("⚠️ Nenhum provedor disponível")
            return "Erro: Nenhum provedor de IA disponível para gerar texto."

        provider = self.providers[provider_name]
        logger.info(f"🤖 Usando {provider_name} para geração de texto")

        try:
            if provider_name == "openrouter":
                client = provider["client"]
                response = client.chat.completions.create(
                    model=provider["model"],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content

            elif provider_name == "gemini":
                model = genai.GenerativeModel("gemini-2.0-flash-exp")
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=temperature,
                    )
                )
                return response.text

            elif provider_name == "groq":
                client = provider["client"]
                response = client.chat.completions.create(
                    model=provider["model"],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content

            elif provider_name == "openai":
                client = provider["client"]
                response = client.chat.completions.create(
                    model=provider["model"],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"❌ Erro na geração de texto com {provider_name}: {e}")
            return f"Erro na geração: {str(e)}"

        return "Erro: Método de geração não implementado para este provedor"

    def is_available(self) -> bool:
        """Verifica se há pelo menos um provedor disponível"""
        return any(provider['available'] for provider in self.providers.values())

    def generate_analysis(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """Método de compatibilidade para generate_analysis"""
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
            return f"Análise não pôde ser gerada devido a erro técnico: {str(e)}"

    def generate_content(self, prompt: str, max_tokens: int = 4000) -> str:
        """Método de compatibilidade para generate_content"""
        return self.generate_analysis(prompt, max_tokens)


# Instância global
enhanced_ai_manager = EnhancedAIManager()
