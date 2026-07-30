import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da Página
st.set_page_config(page_title="CLIMA POSITIVO • Gestão", layout="centered", initial_sidebar_state="collapsed")

# --- ESTILO VISUAL PROFISSIONAL E LIMPO ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    /* Cabeçalho */
    .header-box { display: flex; justify-content: space-between; align-items: center; background: white; padding: 16px 20px; border-radius: 12px; border: 1px solid #E5E7EB; margin-bottom: 20px; }
    
    /* Cartões de Resumo */
    .metric-row { display: flex; gap: 12px; margin-bottom: 20px; width: 100%; }
    .metric-card { flex: 1; padding: 18px; border-radius: 12px; color: white; text-align: left; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .card-orange { background: linear-gradient(135deg, #FF7043 0%, #F4511E 100%); }
    .card-green { background: linear-gradient(135deg, #26A69A 0%, #00897B 100%); }
    .card-blue { background: linear-gradient(135deg, #42A5F5 0%, #1E88E5 100%); }
    .metric-title { font-size: 13px; font-weight: 600; opacity: 0.9; margin-bottom: 4px; text-transform: uppercase; }
    .metric-value { font-size: 26px; font-weight: 800; }

    /* Contentores e Formulários */
    .content-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    
    /* Lista de Itens */
    .item-row { background: white; padding: 14px 16px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #E5E7EB; display: flex; justify-content: space-between; align-items: center; }
    .item-code { font-size: 12px; color: #6B7280; font-family: monospace; font-weight: bold; background: #F3F4F6; padding: 2px 6px; border-radius: 4px; }
    .item-name { font-size: 15px; font-weight: 600; color: #111827; margin-top: 4px; }
    .item-meta { font-size: 12px; color: #9CA3AF; margin-top: 2px; }
    .item-qty { background: #E6F4EA; color: #137333; padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 14px; }

    /* Botões de Navegação */
    div.stButton > button { width: 100%; border-radius: 8px; font-weight: 600; background-color: #00897B; color: white; border: none; padding: 10px; }
    div.stButton > button:hover { background-color: #00695C; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- PERSISTÊNCIA CSV ---
ARQUIVO_DADOS = "dados_sobras_v2.csv"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            return pd.read_csv(ARQUIVO_DADOS)
        except Exception:
            return pd.DataFrame(columns=["codigo", "material", "qtd", "local", "data"])
    else:
        return pd.DataFrame(columns=["codigo", "material", "qtd", "local", "data"])

def guardar_dados(df):
    df.to_csv(ARQUIVO_DADOS, index=False)

if "obras" not in st.session_state:
    st.session_state.obras = ["Armazém Central", "Obra Alpha", "Residencial Parque"]

if "pagina_ativa" not in st.session_state:
    st.session_state.pagina_ativa = "Painel"

# --- CABEÇALHO ---
st.markdown("""
    <div class="header-box">
        <div>
            <div style="font-size: 12px; color: #6B7280; font-weight: 600;">PAINEL DE CONTROLO</div>
            <div style="font-size: 20px; font-weight: 800; color: #111827;">CLIMA POSITIVO</div>
        </div>
        <div style="background: #E6F4EA; color: #137333; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 12px;">
            ● Online
        </div>
    </div>
""", unsafe_allow_html=True)

# --- MENU DE NAVEGAÇÃO ---
col_n1, col_n2, col_n3 = st.columns(3)
with col_n1:
    if st.button("📊 Painel"): st.session_state.pagina_ativa = "Painel"
with col_n2:
    if st.button("➕ Registar"): st.session_state.pagina_ativa = "Registo"
with col_n3:
    if st.button("📋 Inventário"): st.session_state.pagina_ativa = "Inventario"

st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
df_atual = carregar_dados()

# ==========================================
# 1. PAINEL GERAL
# ==========================================
if st.session_state.pagina_ativa == "Painel":
    total_materiais = len(df_atual)
    total_sobras = int(df_atual["qtd"].sum()) if total_materiais > 0 else 0
    total_obras = len(st.session_state.obras)

    st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card card-orange">
                <div class="metric-title">📦 Total Itens</div>
                <div class="metric-value">{total_materiais}</div>
            </div>
            <div class="metric-card card-green">
                <div class="metric-title">🍃 Total Qtd</div>
                <div class="metric-value">{total_sobras}</div>
            </div>
            <div class="metric-card card-blue">
                <div class="metric-title">🏗️ Obras</div>
                <div class="metric-value">{total_obras}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🏢 Gestão de Obras</h3>", unsafe_allow_html=True)
    with st.form("form_obra", clear_on_submit=True):
        nova_obra = st.text_input("Nome da Nova Obra")
        if st.form_submit_button("Adicionar Obra") and nova_obra:
            if nova_obra not in st.session_state.obras:
                st.session_state.obras.append(nova_obra)
                st.success(f"Obra '{nova_obra}' adicionada!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📌 Obras Ativas</h3>", unsafe_allow_html=True)
    for o in st.session_state.obras:
        st.markdown(f"- 🏢 {o}")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 2. REGISTO DE MATERIAL
# ==========================================
elif st.session_state.pagina_ativa == "Registo":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("<h3>➕ Novo Registo de Material</h3>", unsafe_allow_html=True)
    
    with st.form("form_registo", clear_on_submit=True):
        codigo = st.text_input("CÓDIGO DO PRODUTO (Ex: P125)")
        material = st.text_input("NOME DO MATERIAL / DESCRIÇÃO")
        qtd = st.number_input("QUANTIDADE", min_value=1.0, step=1.0, value=1.0, format="%.0f")
        local = st.selectbox("LOCALIZAÇÃO / OBRA", st.session_state.obras)
        
        if st.form_submit_button("Guardar Material"):
            if not codigo or not material:
                st.error("❌ Preencha o código e o nome do material.")
            else:
                df_base = carregar_dados()
                novo_reg = {
                    "codigo": str(codigo).upper(),
                    "material": material,
                    "qtd": int(qtd),
                    "local": local,
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                df_novo = pd.concat([df_base, pd.DataFrame([novo_reg])], ignore_index=True)
                guardar_dados(df_novo)
                st.success("✅ Material guardado com sucesso!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. INVENTÁRIO COMPLETO
# ==========================================
elif st.session_state.pagina_ativa == "Inventario":
    st.markdown("<h3>📋 Inventário de Materiais</h3>", unsafe_allow_html=True)
    
    if df_atual.empty:
        st.info("ℹ️ O inventário está vazio.")
    else:
        pesquisa = st.text_input("🔍 Pesquisar código, material ou obra...", "")
        if pesquisa:
            df_exibe = df_atual[
                df_atual['codigo'].str.contains(pesquisa, case=False) |
                df_atual['material'].str.contains(pesquisa, case=False) |
                df_atual['local'].str.contains(pesquisa, case=False)
            ]
        else:
            df_exibe = df_atual

        if df_exibe.empty:
            st.warning("⚠️ Nenhum resultado encontrado.")
        else:
            for _, row in df_exibe.iterrows():
                st.markdown(f"""
                    <div class="item-row">
                        <div>
                            <span class="item-code">{row['codigo']}</span>
                            <div class="item-name">{row['material']}</div>
                            <div class="item-meta">📍 {row['local']} • 📅 {row['data']}</div>
                        </div>
                        <div class="item-qty">{int(row['qtd'])} un</div>
                    </div>
                """, unsafe_allow_html=True)
