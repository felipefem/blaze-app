# BLAZE IA 3.0 - SISTEMA 100% AUTOMÁTICO
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter, defaultdict
import numpy as np
from datetime import datetime, timedelta
import json
import pickle
import os
import random
import time
import threading

# Configuração da página
st.set_page_config(
    page_title="Blaze IA Auto - Sistema Automático",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado premium
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .auto-on {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        border: 3px solid #00b09b;
        animation: pulse 2s infinite;
    }
    .auto-off {
        background: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        border: 3px solid #8E2DE2;
    }
    .prediction-high {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 2px solid #00b09b;
    }
    .prediction-medium {
        background: linear-gradient(135deg, #f46b45 0%, #eea849 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 2px solid #eea849;
    }
    .prediction-low {
        background: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 2px solid #8E2DE2;
    }
    .stats-card {
        background: rgba(30, 30, 30, 0.8);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #FFD700;
        backdrop-filter: blur(10px);
    }
    .bet-won {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        padding: 0.8rem;
        border-radius: 10px;
        color: white;
        margin: 0.3rem 0;
    }
    .bet-lost {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 0.8rem;
        border-radius: 10px;
        color: white;
        margin: 0.3rem 0;
    }
    .bank-up {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .bank-down {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .sequence-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online {
        background: #00b09b;
        animation: blink 2s infinite;
    }
    .status-offline {
        background: #ff4b2b;
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">⚡ BLAZE IA AUTO - SISTEMA 100% AUTOMÁTICO</h1>', unsafe_allow_html=True)
st.markdown("### 🤖 IA Avançada • ⚡ Atualização Automática • 💰 Apostas Autônomas")

# Sistema de arquivos
IA_DATA_FILE = "ia_blaze_auto.pkl"

# Classe da IA AUTO com sistema totalmente automático
class BlazeIA_Auto:
    def __init__(self):
        self.historico = []
        self.previsoes = []
        self.padroes_aprendidos = defaultdict(list)
        self.apostas = []
        self.saldo = 1000.0
        self.estatisticas = {
            'total_previsoes': 0,
            'acertos': 0,
            'melhor_sequencia': 0,
            'sequencia_atual': 0,
            'metodos_eficazes': defaultdict(int),
            'ultima_atualizacao': datetime.now(),
            'total_apostas': 0,
            'apostas_vencedoras': 0,
            'lucro_total': 0.0,
            'maior_sequencia_vitorias': 0,
            'sequencia_vitorias_atual': 0,
            'ultimo_resultado_verificado': None
        }
        self.ultimo_id_aposta = 0
        self.modo_auto = False
        self.ultima_atualizacao = datetime.now()
        self.carregar_dados()
        
    def carregar_dados(self):
        """Carrega dados históricos da IA"""
        try:
            if os.path.exists(IA_DATA_FILE):
                with open(IA_DATA_FILE, 'rb') as f:
                    dados = pickle.load(f)
                    self.historico = dados.get('historico', [])
                    self.previsoes = dados.get('previsoes', [])
                    self.apostas = dados.get('apostas', [])
                    self.saldo = dados.get('saldo', 1000.0)
                    self.ultimo_id_aposta = dados.get('ultimo_id_aposta', 0)
                    self.modo_auto = dados.get('modo_auto', False)
                    
                    padroes_carregados = dados.get('padroes', {})
                    self.padroes_aprendidos = defaultdict(list)
                    for k, v in padroes_carregados.items():
                        if isinstance(k, (tuple, list)):
                            self.padroes_aprendidos[tuple(k)] = v
                    
                    self.estatisticas = dados.get('estatisticas', self.estatisticas)
                st.success(f"📚 Sistema carregado: {len(self.historico)} registros, {len(self.apostas)} apostas")
        except Exception as e:
            st.warning(f"⚠️ Iniciando novo sistema: {e}")
            self.resetar_sistema()
    
    def salvar_dados(self):
        """Salva dados da IA"""
        try:
            padroes_para_salvar = {k: v for k, v in self.padroes_aprendidos.items()}
            
            dados = {
                'historico': self.historico,
                'previsoes': self.previsoes,
                'apostas': self.apostas,
                'saldo': self.saldo,
                'ultimo_id_aposta': self.ultimo_id_aposta,
                'modo_auto': self.modo_auto,
                'padroes': padroes_para_salvar,
                'estatisticas': self.estatisticas
            }
            with open(IA_DATA_FILE, 'wb') as f:
                pickle.dump(dados, f)
        except Exception as e:
            st.error(f"❌ Erro ao salvar: {e}")
    
    def resetar_sistema(self):
        """Reseta todo o sistema"""
        self.historico = []
        self.previsoes = []
        self.padroes_aprendidos = defaultdict(list)
        self.apostas = []
        self.saldo = 1000.0
        self.ultimo_id_aposta = 0
        self.modo_auto = False
        self.estatisticas = {
            'total_previsoes': 0,
            'acertos': 0,
            'melhor_sequencia': 0,
            'sequencia_atual': 0,
            'metodos_eficazes': defaultdict(int),
            'ultima_atualizacao': datetime.now(),
            'total_apostas': 0,
            'apostas_vencedoras': 0,
            'lucro_total': 0.0,
            'maior_sequencia_vitorias': 0,
            'sequencia_vitorias_atual': 0,
            'ultimo_resultado_verificado': None
        }
    
    def alternar_modo_auto(self):
        """Alterna entre modo automático e manual"""
        self.modo_auto = not self.modo_auto
        self.salvar_dados()
        return self.modo_auto
    
    def calcular_valor_aposta(self, confianca):
        """Calcula valor da aposta baseado na confiança e estratégia"""
        base = self.saldo * 0.02  # 2% do saldo como base
        
        if confianca > 0.8:
            return min(base * 2, self.saldo * 0.1)  # Máximo 10% do saldo
        elif confianca > 0.65:
            return base * 1.5
        elif confianca > 0.55:
            return base
        else:
            return base * 0.5  # Aposta menor para confiança baixa
    
    def fazer_aposta_automatica(self, previsao):
        """Faz aposta automática baseada na previsão da IA"""
        valor_aposta = self.calcular_valor_aposta(previsao['confianca'])
        
        if valor_aposta > self.saldo or valor_aposta < 1:
            return None  # Saldo insuficiente ou valor muito baixo
        
        self.ultimo_id_aposta += 1
        aposta = {
            'id': self.ultimo_id_aposta,
            'timestamp': datetime.now(),
            'previsao': previsao['previsao'],
            'valor': round(valor_aposta, 2),
            'confianca': previsao['confianca'],
            'metodo': previsao['metodo'],
            'resultado': None,
            'lucro': 0.0,
            'cor': previsao['previsao'],
            'status': 'ativa'
        }
        
        self.apostas.append(aposta)
        self.saldo -= valor_aposta
        self.estatisticas['total_apostas'] += 1
        
        return aposta
    
    def verificar_apostas_ativas(self, resultado_atual):
        """Verifica e atualiza apostas ativas com o resultado atual"""
        apostas_atualizadas = []
        
        for aposta in self.apostas:
            if aposta['status'] == 'ativa' and aposta['resultado'] is None:
                # Verificar se a aposta acertou
                acertou = (aposta['cor'] == resultado_atual)
                
                if acertou:
                    # Calcular lucro (aposta em cores paga 2x)
                    lucro = aposta['valor'] * 2
                    aposta['resultado'] = 'ganhou'
                    aposta['lucro'] = lucro
                    aposta['status'] = 'finalizada'
                    self.saldo += lucro
                    self.estatisticas['apostas_vencedoras'] += 1
                    self.estatisticas['lucro_total'] += (lucro - aposta['valor'])
                    self.estatisticas['sequencia_vitorias_atual'] += 1
                    self.estatisticas['maior_sequencia_vitorias'] = max(
                        self.estatisticas['maior_sequencia_vitorias'],
                        self.estatisticas['sequencia_vitorias_atual']
                    )
                else:
                    aposta['resultado'] = 'perdeu'
                    aposta['lucro'] = -aposta['valor']
                    aposta['status'] = 'finalizada'
                    self.estatisticas['sequencia_vitorias_atual'] = 0
                
                apostas_atualizadas.append(aposta)
        
        return apostas_atualizadas
    
    def analisar_tendencias_avancadas(self, dados):
        """Análise avançada de tendências"""
        if len(dados) < 5:
            return self.previsao_inteligente_fallback(dados)
        
        ultimas_15 = [dados[i].get('color', 0) for i in range(min(15, len(dados)))]
        ultimas_cores = ultimas_15[:10]
        
        # Estratégia 1: Sequências longas
        sequencia_resultado = self.analisar_sequencias_longas(ultimas_cores)
        if sequencia_resultado:
            return sequencia_resultado
        
        # Estratégia 2: Padrões de alternância
        alternancia_resultado = self.detectar_padrao_alternancia(ultimas_cores)
        if alternancia_resultado:
            return alternancia_resultado
        
        # Estratégia 3: Análise de clusters
        cluster_resultado = self.analisar_clusters(ultimas_15)
        if cluster_resultado:
            return cluster_resultado
        
        # Estratégia 4: Frequência relativa ajustada
        return self.analise_frequencia_ajustada(dados)
    
    def analisar_sequencias_longas(self, ultimas_cores):
        if len(ultimas_cores) >= 4:
            for cor in [1, 2]:
                if all(c == cor for c in ultimas_cores[:4]):
                    cor_oposta = 2 if cor == 1 else 1
                    return {
                        'previsao': cor_oposta, 
                        'confianca': 0.88, 
                        'metodo': 'Sequência Longa (4+)',
                        'probabilidades': self.calcular_prob_sequencia(cor_oposta),
                        'detalhes': f'Sequência de {4} {self.nome_cor(cor)} detectada'
                    }
        
        if len(ultimas_cores) >= 3:
            for cor in [1, 2]:
                if all(c == cor for c in ultimas_cores[:3]):
                    cor_oposta = 2 if cor == 1 else 1
                    return {
                        'previsao': cor_oposta, 
                        'confianca': 0.78, 
                        'metodo': 'Sequência Média (3)',
                        'probabilidades': self.calcular_prob_sequencia(cor_oposta),
                        'detalhes': f'Sequência de {3} {self.nome_cor(cor)} detectada'
                    }
        return None
    
    def detectar_padrao_alternancia(self, ultimas_cores):
        if len(ultimas_cores) >= 6:
            padrao_zebra = all(ultimas_cores[i] != ultimas_cores[i+1] for i in range(len(ultimas_cores)-1))
            if padrao_zebra:
                ultima_cor = ultimas_cores[0]
                cor_oposta = 2 if ultima_cor == 1 else 1
                return {
                    'previsao': cor_oposta,
                    'confianca': 0.72,
                    'metodo': 'Padrão Zebra Perfeito',
                    'probabilidades': self.calcular_prob_alternancia(cor_oposta),
                    'detalhes': 'Padrão de alternância constante detectado'
                }
        return None
    
    def analisar_clusters(self, dados):
        if len(dados) < 8:
            return None
            
        metade1 = dados[:len(dados)//2]
        metade2 = dados[len(dados)//2:]
        
        count_red1 = metade1.count(1)
        count_black1 = metade1.count(2)
        count_red2 = metade2.count(1)
        count_black2 = metade2.count(2)
        
        diff_red = count_red1 - count_red2
        
        if abs(diff_red) > 3:
            previsao = 2 if diff_red > 0 else 1
            return {
                'previsao': previsao,
                'confianca': 0.68,
                'metodo': 'Análise de Clusters',
                'probabilidades': self.calcular_prob_cluster(previsao),
                'detalhes': f'Mudança de cluster detectada: {diff_red} vermelhos'
            }
        return None
    
    def analise_frequencia_ajustada(self, dados):
        todas_cores = [jogo.get('color', 0) for jogo in dados]
        cores_recentes = todas_cores[:20]
        
        total_geral = len(todas_cores)
        if total_geral == 0:
            return self.previsao_inteligente_fallback(dados)
        
        count_red_geral = todas_cores.count(1)
        count_black_geral = todas_cores.count(2)
        count_zero_geral = todas_cores.count(0)
        
        prob_red_base = count_red_geral / total_geral
        prob_black_base = count_black_geral / total_geral
        prob_zero_base = count_zero_geral / total_geral
        
        # Ajustes dinâmicos
        ajuste_tendencia = 0.2
        total_recente = len(cores_recentes)
        
        if total_recente > 5:
            count_red_recente = cores_recentes.count(1)
            count_black_recente = cores_recentes.count(2)
            tendencia_red = count_red_recente / total_recente
            tendencia_black = count_black_recente / total_recente
            
            if tendencia_red > tendencia_black + 0.3:
                prob_red_base *= (1 - ajuste_tendencia)
                prob_black_base *= (1 + ajuste_tendencia)
            elif tendencia_black > tendencia_red + 0.3:
                prob_black_base *= (1 - ajuste_tendencia)
                prob_red_base *= (1 + ajuste_tendencia)
        
        total_prob = prob_red_base + prob_black_base + prob_zero_base
        prob_red = prob_red_base / total_prob
        prob_black = prob_black_base / total_prob
        prob_zero = prob_zero_base / total_prob
        
        if prob_black > prob_red:
            previsao = 2
            confianca = prob_black
        else:
            previsao = 1
            confianca = prob_red
        
        diferenca = abs(prob_red - prob_black)
        confianca_ajustada = 0.5 + (diferenca * 0.5)
        
        return {
            'previsao': previsao,
            'confianca': min(confianca_ajustada, 0.85),
            'metodo': 'Probabilístico Ajustado',
            'probabilidades': [prob_zero, prob_red, prob_black],
            'detalhes': f'Diferença: {diferenca:.2f} | Base: {total_geral} jogos'
        }
    
    def calcular_prob_sequencia(self, cor_previsao):
        if cor_previsao == 1:
            return [0.02, 0.78, 0.20]
        else:
            return [0.02, 0.20, 0.78]
    
    def calcular_prob_alternancia(self, cor_previsao):
        return [0.03, 0.485, 0.485]
    
    def calcular_prob_cluster(self, cor_previsao):
        if cor_previsao == 1:
            return [0.03, 0.67, 0.30]
        else:
            return [0.03, 0.30, 0.67]
    
    def nome_cor(self, cor):
        return "Vermelho" if cor == 1 else "Preto" if cor == 2 else "Zero"
    
    def previsao_inteligente_fallback(self, dados):
        if len(dados) >= 2:
            ultimas_2 = [dados[i].get('color', 0) for i in range(min(2, len(dados)))]
            if ultimas_2[0] == ultimas_2[1] and ultimas_2[0] in [1, 2]:
                cor_oposta = 2 if ultimas_2[0] == 1 else 1
                return {
                    'previsao': cor_oposta,
                    'confianca': 0.55,
                    'metodo': 'Tendência Inicial',
                    'probabilidades': [0.05, 0.475, 0.475],
                    'detalhes': 'Sequência inicial detectada'
                }
        
        return {
            'previsao': random.choice([1, 2]),
            'confianca': 0.5,
            'metodo': 'Aleatório com Viés',
            'probabilidades': [0.05, 0.475, 0.475],
            'detalhes': 'Poucos dados para análise'
        }
    
    def executar_ciclo_automatico(self):
        """Executa um ciclo completo do sistema automático"""
        if not self.modo_auto:
            return None
        
        try:
            # Buscar dados
            dados = self.buscar_dados_roleta()
            if not dados:
                return None
            
            # Processar dados
            resultado = self.processar_dados_automatico(dados)
            self.ultima_atualizacao = datetime.now()
            self.salvar_dados()
            
            return resultado
            
        except Exception as e:
            st.error(f"❌ Erro no ciclo automático: {e}")
            return None
    
    def buscar_dados_roleta(self):
        """Busca dados da API da Blaze"""
        url = 'https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://blaze.com/',
            'Origin': 'https://blaze.com'
        }
        
        try:
            resposta = requests.get(url, headers=headers, timeout=10)
            if resposta.status_code == 200:
                dados = resposta.json()
                if isinstance(dados, list) and len(dados) > 0:
                    return dados
        except:
            pass
        
        return None
    
    def processar_dados_automatico(self, dados):
        """Processa dados e executa todas as ações automáticas"""
        # Adicionar dados ao histórico
        novos_dados = []
        for jogo in dados:
            if jogo not in self.historico:
                novos_dados.append(jogo)
        
        self.historico.extend(novos_dados)
        
        if len(self.historico) > 2000:
            self.historico = self.historico[-2000:]
        
        # Fazer previsão
        previsao = self.analisar_tendencias_avancadas(dados)
        
        # Registrar previsão automaticamente
        previsao_registro = {
            'timestamp': datetime.now(),
            'previsao': previsao['previsao'],
            'confianca': previsao['confianca'],
            'metodo': previsao['metodo'],
            'dados_utilizados': len(dados),
            'acertou': None,
            'detalhes': previsao.get('detalhes', ''),
            'resultado_real': None
        }
        self.previsoes.append(previsao_registro)
        
        # Fazer aposta automática se confiança > 55%
        if previsao['confianca'] > 0.55:
            aposta = self.fazer_aposta_automatica(previsao)
            if aposta:
                previsao_registro['aposta_id'] = aposta['id']
        
        # Verificar resultados anteriores
        self.verificar_resultados_automaticos(dados)
        
        # Aprender com padrões
        try:
            self.aprender_padroes(dados)
        except:
            pass
        
        # Atualizar estatísticas
        self.estatisticas['total_previsoes'] += 1
        self.estatisticas['ultima_atualizacao'] = datetime.now()
        
        return previsao
    
    def verificar_resultados_automaticos(self, dados_reais):
        """Verifica automaticamente resultados das previsões"""
        if not dados_reais:
            return
        
        resultado_mais_recente = dados_reais[0].get('color')
        
        # Só processar se for um resultado novo
        if resultado_mais_recente == self.estatisticas['ultimo_resultado_verificado']:
            return
        
        self.estatisticas['ultimo_resultado_verificado'] = resultado_mais_recente
        
        # Verificar apostas ativas
        apostas_atualizadas = self.verificar_apostas_ativas(resultado_mais_recente)
        
        # Verificar previsões não verificadas (apenas as mais recentes)
        for previsao in self.previsoes[-5:]:
            if previsao.get('acertou') is None and previsao.get('resultado_real') is None:
                previsao['resultado_real'] = resultado_mais_recente
                previsao['acertou'] = (previsao['previsao'] == resultado_mais_recente)
                
                if previsao['acertou']:
                    self.estatisticas['acertos'] += 1
                    self.estatisticas['sequencia_atual'] += 1
                    self.estatisticas['melhor_sequencia'] = max(
                        self.estatisticas['melhor_sequencia'], 
                        self.estatisticas['sequencia_atual']
                    )
                    metodo = previsao.get('metodo', 'Desconhecido')
                    self.estatisticas['metodos_eficazes'][metodo] += 1
                else:
                    self.estatisticas['sequencia_atual'] = 0
    
    def aprender_padroes(self, dados):
        if len(dados) < 8:
            return
        
        try:
            for i in range(len(dados) - 6):
                sequencia = []
                valida = True
                
                for j in range(i, i+5):
                    if j < len(dados):
                        cor = dados[j].get('color')
                        if cor is None:
                            valida = False
                            break
                        sequencia.append(cor)
                    else:
                        valida = False
                        break
                
                if not valida or len(sequencia) != 5:
                    continue
                
                resultado_index = i + 5
                if resultado_index < len(dados):
                    resultado = dados[resultado_index].get('color')
                    if resultado in [1, 2]:
                        chave = tuple(sequencia)
                        self.padroes_aprendidos[chave].append(resultado)
                        
                        if len(self.padroes_aprendidos[chave]) > 50:
                            self.padroes_aprendidos[chave] = self.padroes_aprendidos[chave][-50:]
        except:
            pass
    
    def get_estatisticas_apostas(self):
        """Retorna estatísticas detalhadas das apostas"""
        if not self.apostas:
            return {
                'total': 0,
                'vencedoras': 0,
                'perdedoras': 0,
                'taxa_acerto': 0,
                'lucro_total': 0,
                'roi': 0
            }
        
        apostas_finalizadas = [a for a in self.apostas if a['status'] == 'finalizada']
        total = len(apostas_finalizadas)
        vencedoras = len([a for a in apostas_finalizadas if a['resultado'] == 'ganhou'])
        perdedoras = len([a for a in apostas_finalizadas if a['resultado'] == 'perdeu'])
        lucro_total = sum(a['lucro'] for a in apostas_finalizadas)
        investido_total = sum(a['valor'] for a in apostas_finalizadas if a['resultado'] == 'perdeu')
        
        taxa_acerto = vencedoras / total if total > 0 else 0
        roi = (lucro_total / investido_total * 100) if investido_total > 0 else 0
        
        return {
            'total': total,
            'vencedoras': vencedoras,
            'perdedoras': perdedoras,
            'taxa_acerto': taxa_acerto,
            'lucro_total': lucro_total,
            'roi': roi
        }

# Inicializar IA AUTO
if 'ia_auto' not in st.session_state:
    st.session_state.ia_auto = BlazeIA_Auto()

# Configurar atualização automática
if 'ultima_execucao' not in st.session_state:
    st.session_state.ultima_execucao = datetime.now()

# Verificar se precisa executar ciclo automático
tempo_decorrido = (datetime.now() - st.session_state.ultima_execucao).total_seconds()
if st.session_state.ia_auto.modo_auto and tempo_decorrido > 30:  # Executar a cada 30 segundos
    with st.spinner("🔄 Executando ciclo automático..."):
        resultado = st.session_state.ia_auto.executar_ciclo_automatico()
        st.session_state.ultima_execucao = datetime.now()
        if resultado:
            st.rerun()

# SIDEBAR AUTOMÁTICA
with st.sidebar:
    st.markdown("### ⚡ CONTROLE PRINCIPAL")
    
    # Botão LIGAR/DESLIGAR
    col_auto1, col_auto2 = st.columns([1, 2])
    with col_auto1:
        status_class = "status-online" if st.session_state.ia_auto.modo_auto else "status-offline"
        st.markdown(f'<div class="{status_class}"></div>', unsafe_allow_html=True)
    
    with col_auto2:
        if st.session_state.ia_auto.modo_auto:
            if st.button("🔴 PARAR SISTEMA", use_container_width=True, type="primary"):
                st.session_state.ia_auto.alternar_modo_auto()
                st.rerun()
        else:
            if st.button("🟢 LIGAR SISTEMA", use_container_width=True, type="primary"):
                st.session_state.ia_auto.alternar_modo_auto()
                st.rerun()
    
    # Status do modo automático
    if st.session_state.ia_auto.modo_auto:
        st.markdown('<div class="auto-on">', unsafe_allow_html=True)
        st.markdown("### 🟢 SISTEMA LIGADO")
        st.markdown("**Atualização automática ativa**")
        st.markdown("⏰ Próxima atualização: 30 segundos")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="auto-off">', unsafe_allow_html=True)
        st.markdown("### 🔴 SISTEMA PARADO")
        st.markdown("**Modo manual**")
        st.markdown("Clique em LIGAR para ativar")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # BANCO EM TEMPO REAL
    st.markdown("### 💰 BANCO VIRTUAL")
    saldo = st.session_state.ia_auto.saldo
    saldo_class = "bank-up" if saldo >= 1000 else "bank-down"
    st.markdown(f'<div class="{saldo_class}">', unsafe_allow_html=True)
    st.metric("💰 Saldo Atual", f"R$ {saldo:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    estat_apostas = st.session_state.ia_auto.get_estatisticas_apostas()
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("📈 Apostas", f"{estat_apostas['vencedoras']}/{estat_apostas['total']}")
    with col_s2:
        st.metric("🎯 Taxa", f"{estat_apostas['taxa_acerto']:.1%}")
    
    st.markdown("---")
    
    # ESTATÍSTICAS RÁPIDAS
    st.markdown("### 📊 ESTATÍSTICAS")
    desempenho = st.session_state.ia_auto.estatisticas
    
    st.metric("🤖 Previsões", f"{desempenho['acertos']}/{desempenho['total_previsoes']}")
    st.metric("📈 Acurácia", f"{(desempenho['acertos']/desempenho['total_previsoes']):.1%}" if desempenho['total_previsoes'] > 0 else "0%")
    st.metric("🔥 Sequência", desempenho['sequencia_atual'])
    st.metric("💰 Lucro Total", f"R$ {estat_apostas['lucro_total']:.2f}")
    
    st.markdown("---")
    
    # CONTROLES MANUAIS
    st.markdown("### ⚙️ CONTROLES")
    col_man1, col_man2 = st.columns(2)
    with col_man1:
        if st.button("🔄 Atualizar Agora", use_container_width=True):
            if st.session_state.ia_auto.modo_auto:
                st.warning("⏸️ Modo automático pausado temporariamente")
                st.session_state.ia_auto.modo_auto = False
            resultado = st.session_state.ia_auto.executar_ciclo_automatico()
            if resultado:
                st.success("✅ Atualização manual concluída!")
                st.rerun()
    
    with col_man2:
        if st.button("💾 Salvar", use_container_width=True):
            st.session_state.ia_auto.salvar_dados()
            st.success("✅ Sistema salvo!")
    
    if st.button("🔄 Resetar Sistema", type="secondary"):
        if st.checkbox("Confirmar reset completo"):
            st.session_state.ia_auto.resetar_sistema()
            st.success("✅ Sistema resetado!")
            st.rerun()

# LAYOUT PRINCIPAL
st.markdown("### 🎯 PAINEL DE CONTROLE AUTOMÁTICO")

# Buscar dados atuais (sempre)
with st.spinner("🔄 Buscando dados atualizados..."):
    dados = st.session_state.ia_auto.buscar_dados_roleta()

if not dados:
    st.error("Não foi possível carregar dados. Verifique a conexão.")
    st.stop()

# Se estiver no modo automático, processar dados
if st.session_state.ia_auto.modo_auto:
    with st.spinner("⚡ Processando automaticamente..."):
        previsao_ia = st.session_state.ia_auto.processar_dados_automatico(dados)
else:
    # No modo manual, apenas mostrar dados sem processar
    previsao_ia = st.session_state.ia_auto.analisar_tendencias_avancadas(dados)

# LINHA 1: MÉTRICAS PRINCIPAIS
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🎰 Total Jogos", len(dados))

with col2:
    ultimo_numero = dados[0].get('roll', 'N/A')
    st.metric("🔢 Último Número", ultimo_numero)

with col3:
    ultima_cor = dados[0].get('color', 0)
    cor_emoji = "🔴" if ultima_cor == 1 else "⚫" if ultima_cor == 2 else "🟢"
    st.metric("🎨 Última Cor", cor_emoji)

with col4:
    cor_previsao = previsao_ia['previsao']
    cor_ia_emoji = "🔴" if cor_previsao == 1 else "⚫"
    st.metric("🤖 Previsão IA", cor_ia_emoji)

with col5:
    confianca = previsao_ia['confianca']
    st.metric("🎯 Confiança", f"{confianca:.1%}")

# CARD DE PREVISÃO DINÂMICO
st.markdown("---")
confianca_class = "prediction-high" if confianca > 0.7 else "prediction-medium" if confianca > 0.55 else "prediction-low"
st.markdown(f'<div class="{confianca_class}">', unsafe_allow_html=True)

col_pred1, col_pred2, col_pred3 = st.columns([1, 2, 1])
with col_pred2:
    st.markdown(f"### 🎯 PREVISÃO ATIVA: {cor_ia_emoji} {'VERMELHO' if cor_previsao == 1 else 'PRETO'}")
    st.markdown(f"**Confiança:** {confianca:.1%} | **Método:** {previsao_ia['metodo']}")
    if 'detalhes' in previsao_ia:
        st.markdown(f"*{previsao_ia['detalhes']}*")
    
    # Status da aposta automática
    apostas_ativas = [a for a in st.session_state.ia_auto.apostas if a['status'] == 'ativa']
    if apostas_ativas:
        ultima_aposta = apostas_ativas[-1]
        st.success(f"💰 **Aposta automática ativa:** R$ {ultima_aposta['valor']:.2f}")

st.markdown('</div>', unsafe_allow_html=True)

# ABAS PRINCIPAIS (mesmo conteúdo da versão anterior)
tab1, tab2, tab3, tab4 = st.tabs(["🎰 DASHBOARD", "💰 APOSTAS", "📈 RELATÓRIOS", "🔍 ANÁLISE"])

with tab1:
    st.subheader("🎰 DASHBOARD INTERATIVO")
    
    col_dash1, col_dash2 = st.columns([2, 1])
    
    with col_dash1:
        # VISUALIZAÇÃO DE SEQUÊNCIA
        st.markdown("### 🔄 SEQUÊNCIA ATUAL")
        sequencia_cores = []
        for i, jogo in enumerate(dados[:15]):
            cor = jogo.get('color', 0)
            numero = jogo.get('roll', 'N/A')
            sequencia_cores.append((cor, numero, i))
        
        cols_seq = st.columns(15)
        for idx, (cor, numero, pos) in enumerate(sequencia_cores[:15]):
            with cols_seq[idx]:
                emoji = "🔴" if cor == 1 else "⚫" if cor == 2 else "🟢"
                st.markdown(f"""
                <div style='text-align: center; padding: 8px; border-radius: 8px; 
                            background: {"#ff4444" if cor == 1 else "#000000" if cor == 2 else "#00aa00"}; 
                            color: white; font-weight: bold; font-size: 0.9em;'>
                    {emoji}<br>{numero}
                </div>
                """, unsafe_allow_html=True)
        
        # GRÁFICO DE DISTRIBUIÇÃO
        cores = [jogo.get('color') for jogo in dados if jogo.get('color') is not None]
        if cores:
            contador = Counter(cores)
            df_cores = pd.DataFrame({
                'Cor': ['Vermelho', 'Preto', 'Zero'],
                'Quantidade': [contador.get(1,0), contador.get(2,0), contador.get(0,0)]
            })
            
            fig = px.pie(df_cores, values='Quantidade', names='Cor',
                        title='Distribuição de Cores - Dados Reais',
                        color='Cor', color_discrete_map={'Vermelho': 'red', 'Preto': 'black', 'Zero': 'green'})
            st.plotly_chart(fig)
    
    with col_dash2:
        # INFORMAÇÕES RÁPIDAS
        st.markdown("### 📊 INFORMAÇÕES")
        
        # Sequências atuais
        sequencias = []
        cores_simples = [cor for cor, _, _ in sequencia_cores]
        if cores_simples:
            cor_atual = cores_simples[0]
            contagem = 1
            for cor in cores_simples[1:]:
                if cor == cor_atual:
                    contagem += 1
                else:
                    sequencias.append((cor_atual, contagem))
                    cor_atual = cor
                    contagem = 1
            sequencias.append((cor_atual, contagem))
        
        st.write("**🔄 Sequências:**")
        for cor, comprimento in sequencias[:3]:
            cor_nome = "Vermelho" if cor == 1 else "Preto" if cor == 2 else "Zero"
            badge_color = "red" if cor == 1 else "black" if cor == 2 else "green"
            st.markdown(f'<span class="sequence-badge" style="background: {badge_color};">{cor_nome} ×{comprimento}</span>', unsafe_allow_html=True)
        
        # Estatísticas rápidas
        if cores:
            contador = Counter(cores)
            total = len(cores)
            st.write("**📈 Distribuição:**")
            st.write(f"🔴 {contador.get(1,0)} ({contador.get(1,0)/total:.1%})")
            st.write(f"⚫ {contador.get(2,0)} ({contador.get(2,0)/total:.1%})")
            st.write(f"🟢 {contador.get(0,0)} ({contador.get(0,0)/total:.1%})")

# (Continuação com as outras abas - mantendo o mesmo conteúdo da versão anterior)
with tab2:
    st.subheader("💰 HISTÓRICO DE APOSTAS AUTOMÁTICAS")
    
    col_ap1, col_ap2 = st.columns([3, 1])
    
    with col_ap1:
        apostas_recentes = st.session_state.ia_auto.apostas[-20:]
        
        if not apostas_recentes:
            st.info("📝 Nenhuma aposta registrada ainda. As apostas automáticas começam quando a confiança é > 55%")
        else:
            for aposta in reversed(apostas_recentes):
                if aposta['status'] == 'ativa':
                    st.markdown(f'<div class="bet-won">', unsafe_allow_html=True)
                    st.write(f"🔄 **Aposta #{aposta['id']} - ATIVA**")
                    st.write(f"🎯 { '🔴 Vermelho' if aposta['cor'] == 1 else '⚫ Preto'} | 💰 R$ {aposta['valor']:.2f}")
                    st.write(f"📊 Confiança: {aposta['confianca']:.1%} | Método: {aposta['metodo']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                elif aposta['resultado'] == 'ganhou':
                    st.markdown(f'<div class="bet-won">', unsafe_allow_html=True)
                    st.write(f"✅ **Aposta #{aposta['id']} - GANHOU +R$ {aposta['lucro']:.2f}**")
                    st.write(f"🎯 { '🔴 Vermelho' if aposta['cor'] == 1 else '⚫ Preto'} | 💰 R$ {aposta['valor']:.2f}")
                    st.write(f"⏰ {aposta['timestamp'].strftime('%H:%M')} | Método: {aposta['metodo']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bet-lost">', unsafe_allow_html=True)
                    st.write(f"❌ **Aposta #{aposta['id']} - PERDEU R$ {aposta['valor']:.2f}**")
                    st.write(f"🎯 { '🔴 Vermelho' if aposta['cor'] == 1 else '⚫ Preto'} | 💰 R$ {aposta['valor']:.2f}")
                    st.write(f"⏰ {aposta['timestamp'].strftime('%H:%M')} | Método: {aposta['metodo']}")
                    st.markdown('</div>', unsafe_allow_html=True)
    
    with col_ap2:
        st.markdown("### 📈 ESTATÍSTICAS")
        estat = st.session_state.ia_auto.get_estatisticas_apostas()
        
        st.metric("🎯 Total Apostas", estat['total'])
        st.metric("✅ Vitórias", estat['vencedoras'])
        st.metric("❌ Derrotas", estat['perdedoras'])
        st.metric("📊 Taxa Acerto", f"{estat['taxa_acerto']:.1%}")
        st.metric("💰 Lucro Total", f"R$ {estat['lucro_total']:.2f}")
        st.metric("📈 ROI", f"{estat['roi']:.1f}%")

with tab3:
    st.subheader("📈 RELATÓRIOS DE DESEMPENHO")
    
    col_rep1, col_rep2 = st.columns(2)
    
    with col_rep1:
        st.markdown("### 🎯 DESEMPENHO DA IA")
        desempenho = st.session_state.ia_auto.estatisticas
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("🤖 Previsões", desempenho['total_previsoes'])
            st.metric("🎯 Acertos", desempenho['acertos'])
        with col_m2:
            acuracia = (desempenho['acertos'] / desempenho['total_previsoes']) if desempenho['total_previsoes'] > 0 else 0
            st.metric("📈 Acurácia", f"{acuracia:.1%}")
            st.metric("🔥 Sequência", desempenho['sequencia_atual'])
        
        st.markdown("#### 📊 PROGRESSO")
        alvo_acuracia = 0.55
        progresso = min(acuracia / alvo_acuracia, 1.0)
        st.progress(progresso, text=f"Acurácia: {acuracia:.1%} / Meta: {alvo_acuracia:.0%}")
        
        st.markdown("#### 🔧 MÉTODOS")
        if desempenho['metodos_eficazes']:
            for metodo, acertos in list(desempenho['metodos_eficazes'].items())[:5]:
                st.write(f"**{metodo}:** {acertos} acertos")
    
    with col_rep2:
        st.markdown("### 💰 DESEMPENHO FINANCEIRO")
        estat_apostas = st.session_state.ia_auto.get_estatisticas_apostas()
        
        if st.session_state.ia_auto.apostas:
            lucro_acumulado = []
            lucro_atual = 0
            for aposta in st.session_state.ia_auto.apostas:
                if aposta['status'] == 'finalizada':
                    lucro_atual += aposta['lucro']
                    lucro_acumulado.append(lucro_atual)
            
            if lucro_acumulado:
                df_lucro = pd.DataFrame({
                    'Aposta': range(1, len(lucro_acumulado) + 1),
                    'Lucro Acumulado': lucro_acumulado
                })
                
                fig = px.line(df_lucro, x='Aposta', y='Lucro Acumulado',
                             title='Evolução do Lucro',
                             labels={'Aposta': 'Número da Aposta', 'Lucro Acumulado': 'Lucro (R$)'})
                st.plotly_chart(fig)
        
        st.markdown("### 💡 RECOMENDAÇÕES")
        if estat_apostas['total'] < 10:
            st.info("🔴 **Continue apostando** - Precisa de mais dados para análise")
        elif estat_apostas['taxa_acerto'] > 0.6:
            st.success("🟢 **Excelente desempenho** - Continue com a estratégia atual")
        elif estat_apostas['taxa_acerto'] < 0.45:
            st.warning("🟡 **Ajuste necessário** - Considere revisar a estratégia")
        
        if st.session_state.ia_auto.saldo < 500:
            st.error("🔴 **Saldo baixo** - Considere resetar o sistema")

with tab4:
    st.subheader("🔍 ANÁLISE AVANÇADA")
    
    col_an1, col_an2 = st.columns(2)
    
    with col_an1:
        st.markdown("### 🧠 INTELIGÊNCIA DA IA")
        
        st.markdown("#### 📊 PADRÕES IDENTIFICADOS")
        if st.session_state.ia_auto.padroes_aprendidos:
            st.write(f"**Padrões ativos:** {len(st.session_state.ia_auto.padroes_aprendidos)}")
            
            padroes_consistentes = []
            for padrao, resultados in list(st.session_state.ia_auto.padroes_aprendidos.items())[:8]:
                if len(resultados) >= 3:
                    cor_mais_comum = max(set(resultados), key=resultados.count)
                    prob = resultados.count(cor_mais_comum) / len(resultados)
                    padroes_consistentes.append((padrao, cor_mais_comum, prob, len(resultados)))
            
            padroes_consistentes.sort(key=lambda x: x[2], reverse=True)
            
            for padrao, cor, prob, total in padroes_consistentes[:4]:
                cor_nome = "Vermelho" if cor == 1 else "Preto"
                st.write(f"`{padrao}` → **{cor_nome}** ({prob:.0%} em {total} casos)")
        else:
            st.info("🤔 A IA está aprendendo... Use o sistema para identificar padrões")
        
        st.markdown("#### 🎯 ESTRATÉGIAS ATIVAS")
        st.write("""
        - **🎰 Sequências Longas**: 3+ cores iguais → prevê mudança
        - **🦓 Padrão Zebra**: Alternância constante → prevê continuação  
        - **📊 Análise de Clusters**: Compara períodos diferentes
        - **⚖️ Probabilístico**: Balanceamento natural
        """)
    
    with col_an2:
        st.markdown("### 📈 TENDÊNCIAS")
        
        st.markdown("#### 📋 HISTÓRICO RECENTE")
        previsoes_recentes = st.session_state.ia_auto.previsoes[-10:]
        
        for prev in reversed(previsoes_recentes):
            if prev.get('acertou') is not None:
                cor_emoji = "🔴" if prev['previsao'] == 1 else "⚫"
                resultado = "✅" if prev['acertou'] else "❌"
                st.write(f"{resultado} {cor_emoji} {prev['metodo']} ({prev['confianca']:.0%})")
            else:
                cor_emoji = "🔴" if prev['previsao'] == 1 else "⚫"
                st.write(f"🔄 {cor_emoji} {prev['metodo']} ({prev['confianca']:.0%})")

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<p>⚡ <strong>BLAZE IA AUTO</strong> - Sistema 100% Automático</p>
<p>🟢 Modo Automático: Atualiza a cada 30 segundos • 🔴 Modo Manual: Controle total</p>
</div>
""", unsafe_allow_html=True)

# SALVAR DADOS E ATUALIZAR
try:
    st.session_state.ia_auto.salvar_dados()
except:
    pass

# ATUALIZAÇÃO AUTOMÁTICA
if st.session_state.ia_auto.modo_auto:
    # Usar st.balloons() para indicar atividade (mais discreto que rerun constante)
    time.sleep(1)  # Pequena pausa para evitar sobrecarga
    st.caption(f"🕒 Próxima atualização automática em: {30 - tempo_decorrido:.0f}s | Última: {st.session_state.ia_auto.ultima_atualizacao.strftime('%H:%M:%S')}")
else:
    st.caption(f"🕒 Última atualização: {st.session_state.ia_auto.ultima_atualizacao.strftime('%d/%m/%Y %H:%M:%S')}")

# Atualizar a página automaticamente se estiver no modo auto
if st.session_state.ia_auto.modo_auto and tempo_decorrido > 30:
    st.rerun()
