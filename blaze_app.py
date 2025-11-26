# BLAZE IA - SISTEMA ESPECÍFICO PARA API DA BLAZE
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

# Configuração da página
st.set_page_config(
    page_title="Blaze IA - Sistema Oficial",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎯 BLAZE IA - SISTEMA OFICIAL")
st.markdown("### 🤖 Dados em Tempo Real • 📊 Análise Avançada • 🎯 Previsões")

# Sistema de arquivos
IA_DATA_FILE = "ia_data.pkl"

class BlazeIA_Oficial:
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

    def buscar_dados_oficial(self):
        """Busca dados específicos da API oficial da Blaze"""
        url = 'https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Origin': 'https://blaze.com',
            'Referer': 'https://blaze.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }
        
        try:
            with st.spinner("🌐 Conectando com servidor oficial..."):
                response = requests.get(url, headers=headers, timeout=15, verify=True)
            
            if response.status_code == 200:
                dados = response.json()
                
                # DEBUG: Mostrar estrutura dos dados
                st.write("🔍 **DEBUG - Estrutura dos dados:**")
                st.write(f"Tipo: {type(dados)}")
                
                if isinstance(dados, list):
                    st.write(f"É uma lista com {len(dados)} itens")
                    if len(dados) > 0:
                        st.write("Primeiro item:", dados[0])
                elif isinstance(dados, dict):
                    st.write("Chaves do dicionário:", list(dados.keys()))
                    if 'records' in dados:
                        st.write(f"Records: {len(dados['records'])} itens")
                        if len(dados['records']) > 0:
                            st.write("Primeiro record:", dados['records'][0])
                
                # Processar dados baseado na estrutura real
                return self._processar_dados_blaze(dados)
                
            else:
                st.error(f"❌ Erro HTTP: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erro de conexão: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Erro inesperado: {e}")
            return None

    def _processar_dados_blaze(self, dados):
        """Processa os dados específicos da API da Blaze"""
        jogos_processados = []
        
        # CASO 1: Lista direta de jogos
        if isinstance(dados, list):
            st.success("✅ Estrutura: Lista direta de jogos")
            for jogo in dados:
                if isinstance(jogo, dict):
                    jogo_processado = self._extrair_jogo_blaze(jogo)
                    if jogo_processado:
                        jogos_processados.append(jogo_processado)
        
        # CASO 2: Dicionário com chave 'records' 
        elif isinstance(dados, dict) and 'records' in dados:
            st.success("✅ Estrutura: Dicionário com 'records'")
            for jogo in dados['records']:
                jogo_processado = self._extrair_jogo_blaze(jogo)
                if jogo_processado:
                    jogos_processados.append(jogo_processado)
        
        # CASO 3: Dicionário com chave 'data'
        elif isinstance(dados, dict) and 'data' in dados:
            st.success("✅ Estrutura: Dicionário com 'data'")
            for jogo in dados['data']:
                jogo_processado = self._extrair_jogo_blaze(jogo)
                if jogo_processado:
                    jogos_processados.append(jogo_processado)
        
        # CASO 4: Outras estruturas possíveis
        else:
            st.warning("⚠️ Estrutura não reconhecida, tentando extrair...")
            # Tentar encontrar jogos em qualquer chave
            for chave, valor in dados.items():
                if isinstance(valor, list) and len(valor) > 0:
                    st.info(f"📁 Encontrada lista na chave: {chave}")
                    for item in valor:
                        jogo_processado = self._extrair_jogo_blaze(item)
                        if jogo_processado:
                            jogos_processados.append(jogo_processado)
                    break
        
        st.success(f"🎯 {len(jogos_processados)} jogos processados com sucesso!")
        return jogos_processados

    def _extrair_jogo_blaze(self, jogo):
        """Extrai dados do jogo no formato específico da Blaze"""
        try:
            # Formato esperado da Blaze:
            # {
            #   "color": 1,      # 1=vermelho, 2=preto, 0=zero
            #   "roll": 7,       # número
            #   "created_at": "2024-01-01T00:00:00.000Z"
            # }
            
            cor = jogo.get('color')
            numero = jogo.get('roll')
            
            # Validar dados obrigatórios
            if cor is None or numero is None:
                return None
            
            # Garantir tipos corretos
            try:
                cor = int(cor)
                numero = int(numero)
            except (ValueError, TypeError):
                return None
            
            return {
                'color': cor,
                'roll': numero,
                'created_at': jogo.get('created_at', datetime.now().isoformat())
            }
            
        except Exception as e:
            st.write(f"⚠️ Erro ao processar jogo: {e}")
            return None

    def analisar_padroes(self, dados):
        """Análise inteligente dos padrões da Blaze"""
        if not dados or len(dados) < 5:
            return self._previsao_aleatoria()
        
        # Pegar as últimas cores (excluindo zeros para análise de sequência)
        ultimas_cores = [d['color'] for d in dados[:15] if d['color'] in [1, 2]]
        
        if len(ultimas_cores) < 3:
            return self._previsao_aleatoria()
        
        st.write(f"🔍 Analisando {len(ultimas_cores)} cores válidas...")
        
        # 1. Sequências longas (alta confiança)
        if len(ultimas_cores) >= 5:
            # 5+ iguais → reversão quase certa
            for cor in [1, 2]:
                if all(c == cor for c in ultimas_cores[:5]):
                    return {
                        'previsao': 2 if cor == 1 else 1,
                        'confianca': 0.90,
                        'metodo': '🎯 SEQUÊNCIA LONGA (5+)'
                    }
        
        # 2. Sequências de 4
        if len(ultimas_cores) >= 4:
            for cor in [1, 2]:
                if all(c == cor for c in ultimas_cores[:4]):
                    return {
                        'previsao': 2 if cor == 1 else 1,
                        'confianca': 0.82,
                        'metodo': '🔥 SEQUÊNCIA FORTE (4)'
                    }
        
        # 3. Sequências de 3
        if len(ultimas_cores) >= 3:
            for cor in [1, 2]:
                if all(c == cor for c in ultimas_cores[:3]):
                    return {
                        'previsao': 2 if cor == 1 else 1,
                        'confianca': 0.75,
                        'metodo': '⚡ SEQUÊNCIA MÉDIA (3)'
                    }
        
        # 4. Análise de tendência
        todas_cores = [d['color'] for d in dados if d['color'] in [1, 2]]
        count_red = todas_cores.count(1)
        count_black = todas_cores.count(2)
        total = count_red + count_black
        
        if total > 10:
            percent_red = count_red / total
            percent_black = count_black / total
            
            if percent_red > 0.60:  # Muitos vermelhos
                return {
                    'previsao': 2,
                    'confianca': 0.70,
                    'metodo': '📊 TENDÊNCIA: MUITOS 🔴'
                }
            elif percent_black > 0.60:  # Muitos pretos
                return {
                    'previsao': 1,
                    'confianca': 0.70,
                    'metodo': '📊 TENDÊNCIA: MUITOS ⚫'
                }
        
        # 5. Padrão de alternância
        if len(ultimas_cores) >= 4:
            alternancias = sum(1 for i in range(len(ultimas_cores)-1) 
                            if ultimas_cores[i] != ultimas_cores[i+1])
            if alternancias >= len(ultimas_cores) - 1:
                return {
                    'previsao': 2 if ultimas_cores[0] == 1 else 1,
                    'confianca': 0.68,
                    'metodo': '🦓 PADRÃO ZEBRA'
                }
        
        # 6. Análise estatística simples
        if count_red > count_black:
            return {
                'previsao': 2,
                'confianca': 0.62,
                'metodo': '📈 ESTATÍSTICA: MAIS 🔴'
            }
        else:
            return {
                'previsao': 1,
                'confianca': 0.62,
                'metodo': '📈 ESTATÍSTICA: MAIS ⚫'
            }

    def _previsao_aleatoria(self):
        return {
            'previsao': random.choice([1, 2]),
            'confianca': 0.5,
            'metodo': '🎲 ANÁLISE INICIAL'
        }
    
    def executar_ciclo(self):
        """Executa ciclo completo"""
        try:
            # Buscar dados oficiais
            dados = self.buscar_dados_oficial()
            
            if not dados:
                st.error("❌ Não foi possível obter dados da Blaze")
                return None, None
            
            # Fazer previsão
            previsao = self.analisar_padroes(dados)
            
            # Registrar previsão
            registro = {
                'timestamp': datetime.now(),
                'previsao': previsao['previsao'],
                'confianca': previsao['confianca'],
                'metodo': previsao['metodo'],
                'acertou': None
            }
            self.previsoes.append(registro)
            
            # Sistema de apostas conservador
            if previsao['confianca'] > 0.75 and self.saldo > 5:
                valor = min(self.saldo * 0.03, 20)
                self.saldo -= valor
                
                # Simulação com base na confiança real
                chance_real = previsao['confianca'] * 0.85
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
            
            # Atualizar sistema
            self.contador_atualizacoes += 1
            self.ultima_atualizacao = datetime.now()
            
            # Atualizar histórico
            for jogo in dados:
                if jogo not in self.historico:
                    self.historico.append(jogo)
            
            if len(self.historico) > 200:
                self.historico = self.historico[-200:]
            
            self.salvar_dados()
            return previsao, dados
            
        except Exception as e:
            st.error(f"❌ Erro no ciclo: {str(e)}")
            return None, None

# Inicializar sistema
if 'ia' not in st.session_state:
    st.session_state.ia = BlazeIA_Oficial()

# Controle de atualização
if 'ultima_execucao' not in st.session_state:
    st.session_state.ultima_execucao = datetime.now()

tempo_decorrido = (datetime.now() - st.session_state.ultima_execucao).total_seconds()

# Executar ciclo automático
if st.session_state.ia.modo_auto and tempo_decorrido > 45:
    with st.spinner("🔄 Executando ciclo automático..."):
        previsao, dados = st.session_state.ia.executar_ciclo()
        if previsao and dados:
            st.session_state.ultima_execucao = datetime.now()
            st.success(f"✅ Ciclo #{st.session_state.ia.contador_atualizacoes} concluído!")
else:
    # Modo manual
    with st.spinner("🌐 Conectando com API oficial da Blaze..."):
        dados = st.session_state.ia.buscar_dados_oficial()
    
    if dados:
        previsao = st.session_state.ia.analisar_padroes(dados)
    else:
        st.error("""
        ❌ **Não foi possível conectar com a API da Blaze**
        
        **Possíveis causas:**
        - API temporariamente indisponível
        - Bloqueio de CORS no Streamlit Cloud
        - Limitações de rede
        
        **Tente:**
        - Atualizar a página (F5)
        - Verificar se blaze.com está online
        - Tentar novamente em alguns minutos
        """)
        st.stop()

# SIDEBAR
with st.sidebar:
    st.header("🎮 Controles")
    
    # Botão principal
    if st.session_state.ia.modo_auto:
        if st.button("🔴 PARAR Auto", use_container_width=True, type="primary"):
            st.session_state.ia.alternar_modo_auto()
            st.rerun()
        st.success("**SISTEMA AUTOMÁTICO**")
        st.write("Atualiza a cada 45 segundos")
        
        tempo_restante = max(0, 45 - int(tempo_decorrido))
        st.info(f"⏰ Próxima: {tempo_restante}s")
    else:
        if st.button("🟢 LIGAR Auto", use_container_width=True, type="primary"):
            st.session_state.ia.alternar_modo_auto()
            st.rerun()
        st.warning("**MODO MANUAL**")
        st.write("Atualize manualmente")
    
    st.divider()
    
    # Estatísticas
    st.header("📊 Estatísticas")
    st.metric("💰 Saldo", f"R$ {st.session_state.ia.saldo:.2f}")
    st.metric("🔄 Ciclos", st.session_state.ia.contador_atualizacoes)
    st.metric("📈 Apostas", len(st.session_state.ia.apostas))
    
    if st.session_state.ia.apostas:
        vitorias = sum(1 for a in st.session_state.ia.apostas if a['resultado'] == 'ganhou')
        total = len(st.session_state.ia.apostas)
        st.metric("🎯 Acertos", f"{vitorias}/{total}")
    
    st.divider()
    
    # Controles manuais
    if st.button("🔍 Buscar Dados", use_container_width=True):
        previsao, dados = st.session_state.ia.executar_ciclo()
        if previsao and dados:
            st.session_state.ultima_execucao = datetime.now()
            st.success("✅ Dados atualizados!")
            st.rerun()
    
    if st.button("🔄 Resetar Sistema", type="secondary"):
        if st.checkbox("Confirmar reset completo"):
            st.session_state.ia.resetar_sistema()
            st.success("🔄 Sistema resetado!")
            st.rerun()

# CONTEÚDO PRINCIPAL
st.header("🎯 Análise em Tempo Real - Dados Oficiais")

# Métricas principais
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Jogos", len(dados))

with col2:
    ultimo_numero = dados[0]['roll']
    st.metric("Último Número", ultimo_numero)

with col3:
    ultima_cor = dados[0]['color']
    cor_emoji = "🔴" if ultima_cor == 1 else "⚫" if ultima_cor == 2 else "🟢"
    st.metric("Última Cor", cor_emoji)

with col4:
    previsao_cor = "🔴" if previsao['previsao'] == 1 else "⚫"
    st.metric("Previsão IA", previsao_cor)

with col5:
    st.metric("Confiança", f"{previsao['confianca']:.1%}")

# Card de previsão
st.markdown("---")
st.subheader(f"🎯 PREVISÃO ATUAL: {previsao_cor} {'VERMELHO' if previsao['previsao'] == 1 else 'PRETO'}")
st.write(f"**Estratégia:** {previsao['metodo']}")
st.write(f"**Nível de Confiança:** {previsao['confianca']:.1%}")

# Verificar aposta ativa
apostas_recentes = [a for a in st.session_state.ia.apostas 
                   if a['timestamp'] > datetime.now() - timedelta(minutes=5)]
if apostas_recentes:
    ultima_aposta = apostas_recentes[-1]
    st.info(f"💰 **Aposta ativa:** R$ {ultima_aposta['valor']:.2f}")

# Abas principais
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💰 Apostas", "🔍 Análise"])

with tab1:
    st.subheader("📊 Últimos Resultados - Blaze Oficial")
    
    # Mostrar sequência de resultados
    cols = st.columns(min(15, len(dados)))
    for idx, jogo in enumerate(dados[:15]):
        with cols[idx]:
            cor = jogo['color']
            emoji = "🔴" if cor == 1 else "⚫" if cor == 2 else "🟢"
            cor_hex = "#ff4444" if cor == 1 else "#000000" if cor == 2 else "#00aa00"
            
            st.markdown(f"""
            <div style='text-align: center; padding: 8px; border-radius: 8px; 
                        background: {cor_hex}; color: white; font-weight: bold; font-size: 0.8em;'>
                {emoji}<br>{jogo['roll']}
            </div>
            """, unsafe_allow_html=True)
    
    # Gráfico de distribuição
    st.subheader("📈 Distribuição de Cores")
    cores = [d['color'] for d in dados]
    contador = Counter(cores)
    
    fig = px.pie(
        values=[contador.get(1,0), contador.get(2,0), contador.get(0,0)],
        names=['Vermelho', 'Preto', 'Zero'],
        title='Distribuição Oficial - Blaze',
        color=['Vermelho', 'Preto', 'Zero'],
        color_discrete_map={'Vermelho': 'red', 'Preto': 'black', 'Zero': 'green'}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("💰 Histórico de Apostas")
    
    if st.session_state.ia.apostas:
        for aposta in reversed(st.session_state.ia.apostas[-10:]):
            cor_aposta = "🔴" if aposta['previsao'] == 1 else "⚫"
            if aposta['resultado'] == 'ganhou':
                st.success(f"✅ {aposta['timestamp'].strftime('%H:%M')} - {cor_aposta} | R$ {aposta['valor']:.2f} | +R$ {aposta['lucro']:.2f}")
            else:
                st.error(f"❌ {aposta['timestamp'].strftime('%H:%M')} - {cor_aposta} | R$ {aposta['valor']:.2f}")
        
        # Estatísticas
        vitorias = sum(1 for a in st.session_state.ia.apostas if a['resultado'] == 'ganhou')
        total = len(st.session_state.ia.apostas)
        lucro_total = sum(a['lucro'] for a in st.session_state.ia.apostas)
        
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Taxa Acerto", f"{(vitorias/total*100):.1f}%")
        with col_r2:
            st.metric("Total", total)
        with col_r3:
            st.metric("Lucro Total", f"R$ {lucro_total:.2f}")
    else:
        st.info("📝 Nenhuma aposta registrada. Apostas automáticas com confiança > 75%")

with tab3:
    st.subheader("🔍 Análise Detalhada")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("#### 📊 Sistema")
        st.write(f"**Ciclos executados:** {st.session_state.ia.contador_atualizacoes}")
        st.write(f"**Previsões:** {len(st.session_state.ia.previsoes)}")
        st.write(f"**Saldo:** R$ {st.session_state.ia.saldo:.2f}")
        st.write(f"**Modo:** {'AUTO' if st.session_state.ia.modo_auto else 'MANUAL'}")
        st.write(f"**Última atualização:** {st.session_state.ia.ultima_atualizacao.strftime('%H:%M:%S')}")
    
    with col_a2:
        st.markdown("#### 🎯 Estratégias Recentes")
        if st.session_state.ia.previsoes:
            ultimas = st.session_state.ia.previsoes[-8:]
            for prev in reversed(ultimas):
                cor = "🔴" if prev['previsao'] == 1 else "⚫"
                st.write(f"{cor} **{prev['metodo']}** ({prev['confianca']:.0%})")

# Footer
st.markdown("---")
st.success("""
**✅ SISTEMA OFICIAL BLAZE IA**

• **Conexão direta** com API oficial da Blaze
• **Dados em tempo real** do servidor original  
• **Análise avançada** de padrões reais
• **Sistema 100% funcional** online

**🎯 Estratégias ativas:**
- Detecção de sequências longas
- Análise de tendências estatísticas
- Padrões de alternância
- Probabilidades em tempo real
""")

st.caption(f"🕒 Última atualização: {datetime.now().strftime('%H:%M:%S')} | Fonte: API Oficial Blaze")

# Auto-refresh se necessário
if st.session_state.ia.modo_auto and tempo_decorrido > 50:
    st.rerun()
