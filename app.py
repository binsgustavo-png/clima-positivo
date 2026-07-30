import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="CLIMA POSITIVO • Gestão", page_layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #F3F4F6; }
    h1, h2, h3 { color: #111827; font-family: sans-serif; }
    .card-container { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
    .card { flex: 1; min-width: 180px; padding: 1.25rem; border-radius: 12px; color: white; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .card-title { font-size: 0.85rem; font-weight: 600; opacity: 0.9; margin-bottom: 0.4rem; }
    .card-value { font-size: 1.75rem; font-weight: 700; }
    .bg-orange { background-color: #EA580C; }
    .bg-green { background-color: #059669; }
    .bg-blue { background-color: #0284C7; }
    
    .item-card {
        background-color: white; padding: 1rem; border-radius: 12px; margin-bottom: 0.75rem;
        border: 1px solid #E5E7EB; display: flex; justify-content: space-between; align-items: center;
    }
    .item-codigo { font-size: 0.85rem; color: #6B7280; font-family: monospace; font-weight: bold; }
    .item-nome { font-size: 1rem; font-weight: 600; color: #111827; }
    .item-meta { font-size: 0.8rem; color: #6B7280; }
    .item-qtd { background-color: #ECFDF5; color: #059669; padding: 0.2rem 0.6rem; border-radius: 99px; font-weight: 700; font-size: 1rem; }
    
    div.stButton > button {
        width: 100%; background-color: #059669; color: white; border-radius: 8px; font-weight: 600; padding: 0.6rem; border: none;
    }
    div.stButton > button:hover { background-color: #047857; }
    </style>
""", unsafe_allow_html=True)

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

st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
        <div>
            <p style='margin: 0; color: #6B7280; font-size: 0.9rem;'>Painel de Controlo</p>
            <h1 style='margin: 0; font-size: 1.8rem;'>CLIMA POSITIVO</h1>
        </div>
        <div style='background: #E0F2FE; color: #0369A1; padding: 0.4rem 0.8rem; border-radius: 99px; font-weight: 600; font-size: 0.85rem;'>
            🟢 Online
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

nav_cols = st.columns(3)
with nav_cols[0]:
    if st.button("📊 Painel", key="nav_p"): st.session_state.pagina_ativa = "Painel"
with nav_cols[1]:
    if st.button("➕ Registar", key="nav_r"): st.session_state.pagina_ativa = "Registo"
with nav_cols[2]:
    if st.button("📋 Inventário", key="nav_i"): st.session_state.pagina_ativa = "Inventario"

st.markdown("---")
df_atual = carregar_dados()

if st.session_state.pagina_ativa == "Painel":
    total_materiais = len(df_atual)
    total_sobras = int(df_atual["qtd"].sum()) if total_materiais > 0 else 0
    total_obras = len(st.session_state.obras)

    st.markdown(f"""
        <div class="card-container">
            <div class="card bg-orange">
                <div class="card-title">📦 Total Itens</div>
                <div class="card-value">{total_materiais}</div>
            </div>
            <div class="card bg-green">
                <div class="card-title">🍃 Total Qtd</div>
                <div class="card-value">{total_sobras} un</div>
            </div>
            <div class="card bg-blue">
                <div class="card-title">🏗️ Obras</div>
                <div class="card-value">{total_obras}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏢 Gestão de Obras")
    with st.form("form_obra", clear_on_submit=True):
        nova_obra = st.text_input("Nome da Nova Obra")
        if st.form_submit_button("Adicionar Obra") and nova_obra:
            if nova_obra not in st.session_state.obras:
                st.session_state.obras.append(nova_obra)
                st.success(f"Obra '{nova_obra}' adicionada!")
                st.rerun()

    for o in st.session_state.obras:
        st.markdown(f"- 📌 {o}")

elif st.session_state.pagina_ativa == "Registo":
    st.markdown("<h3>➕ Registo de Material</h3>", unsafe_allow_html=True)
    
    # Utilizar a câmara nativa para tirar foto do produto/etiqueta se desejar
    foto = st.camera_input("📷 Tirar foto do produto ou código (Opcional)")

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

elif st.session_state.pagina_ativa == "Inventario":
    st.markdown("<h3>📋 Inventário e Consultas</h3>", unsafe_allow_html=True)
    
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
                    <div class="item-card">
                        <div>
                            <span class='item-codigo'>{row['codigo']}</span><br>
                            <span class='item-nome'>{row['material']}</span><br>
                            <span class='item-meta'>📍 {row['local']} • 📅 {row['data']}</span>
                        </div>
                        <div class='item-qtd'>{int(row['qtd'])} un</div>
                    </div>
                """, unsafe_allow_html=True)
