import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração corrigida com 'layout'
st.set_page_config(page_title="CLIMA POSITIVO", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main {
        background-color: #F8F9FA;
    }
    .card-orange {
        background-color: #FF7043;
        color: white;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 12px;
    }
    .card-green {
        background-color: #26A69A;
        color: white;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 12px;
    }
    .card-blue {
        background-color: #42A5F5;
        color: white;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 12px;
    }
    .card-yellow {
        background-color: #FFA726;
        color: white;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 4px;
        opacity: 0.9;
    }
    .card-value {
        font-size: 32px;
        font-weight: 700;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        background-color: #26A69A;
        color: white;
        border: none;
        padding: 10px;
    }
    div.stButton > button:hover {
        background-color: #00897B;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

ARQUIVO_DADOS = "dados_sobras.csv"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            return pd.read_csv(ARQUIVO_DADOS)
        except Exception:
            return pd.DataFrame(columns=["codigo", "material", "qtd", "local", "estado", "data"])
    else:
        return pd.DataFrame(columns=["codigo", "material", "qtd", "local", "estado", "data"])

def guardar_dados(df):
    df.to_csv(ARQUIVO_DADOS, index=False)

if "obras" not in st.session_state:
    st.session_state.obras = ["Armazém Central", "Obra Alpha", "Residencial Parque"]

if "menu_ativo" not in st.session_state:
    st.session_state.menu_ativo = "Resumo"

st.markdown("<p style='color: #71717A; font-size: 14px; margin-bottom: 0px;'>Olá, Administrador</p>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #09090B; margin-top: 0px; font-weight: 700;'>Painel de Controlo</h2>", unsafe_allow_html=True)

menu_cols = st.columns(5)
with menu_cols[0]:
    if st.button("📊 Resumo", key="btn_res"): st.session_state.menu_ativo = "Resumo"
with menu_cols[1]:
    if st.button("📦 Estoque", key="btn_est"): st.session_state.menu_ativo = "Estoque"
with menu_cols[2]:
    if st.button("🔄 Movs", key="btn_mov"): st.session_state.menu_ativo = "Movimentos"
with menu_cols[3]:
    if st.button("♻️ Sobras", key="btn_sob"): st.session_state.menu_ativo = "Sobras"
with menu_cols[4]:
    if st.button("🏗️ Obras", key="btn_obr"): st.session_state.menu_ativo = "Obras"

st.markdown("---")

df_atual = carregar_dados()

if st.session_state.menu_ativo == "Resumo":
    total_materiais = len(df_atual) if not df_atual.empty else 0
    total_sobras = df_atual["qtd"].sum() if not df_atual.empty else 0

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="card-orange">
                <div class="card-title">📦 Materiais</div>
                <div class="card-value">{total_materiais}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="card-green">
                <div class="card-title">📥 Registos Hoje</div>
                <div class="card-value">{total_materiais}</div>
            </div>
        """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
            <div class="card-blue">
                <div class="card-title">🔄 Obras Ativas</div>
                <div class="card-value">{len(st.session_state.obras)}</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="card-yellow">
                <div class="card-title">🍃 Sobras Disp.</div>
                <div class="card-value">{int(total_sobras)}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🕒 Últimos Movimentos")
    if not df_atual.empty:
        ultimos = df_atual.tail(5).iloc[::-1]
        for _, row in ultimos.iterrows():
            st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #E4E4E7; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #09090B;">{row['material']}</strong><br>
                        <span style="color: #71717A; font-size: 12px;">{row['local']} • {row['codigo']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #26A69A; font-weight: 700;">+{int(row['qtd'])} un</span><br>
                        <span style="color: #A1A1AA; font-size: 11px;">{row['data']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Ainda não existem movimentos registados.")

elif st.session_state.menu_ativo == "Sobras" or st.session_state.menu_ativo == "Estoque":
    st.markdown("### ♻️ Banco de Sobras e Materiais")
    
    with st.form("form_registo", clear_on_submit=True):
        codigo = st.text_input("CÓDIGO DO PRODUTO (Ex: P125)")
        material = st.text_input("NOME DO MATERIAL")
        qtd = st.number_input("QUANTIDADE", min_value=0.0, step=1.0, value=1.0)
        local = st.selectbox("LOCALIZAÇÃO", st.session_state.obras)
        
        if st.form_submit_button("Guardar Material"):
            if not codigo or not material:
                st.error("Preencha o código e o nome.")
            else:
                df_base = carregar_dados()
                if not df_base.empty and codigo in df_base["codigo"].astype(str).values:
                    st.error(f"❌ O código '{codigo}' já está registado!")
                else:
                    novo = {
                        "codigo": codigo,
                        "material": material,
                        "qtd": qtd,
                        "local": local,
                        "estado": "Disponível",
                        "data": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    df_novo = pd.concat([df_base, pd.DataFrame([novo])], ignore_index=True)
                    guardar_dados(df_novo)
                    st.success("Material guardado com sucesso!")
                    st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Lista de Materiais Existentes")
    if not df_atual.empty:
        for idx, row in df_atual.iterrows():
            st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #E4E4E7;">
                    <b>{row['codigo']}</b> - {row['material']}<br>
                    <span style="color: #71717A; font-size: 13px;">Qtd: {row['qtd']} un | Local: {row['local']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Sem materiais registados.")

elif st.session_state.menu_ativo == "Obras":
    st.markdown("### 🏗️ Gestão de Obras")
    with st.form("form_obra", clear_on_submit=True):
        nova_obra = st.text_input("Nome da Nova Obra")
        if st.form_submit_button("Adicionar Obra") and nova_obra:
            if nova_obra not in st.session_state.obras:
                st.session_state.obras.append(nova_obra)
                st.success("Obra adicionada!")
                st.rerun()
    for o in st.session_state.obras:
        st.markdown(f"- 📌 {o}")

elif st.session_state.menu_ativo == "Movimentos":
    st.markdown("### 🔄 Histórico de Movimentos")
    if not df_atual.empty:
        st.dataframe(df_atual, use_container_width=True)
    else:
        st.info("Ainda sem movimentos.")
