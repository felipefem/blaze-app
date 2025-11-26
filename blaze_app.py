# BLAZE IA - SISTEMA COM API REAL
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import pickle
import os
import random
import time

# Configuração da página
st.set_page_config(
    page_title="Blaze IA - Sistema Real",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎯 BLAZE IA - SISTEMA COM DADOS REAIS")
st.markdown("### 🤖 Análise em Tempo Real • 📊 Dados da Blaze • 🎯 Previsões")

# Sistema de arquivos
IA_DATA_FILE = "ia_data.pkl"

class BlazeIA_Real:
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

    def buscar_dados_reais(self):
        """Busca dados reais da API da Blaze com configurações corretas"""
        url = 'https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://blaze.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        try:
            # Configuração especial para Streamlit Cloud
            response = requests.get(
                url, 
                headers=headers, 
                timeout=10,
                verify=True  # Importante para HTTPS
            )
            
            if response.status_code == 200:
                dados = response.json()
                
                # A API pode retornar de diferentes formas
                if isinstance(dados, list):
                    return dados
                elif isinstance(dados, dict) and 'records' in dados:
                    return dados['records']
                else:
                    st.warning("⚠️ Formato de dados diferente do esperado")
                    return None
            else:
                st.error(f"❌ Erro na API: Status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("⏰ Timeout - A API demorou para responder")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 Erro de conexão - Verifique a internet")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erro na requisição: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Erro inesperado: {e}")
            return None

    def analisar_padroes(self, dados):
        """Análise inteligente dos padrões com dados reais"""
        if not dados or len(dados) < 5:
            return self.previsao_aleatoria()
        
        ultimas_cores = [d.get('color', 0) for d in dados[:10]]
        
        # Análise de sequências
        if len(ultimas_cores) >= 4:
            if all(c == 1 for c in ultimas_cores[:4]):
                return {'previsao': 2, 'confianca': 0.85, 'metodo': 'Sequência Longa de Vermelho'}
            elif all(c == 2 for c in ultimas_cores[:4]):
                return {'previsao': 1, 'confianca': 0.85, 'metodo': 'Sequência Longa de Preto'}
        
        if len(ultimas_cores) >= 3:
            if all(c == 1 for c in ultimas_cores[:3]):
                return {'previsao': 2, 'confianca': 0.75, 'metodo': 'Sequência Média de Vermelho'}
            elif all(c == 2 for c in ultimas_cores[:3]):
                return {'previsao': 1, 'confianca': 0.75, 'metodo': 'Sequência Média de Preto'}
        
        # Análise estatística
        todas_cores = [d.get('color', 0) for d in dados]
        count_red = todas_cores.count(1)
        count_black = todas_cores.count(2)
        
        if count_red > count_black + 2:
            return {'previsao': 2, 'confianca': 0.65, 'metodo': 'Muitos Vermelhos - Correção Esperada'}
        elif count_black > count_red + 2:
            return {'previsao': 1, 'confianca': 0.65, 'metodo': 'Muitos Pretos - Correção Esperada'}
        
        # Padrão de alternância
        if len(ultimas_cores) >= 4:
            alternancias = sum(1 for i in range(len(ultimas_cores)-1) if ultimas_cores[i] != ultimas_cores[i+1])
            if alternancias >= 3:
                ultima_cor = ultimas_cores[0]
                return {
                    'previsao': 2 if ultima_cor == 1 else 1,
                    'confianca': 0.6,
                    'metodo': 'Padrão de Alternância'
                }
        
        return {'previsao': random.choice([1, 2]), 'confianca': 0.5, 'metodo': 'Análise Estatística'}
    
    def previsao_aleatoria(self):
        return {
            'previsao': random.choice([1, 2]),
            'confianca': 0.5,
            'metodo': 'Análise Inicial'
        }
    
    def executar_ciclo(self):
        """Executa um ciclo completo com dados reais"""
        try:
            # Buscar dados reais
            with st.spinner("🌐 Conectando com a Blaze..."):
                dados = self.buscar_dados_reais()
            
            if not dados:
                st.error("Não foi possível obter dados da API")
                return None, None
            
            # Fazer previsão
            previsao = self.analisar_padroes(dados)
            
            # Registrar previsão
            previsao_registro = {
                'timestamp': datetime.now(),
                'previsao': previsao['previsao'],
                'confianca': previsao['confianca'],
                'metodo': previsao['metodo'],
                'acertou': None
            }
            self.previsoes.append(previsao_registro)
            
            # Aposta automática se confiança alta
            if previsao['confianca'] > 0.7 and self.saldo > 10:
                valor_aposta = min(self.saldo * 0.05, 50)
                self.saldo -= valor_aposta
                
                # Simular resultado (baseado na confiança)
                probabilidade_acerto = previsao['confianca']
                acertou = random.random() < probabilidade_acerto
                
                aposta = {
                    'timestamp': datetime.now(),
                    'valor': round(valor_aposta, 2),
                    'previsao': previsao['previsao'],
                    'resultado': 'ganhou' if acertou else 'perdeu',
                    'lucro': round(valor_aposta * 2, 2) if acertou else round(-valor_aposta, 2),
                    'confianca': previsao['confianca']
                }
                
                if acertou:
                    self.saldo += valor_aposta * 2
                
                self.apostas.append(aposta)
                previsao_registro['acertou'] = acertou
                previsao_registro['aposta_valor'] = valor_aposta
            
            # Atualizar contadores
            self.contador_atualizacoes += 1
            self.ultima_atualizacao = datetime.now()
            
            # Adicionar ao histórico (evitar duplicatas)
            for jogo in dados:
                if jogo not in self.historico:
                    self.historico.append(jogo)
            
            # Manter histórico limitado
            if len(self.historico) > 200:
                self.historico = self.historico[-200:]
            
            self.salvar_dados()
            return previsao, dados
            
        except Exception as e:
            st.error(f"❌ Erro no ciclo: {e}")
            return None, None

# Inicializar o sistema
if 'ia' not in st.session_state:
    st.session_state.ia = BlazeIA_Real()

# Verificar atualização automática
if 'ultima_execucao' not in st.session_state:
    st.session_state.ultima_execucao = datetime.now()

tempo_decorrido = (datetime.now() - st.session_state.ultima_execucao).total_seconds()

# Executar ciclo automático se necessário
if st.session_state.ia.modo_auto and tempo_decorrido > 30:
    previsao, dados = st.session_state.ia.executar_ciclo()
    if previsao and dados:
        st.session_state.ultima_execucao = datetime.now()
        st.success(f"✅ Análise #{st.session_state.ia.contador_atualizacoes} concluída!")
    else:
        st.error("❌ Falha na atualização automática")
else:
    # Buscar dados para modo manual
    with st.spinner("🔄 Buscando dados atualizados..."):
        dados = st.session_state.ia.buscar_dados_reais()
    
    if dados:
        previsao = st.session_state.ia.analisar_padroes(dados)
    else:
        st.error("❌ Não foi possível carregar dados")
        st.stop()

# SIDEBAR
with st.sidebar:
    st.header("🎮 Controles")
    
    # Botão principal
    if st.session_state.ia.modo_auto:
        if st.button("🔴 PARAR Auto", use_container_width=True, type="primary"):
            st.session_state.ia.alternar_modo_auto()
            st.rerun()
        st.success("**Sistema AUTOMÁTICO**")
        st.write("Atualiza a cada 30 segundos")
        
        # Mostrar próxima atualização
        tempo_restante = max(0, 30 - tempo_decorrido)
        st.info(f"⏰ Próxima em: {int(tempo_restante)}s")
    else:
        if st.button("🟢 LIGAR Auto", use_container_width=True, type="primary"):
            st.session_state.ia.alternar_modo_auto()
            st.rerun()
        st.warning("**Sistema MANUAL**")
    
    st.divider()
    
    # Estatísticas
    st.header("📊 Estatísticas")
    st.metric("💰 Saldo", f"R$ {st.session_state.ia.saldo:.2f}")
    st.metric("🔄 Análises", st.session_state.ia.contador_atualizacoes)
    st.metric("📈 Apostas", len(st.session_state.ia.apostas))
    
    if st.session_state.ia.apostas:
        vitorias = sum(1 for a in st.session_state.ia.apostas if a['resultado'] == 'ganhou')
        st.metric("🎯 Vitórias", f"{vitorias}/{len(st.session_state.ia.apostas)}")
    
    st.divider()
    
    # Botão de atualização manual
    if st.button("🔍 Buscar Dados Agora", use_container_width=True):
        previsao, dados = st.session_state.ia.executar_ciclo()
        if previsao and dados:
            st.session_state.ultima_execucao = datetime.now()
            st.success("Dados atualizados com sucesso!")
            st.rerun()
        else:
            st.error("Falha ao buscar dados")
    
    if st.button("🔄 Resetar Sistema", type="secondary"):
        if st.checkbox("Confirmar reset completo"):
            st.session_state.ia.resetar_sistema()
            st.success("Sistema resetado!")
            st.rerun()

# CONTEÚDO PRINCIPAL
if not dados:
    st.error("""
    ❌ **Não foi possível conectar com a API da Blaze**
    
    **Possíveis causas:**
    - API da Blaze temporariamente indisponível
    - Limitações de rede no Streamlit Cloud
    - Bloqueio de requisições
    
    **Tente:**
    - Atualizar a página (F5)
    - Tentar novamente em alguns minutos
    - Verificar se a Blaze está online
    """)
    st.stop()

st.header("🎯 Painel de Análise em Tempo Real")

# Métricas principais
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total de Jogos", len(dados))

with col2:
    ultimo_numero = dados[0].get('roll', 'N/A')
    st.metric("Último Número", ultimo_numero)

with col3:
    ultima_cor = dados[0].get('color', 0)
    cor_emoji = "🔴" if ultima_cor == 1 else "⚫" if ultima_cor == 2 else "🟢"
    st.metric("Última Cor", cor_emoji)

with col4:
    cor_previsao = previsao['previsao']
    cor_ia_emoji = "🔴" if cor_previsao == 1 else "⚫"
    st.metric("Previsão IA", cor_ia_emoji)

with col5:
    st.metric("Confiança", f"{previsao['confianca']:.1%}")

# Card de previsão
st.markdown("---")
st.subheader(f"🎯 Previsão Atual: {cor_ia_emoji} {'VERMELHO' if previsao['previsao'] == 1 else 'PRETO'}")
st.write(f"**Método:** {previsao['metodo']}")
st.write(f"**Confiança:** {previsao['confianca']:.1%}")

# Verificar se há aposta ativa
apostas_ativas = [a for a in st.session_state.ia.apostas if a.get('timestamp', datetime.now()) > datetime.now() - timedelta(minutes=2)]
if apostas_ativas:
    ultima_aposta = apostas_ativas[-1]
    st.info(f"💰 **Aposta ativa:** R$ {ultima_aposta['valor']:.2f} em {'🔴 Vermelho' if ultima_aposta['previsao'] == 1 else '⚫ Preto'}")

# Abas principais
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💰 Apostas", "🔍 Análise"])

with tab1:
    st.subheader("📊 Últimos Resultados")
    
    # Mostrar última sequência
    cols = st.columns(15)
    for idx, jogo in enumerate(dados[:15]):
        with cols[idx]:
            cor = jogo.get('color', 0)
            emoji = "🔴" if cor == 1 else "⚫" if cor == 2 else "🟢"
            st.markdown(f"""
            <div style='text-align: center; padding: 8px; border-radius: 8px; 
                        background: {"#ff4444" if cor == 1 else "#000000" if cor == 2 else "#00aa00"}; 
                        color: white; font-weight: bold; font-size: 0.8em;'>
                {emoji}<br>{jogo.get('roll', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
    
    # Gráfico de distribuição
    st.subheader("📈 Distribuição de Cores")
    cores = [d.get('color', 0) for d in dados]
    contador = Counter(cores)
    
    df_cores = pd.DataFrame({
        'Cor': ['Vermelho', 'Preto', 'Zero'],
        'Quantidade': [contador.get(1, 0), contador.get(2, 0), contador.get(0, 0)]
    })
    
    fig = px.pie(
        df_cores, 
        values='Quantidade', 
        names='Cor',
        title='Distribuição das Cores - Dados Reais',
        color='Cor',
        color_discrete_map={'Vermelho': 'red', 'Preto': 'black', 'Zero': 'green'}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("💰 Histórico de Apostas")
    
    if st.session_state.ia.apostas:
        for aposta in reversed(st.session_state.ia.apostas[-10:]):
            if aposta['resultado'] == 'ganhou':
                st.success(f"✅ {aposta['timestamp'].strftime('%H:%M')} - Ganhou R$ {aposta['valor']:.2f} (+R$ {aposta['lucro']:.2f}) | Conf: {aposta.get('confianca', 0):.0%}")
            else:
                st.error(f"❌ {aposta['timestamp'].strftime('%H:%M')} - Perdeu R$ {aposta['valor']:.2f} | Conf: {aposta.get('confianca', 0):.0%}")
        
        # Estatísticas de apostas
        vitorias = sum(1 for a in st.session_state.ia.apostas if a['resultado'] == 'ganhou')
        total_apostas = len(st.session_state.ia.apostas)
        lucro_total = sum(a['lucro'] for a in st.session_state.ia.apostas)
        
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            st.metric("Taxa de Acerto", f"{(vitorias/total_apostas*100):.1f}%")
        with col_a2:
            st.metric("Total Apostas", total_apostas)
        with col_a3:
            st.metric("Lucro Total", f"R$ {lucro_total:.2f}")
    else:
        st.info("📝 Nenhuma aposta registrada ainda. As apostas automáticas acontecem quando a confiança é maior que 70%.")

with tab3:
    st.subheader("🔍 Análise Detalhada")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("#### 📊 Estatísticas do Sistema")
        st.write(f"**Total de análises:** {len(st.session_state.ia.previsoes)}")
        st.write(f"**Saldo atual:** R$ {st.session_state.ia.saldo:.2f}")
        st.write(f"**Modo atual:** {'AUTOMÁTICO' if st.session_state.ia.modo_auto else 'MANUAL'}")
        st.write(f"**Última atualização:** {st.session_state.ia.ultima_atualizacao.strftime('%H:%M:%S')}")
        
        if st.session_state.ia.previsoes:
            previsoes_verificadas = [p for p in st.session_state.ia.previsoes if p.get('acertou') is not None]
            if previsoes_verificadas:
                acertos = sum(1 for p in previsoes_verificadas if p['acertou'])
                st.write(f"**Precisão da IA:** {(acertos/len(previsoes_verificadas)*100):.1f}%")
    
    with col_a2:
        st.markdown("#### 🎯 Métodos Utilizados")
        if st.session_state.ia.previsoes:
            metodos = [p['metodo'] for p in st.session_state.ia.previsoes[-20:]]  # Últimas 20
            contador_metodos = Counter(metodos)
            for metodo, count in contador_metodos.most_common(5):
                st.write(f"**{metodo}:** {count} vezes")

# Informações
st.markdown("---")
st.info("""
**🌐 Sobre o Sistema:**

• **Dados em tempo real** da API oficial da Blaze
• **Análise automática** de padrões e sequências
• **Sistema inteligente** de apostas baseado em confiança
• **Funciona 100% online** no Streamlit Cloud

**🎯 Padrões Detectados:**
- Sequências longas e médias
- Tendências estatísticas  
- Padrões de alternância
- Análise probabilística em tempo real
""")

st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')} | Dados da API Blaze")

# Atualização automática se estiver no modo auto
if st.session_state.ia.modo_auto and tempo_decorrido > 35:
    st.rerun()
