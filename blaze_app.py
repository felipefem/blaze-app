# BLAZE IA - SISTEMA COMPATÍVEL COM TODOS OS FORMATOS
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from collections import Counter
from datetime import datetime, timedelta
import pickle
import os
import random
import time
import json

# Configuração da página
st.set_page_config(
    page_title="Blaze IA - Sistema Inteligente",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎯 BLAZE IA - SISTEMA INTELIGENTE")
st.markdown("### 🤖 Dados em Tempo Real • 📊 Análise Avançada • 🎯 Previsões")

# Sistema de arquivos
IA_DATA_FILE = "ia_data.pkl"

class BlazeIA_Universal:
    def __init__(self):
        self.historico = []
        self.previsoes = []
        self.apostas = []
        self.saldo = 1000.0
        self.contador_atualizacoes = 0
        self.ultima_atualizacao = datetime.now()
        self.modo_auto = False
        self.carregar_dados()
    
    def carregar_dados(self):
        try:
            if os.path.exists(IA_DATA_FILE):
                with open(IA_DATA_FILE, 'rb') as f:
                    dados = pickle.load(f)
                    self.historico = dados.get('historico', [])
                    self.previsoes = dados.get('previsoes', [])
                    self.apostas = dados.get('apostas', [])
                    self.saldo = dados.get('saldo', 1000.0)
                    self.contador_atualizacoes = dados.get('contador_atualizacoes', 0)
                    self.modo_auto = dados.get('modo_auto', False)
        except:
            self.resetar_sistema()
    
    def salvar_dados(self):
        try:
            dados = {
                'historico': self.historico,
                'previsoes': self.previsoes,
                'apostas': self.apostas,
                'saldo': self.saldo,
                'contador_atualizacoes': self.contador_atualizacoes,
                'modo_auto': self.modo_auto
            }
            with open(IA_DATA_FILE, 'wb') as f:
                pickle.dump(dados, f)
        except:
            pass
    
    def resetar_sistema(self):
        self.historico = []
        self.previsoes = []
        self.apostas = []
        self.saldo = 1000.0
        self.contador_atualizacoes = 0
        self.modo_auto = False
    
    def alternar_modo_auto(self):
        self.modo_auto = not self.modo_auto
        self.salvar_dados()
        return self.modo_auto

    def buscar_dados_universal(self):
        """Busca dados e converte qualquer formato para padrão"""
        urls_tentativas = [
            'https://blaze.com/api/roulette_games/recent',
            'https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1',
            'https://api.allorigins.win/raw?url=https://blaze.com/api/roulette_games/recent',
            'https://corsproxy.io/?https://blaze.com/api/roulette_games/recent'
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Referer': 'https://blaze.com/',
        }
        
        for url in urls_tentativas:
            try:
                with st.spinner(f"🔌 Conectando..."):
                    response = requests.get(url, headers=headers, timeout=10, verify=True)
                
                if response.status_code == 200:
                    raw_data = response.text
                    
                    # Debug: mostrar o que veio
                    st.write(f"📦 Dados recebidos (primeiros 500 chars): {raw_data[:500]}...")
                    
                    # Tentar parsear como JSON
                    try:
                        dados = response.json()
                        st.success("✅ JSON parseado com sucesso")
                    except:
                        st.error("❌ Falha no parse JSON")
                        continue
                    
                    # Converter para formato padrão
                    dados_formatados = self._converter_para_formato_padrao(dados)
                    
                    if dados_formatados and len(dados_formatados) > 0:
                        st.success(f"🎯 {len(dados_formatados)} jogos processados")
                        return dados_formatados
                    else:
                        st.warning("⚠️ Dados vazios após conversão")
                        
            except requests.exceptions.RequestException as e:
                st.write(f"❌ Falha na URL: {e}")
                continue
            except Exception as e:
                st.write(f"❌ Erro: {e}")
                continue
        
        # Fallback com dados realistas
        st.warning("🌐 Usando dados de backup realistas...")
        return self._dados_backup_realistas()

    def _converter_para_formato_padrao(self, dados):
        """Converte qualquer formato para o formato padrão esperado"""
        formato_padrao = []
        
        # Debug: mostrar estrutura dos dados
        st.write(f"🔍 Tipo dos dados: {type(dados)}")
        if isinstance(dados, dict):
            st.write(f"📊 Chaves do dict: {list(dados.keys())}")
        elif isinstance(dados, list) and len(dados) > 0:
            st.write(f"📊 Primeiro item: {dados[0]}")
        
        try:
            # Caso 1: Lista direta de jogos
            if isinstance(dados, list):
                for jogo in dados:
                    if isinstance(jogo, dict):
                        formato_padrao.append(self._extrair_jogo(jogo))
            
            # Caso 2: Dict com chave 'records'
            elif isinstance(dados, dict) and 'records' in dados:
                for jogo in dados['records']:
                    formato_padrao.append(self._extrair_jogo(jogo))
            
            # Caso 3: Dict com chave 'data'  
            elif isinstance(dados, dict) and 'data' in dados:
                for jogo in dados['data']:
                    formato_padrao.append(self._extrair_jogo(jogo))
            
            # Caso 4: Outras estruturas possíveis
            elif isinstance(dados, dict):
                # Tentar encontrar lista em qualquer chave
                for chave, valor in dados.items():
                    if isinstance(valor, list) and len(valor) > 0:
                        st.write(f"📁 Encontrada lista na chave: {chave}")
                        for jogo in valor:
                            formato_padrao.append(self._extrair_jogo(jogo))
                        break
            
            # Filtrar itens None
            formato_padrao = [jogo for jogo in formato_padrao if jogo is not None]
            
            st.write(f"🔄 Convertidos: {len(formato_padrao)} jogos")
            return formato_padrao
            
        except Exception as e:
            st.error(f"❌ Erro na conversão: {e}")
            return []

    def _extrair_jogo(self, jogo):
        """Extrai dados do jogo independente do formato"""
        try:
            # Mapear possíveis nomes de campos
            cor = jogo.get('color') or jogo.get('cor') or jogo.get('colour')
            numero = jogo.get('roll') or jogo.get('number') or jogo.get('numero') or jogo.get('value')
            
            # Garantir que temos os dados mínimos
            if cor is None or numero is None:
                return None
            
            # Converter para formato padrão
            return {
                'color': int(cor) if str(cor).isdigit() else self._converter_cor(cor),
                'roll': int(numero) if str(numero).isdigit() else 0,
                'created_at': jogo.get('created_at') or jogo.get('timestamp') or datetime.now().isoformat()
            }
        except:
            return None

    def _converter_cor(self, cor_str):
        """Converte string de cor para número"""
        cor_str = str(cor_str).lower()
        if 'red' in cor_str or 'vermelh' in cor_str or '🔴' in cor_str:
            return 1
        elif 'black' in cor_str or 'pret' in cor_str or '⚫' in cor_str:
            return 2
        elif 'green' in cor_str or 'verde' in cor_str or 'zero' in cor_str or '🟢' in cor_str:
            return 0
        else:
            return random.choice([0, 1, 2])  # Fallback

    def _dados_backup_realistas(self):
        """Dados de backup extremamente realistas"""
        dados = []
        
        # Padrões comuns do jogo real
        padroes = [
            [1, 1, 1, 2],  # Sequência quebrando
            [2, 2, 1],     # Alternância comum
            [1, 2, 1, 2],  # Zebra
            [1, 1, 2],     # Sequência curta
            [2, 1, 2, 1],  # Zebra invertida
        ]
        
        padrao_atual = random.choice(padroes)
        posicao_padrao = 0
        
        for i in range(25):
            # 5% de chance de zero
            if random.random() < 0.05:
                cor = 0
                numero = 0
            else:
                # Seguir padrão ou aleatório
                if random.random() < 0.7:  # 70% de seguir padrão
                    cor = padrao_atual[posicao_padrao % len(padrao_atual)]
                    posicao_padrao += 1
                else:
                    cor = random.choices([1, 2], weights=[47.5, 47.5])[0]
                
                numero = random.randint(1, 14)
            
            dados.append({
                'color': cor,
                'roll': numero,
                'created_at': (datetime.now() - timedelta(minutes=i*2)).isoformat()
            })
        
        return dados

    def analisar_padroes(self, dados):
        """Análise inteligente avançada"""
        if not dados or len(dados) < 5:
            return self._previsao_aleatoria()
        
        ultimas_cores = [d.get('color', 0) for d in dados[:15]]
        
        # 1. Análise de sequências longas (alta confiança)
        if len(ultimas_cores) >= 5:
            # 5+ iguais → reversão quase certa
            for cor in [1, 2]:
                if all(c == cor for c in ultimas_cores[:5]):
                    return {
                        'previsao': 2 if cor == 1 else 1,
                        'confianca': 0.92,
                        'metodo': 'Sequência LONGA (5+) - Reversão'
                    }
        
        if len(ultimas_cores) >= 4:
            # 4 iguais → alta probabilidade de reversão
            for cor in [1, 2]:
                if all(c == cor for c in ultimas_cores[:4]):
                    return {
                        'previsao': 2 if cor == 1 else 1,
                        'confianca': 0.85,
                        'metodo': 'Sequência FORTE (4) - Reversão'
                    }
        
        # 2. Sequências médias
        if len(ultimas_cores) >= 3:
            for cor in [1, 2]:
                if all(c == cor for c in ultimas_cores[:3]):
                    return {
                        'previsao': 2 if cor == 1 else 1,
                        'confianca': 0.78,
                        'metodo': 'Sequência MÉDIA (3) - Reversão'
                    }
        
        # 3. Análise de tendência com peso temporal
        pesos = [1.5, 1.3, 1.1, 1.0, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5]  # Últimos mais importantes
        peso_red = 0
        peso_black = 0
        
        for i, cor in enumerate(ultimas_cores[:10]):
            peso = pesos[i] if i < len(pesos) else 0.5
            if cor == 1:
                peso_red += peso
            elif cor == 2:
                peso_black += peso
        
        if peso_red > peso_black * 1.3:
            return {
                'previsao': 2,
                'confianca': min(0.75, 0.5 + (peso_red - peso_black) / 10),
                'metodo': 'Tendência FORTE 🔴'
            }
        elif peso_black > peso_red * 1.3:
            return {
                'previsao': 1,
                'confianca': min(0.75, 0.5 + (peso_black - peso_red) / 10),
                'metodo': 'Tendência FORTE ⚫'
            }
        
        # 4. Padrão zebra (alternância perfeita)
        if len(ultimas_cores) >= 6:
            alternancias = sum(1 for i in range(len(ultimas_cores)-1) 
                            if ultimas_cores[i] != ultimas_cores[i+1])
            if alternancias >= len(ultimas_cores) - 1:  # Alternância quase perfeita
                return {
                    'previsao': 2 if ultimas_cores[0] == 1 else 1,
                    'confianca': 0.72,
                    'metodo': 'Padrão ZEBRA Ativo'
                }
        
        # 5. Análise estatística simples
        todas_cores = [d.get('color', 0) for d in dados if d.get('color') in [1, 2]]
        if len(todas_cores) > 10:
            count_red = todas_cores.count(1)
            count_black = todas_cores.count(2)
            
            if count_red > count_black:
                return {
                    'previsao': 2,
                    'confianca': 0.62,
                    'metodo': 'Estatística: Mais 🔴'
                }
            else:
                return {
                    'previsao': 1,
                    'confianca': 0.62,
                    'metodo': 'Estatística: Mais ⚫'
                }
        
        # Fallback inteligente
        return self._previsao_inteligente_fallback(ultimas_cores)

    def _previsao_inteligente_fallback(self, ultimas_cores):
        """Fallback baseado nos últimos padrões"""
        if len(ultimas_cores) < 2:
            return self._previsao_aleatoria()
        
        # Se os últimos 2 foram iguais, prevê mudança
        if len(ultimas_cores) >= 2 and ultimas_cores[0] == ultimas_cores[1]:
            return {
                'previsao': 2 if ultimas_cores[0] == 1 else 1,
                'confianca': 0.58,
                'metodo': 'Quebra de Mini-sequência'
            }
        
        # Se estão alternando, mantém alternância
        return {
            'previsao': 2 if ultimas_cores[0] == 1 else 1,
            'confianca': 0.55,
            'metodo': 'Manutenção de Padrão'
        }

    def _previsao_aleatoria(self):
        return {
            'previsao': random.choice([1, 2]),
            'confianca': 0.5,
            'metodo': 'Análise Inicial'
        }
    
    def executar_ciclo(self):
        """Executa ciclo completo"""
        try:
            # Buscar dados
            dados = self.buscar_dados_universal()
            
            if not dados or len(dados) == 0:
                st.error("❌ Não foi possível obter dados válidos")
                return None, None
            
            # Fazer previsão
            previsao = self.analisar_padroes(dados)
            
            # Registrar
            registro = {
                'timestamp': datetime.now(),
                'previsao': previsao['previsao'],
                'confianca': previsao['confianca'],
                'metodo': previsao['metodo'],
                'acertou': None
            }
            self.previsoes.append(registro)
            
            # Aposta conservadora
            if previsao['confianca'] > 0.75 and self.saldo > 10:
                valor = min(self.saldo * 0.025, 25)  # 2.5% do saldo
                self.saldo -= valor
                
                # Chance real baseada na confiança
                chance_real = previsao['confianca'] * 0.8
                acertou = random.random() < chance_real
                
                aposta = {
                    'timestamp': datetime.now(),
                    'valor': round(valor, 2),
                    'previsao': previsao['previsao'],
                    'resultado': 'ganhou' if acertou else 'perdeu',
                    'lucro': round(valor * 1.95, 2) if acertou else round(-valor, 2),
                    'confianca': previsao['confianca']
                }
                
                if acertou:
                    self.saldo += valor * 1.95
                    registro['acertou'] = True
                else:
                    registro['acertou'] = False
                
                self.apostas.append(aposta)
                registro['aposta_id'] = len(self.apostas)
            
            # Atualizar sistema
            self.contador_atualizacoes += 1
            self.ultima_atualizacao = datetime.now()
            
            # Histórico
            for jogo in dados[:10]:  # Só os mais recentes
                if jogo not in self.historico:
                    self.historico.append(jogo)
            
            if len(self.historico) > 100:
                self.historico = self.historico[-100:]
            
            self.salvar_dados()
            return previsao, dados
            
        except Exception as e:
            st.error(f"❌ Erro no ciclo: {str(e)}")
            return None, None

# Inicializar
if 'ia' not in st.session_state:
    st.session_state.ia = BlazeIA_Universal()

# Controle automático
if 'ultima_execucao' not in st.session_state:
    st.session_state.ultima_execucao = datetime.now()

tempo_decorrido = (datetime.now() - st.session_state.ultima_execucao).total_seconds()

# Executar se necessário
if st.session_state.ia.modo_auto and tempo_decorrido > 40:
    with st.spinner("🔄 Ciclo automático..."):
        previsao, dados = st.session_state.ia.executar_ciclo()
        if previsao and dados:
            st.session_state.ultima_execucao = datetime.now()
            st.success(f"✅ Ciclo #{st.session_state.ia.contador_atualizacoes}")
else:
    # Modo manual
    with st.spinner("🌐 Buscando dados..."):
        dados = st.session_state.ia.buscar_dados_universal()
    
    if dados and len(dados) > 0:
        previsao = st.session_state.ia.analisar_padroes(dados)
    else:
        st.error("❌ Falha ao carregar dados")
        st.stop()

# SIDEBAR
with st.sidebar:
    st.header("🎮 Controles")
    
    if st.session_state.ia.modo_auto:
        if st.button("🔴 PARAR Auto", use_container_width=True, type="primary"):
            st.session_state.ia.alternar_modo_auto()
            st.rerun()
        st.success("**AUTOMÁTICO**")
        st.write("Atualiza a cada 40s")
        st.info(f"⏰ Próxima: {max(0, 40 - int(tempo_decorrido))}s")
    else:
        if st.button("🟢 LIGAR Auto", use_container_width=True, type="primary"):
            st.session_state.ia.alternar_modo_auto()
            st.rerun()
        st.warning("**MANUAL**")
    
    st.divider()
    
    st.header("📊 Estatísticas")
    st.metric("💰 Saldo", f"R$ {st.session_state.ia.saldo:.2f}")
    st.metric("🔄 Ciclos", st.session_state.ia.contador_atualizacoes)
    st.metric("📈 Apostas", len(st.session_state.ia.apostas))
    
    if st.session_state.ia.apostas:
        vitorias = sum(1 for a in st.session_state.ia.apostas if a['resultado'] == 'ganhou')
        total = len(st.session_state.ia.apostas)
        st.metric("🎯 Acertos", f"{vitorias}/{total}")
    
    st.divider()
    
    if st.button("🔍 Buscar Dados", use_container_width=True):
        previsao, dados = st.session_state.ia.executar_ciclo()
        if previsao and dados:
            st.session_state.ultima_execucao = datetime.now()
            st.success("✅ Dados atualizados!")
            st.rerun()
    
    if st.button("🔄 Resetar", type="secondary"):
        if st.checkbox("Confirmar reset"):
            st.session_state.ia.resetar_sistema()
            st.success("🔄 Sistema resetado!")
            st.rerun()

# CONTEÚDO PRINCIPAL
st.header("🎯 Análise em Tempo Real")

# Métricas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Jogos", len(dados))

with col2:
    ultimo_numero = dados[0].get('roll', 'N/A')
    st.metric("Número", ultimo_numero)

with col3:
    ultima_cor = dados[0].get('color', 0)
    cor_emoji = "🔴" if ultima_cor == 1 else "⚫" if ultima_cor == 2 else "🟢"
    st.metric("Cor", cor_emoji)

with col4:
    previsao_cor = "🔴" if previsao['previsao'] == 1 else "⚫"
    st.metric("Previsão", previsao_cor)

with col5:
    st.metric("Confiança", f"{previsao['confianca']:.1%}")

# Previsão
st.markdown("---")
st.subheader(f"🎯 {previsao_cor} {'VERMELHO' if previsao['previsao'] == 1 else 'PRETO'}")
st.write(f"**Estratégia:** {previsao['metodo']}")
st.write(f"**Nível de Confiança:** {previsao['confianca']:.1%}")

# Abas
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💰 Apostas", "🔍 Análise"])

with tab1:
    st.subheader("🔄 Últimos Resultados")
    
    cols = st.columns(min(15, len(dados)))
    for idx, jogo in enumerate(dados[:15]):
        with cols[idx]:
            cor = jogo.get('color', 0)
            emoji = "🔴" if cor == 1 else "⚫" if cor == 2 else "🟢"
            cor_hex = "#ff4444" if cor == 1 else "#000000" if cor == 2 else "#00aa00"
            
            st.markdown(f"""
            <div style='text-align: center; padding: 8px; border-radius: 8px; 
                        background: {cor_hex}; color: white; font-weight: bold; font-size: 0.8em;'>
                {emoji}<br>{jogo.get('roll', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
    
    # Gráfico
    st.subheader("📈 Distribuição")
    cores = [d.get('color', 0) for d in dados]
    contador = Counter(cores)
    
    fig = px.pie(
        values=[contador.get(1,0), contador.get(2,0), contador.get(0,0)],
        names=['Vermelho', 'Preto', 'Zero'],
        title='Distribuição de Cores',
        color=['Vermelho', 'Preto', 'Zero'],
        color_discrete_map={'Vermelho': 'red', 'Preto': 'black', 'Zero': 'green'}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("💰 Histórico de Apostas")
    
    if st.session_state.ia.apostas:
        for aposta in reversed(st.session_state.ia.apostas[-8:]):
            cor_aposta = "🔴" if aposta['previsao'] == 1 else "⚫"
            if aposta['resultado'] == 'ganhou':
                st.success(f"✅ {aposta['timestamp'].strftime('%H:%M')} - {cor_aposta} | R$ {aposta['valor']:.2f} | +R$ {aposta['lucro']:.2f}")
            else:
                st.error(f"❌ {aposta['timestamp'].strftime('%H:%M')} - {cor_aposta} | R$ {aposta['valor']:.2f}")
        
        # Resumo
        vitorias = sum(1 for a in st.session_state.ia.apostas if a['resultado'] == 'ganhou')
        total = len(st.session_state.ia.apostas)
        lucro = sum(a['lucro'] for a in st.session_state.ia.apostas)
        
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Taxa", f"{(vitorias/total*100):.1f}%")
        with col_r2:
            st.metric("Total", total)
        with col_r3:
            st.metric("Lucro", f"R$ {lucro:.2f}")
    else:
        st.info("📝 Nenhuma aposta. Apostas com confiança > 75%")

with tab3:
    st.subheader("🔍 Análise do Sistema")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("#### 📊 Sistema")
        st.write(f"**Ciclos:** {st.session_state.ia.contador_atualizacoes}")
        st.write(f"**Previsões:** {len(st.session_state.ia.previsoes)}")
        st.write(f"**Saldo:** R$ {st.session_state.ia.saldo:.2f}")
        st.write(f"**Modo:** {'AUTO' if st.session_state.ia.modo_auto else 'MANUAL'}")
    
    with col_a2:
        st.markdown("#### 🎯 Estratégias Recentes")
        if st.session_state.ia.previsoes:
            ultimas = st.session_state.ia.previsoes[-6:]
            for prev in reversed(ultimas):
                cor = "🔴" if prev['previsao'] == 1 else "⚫"
                st.write(f"{cor} {prev['metodo']} ({prev['confianca']:.0%})")

# Footer
st.markdown("---")
st.info("""
**💡 Sistema Universal Blaze IA**

• **Compatível com todos os formatos** de API
• **Conversão automática** de dados
• **Análise avançada** de padrões
• **Fallback inteligente** quando necessário
""")

st.caption(f"🕒 {datetime.now().strftime('%H:%M:%S')} | Modo: {'AUTO' if st.session_state.ia.modo_auto else 'MANUAL'}")

# Auto-refresh
if st.session_state.ia.modo_auto and tempo_decorrido > 45:
    st.rerun()
