import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da Página
st.set_page_config(page_title="CLIMA POSITIVO • Gestão Completa", layout="centered", initial_sidebar_state="collapsed")

# --- ESTILO VISUAL PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    .header-box { display: flex; justify-content: space-between; align-items: center; background: white; padding: 16px 20px; border-radius: 12px; border: 1px solid #E5E7EB; margin-bottom: 20px; }
    
    .metric-row { display: flex; gap: 12px; margin-bottom: 20px; width: 100%; flex-wrap: wrap; }
    .metric-card { flex: 1; min-width: 150px; padding: 18px; border-radius: 12px; color: white; text-align: left; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .card-orange { background: linear-gradient(135deg, #FF7043 0%, #F4511E 100%); }
    .card-green { background: linear-gradient(135deg, #26A69A 0%, #00897B 100%); }
    .card-blue { background: linear-gradient(135deg, #42A5F5 0%, #1E88E5 100%); }
    .card-purple { background: linear-gradient(135deg, #AB47BC 0%, #8E24AA 100%); }
    
    .metric-title { font-size: 12px; font-weight: 600; opacity: 0.9; margin-bottom: 4px; text-transform: uppercase; }
    .metric-value { font-size: 24px; font-weight: 800; }

    .content-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    
    .item-row { background: white; padding: 14px 16px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #E5E7EB; display: flex; justify-content: space-between; align-items: center; }
    .item-code { font-size: 12px; color: #6B7280; font-family: monospace; font-weight: bold; background: #F3F4F6; padding: 2px 6px; border-radius: 4px; }
    .item-name { font-size: 15px; font-weight: 600; color: #111827; margin-top: 4px; }
    .item-meta { font-size: 12px; color: #9CA3AF; margin-top: 2px; }
    .item-qty { background: #E6F4EA; color: #137333; padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 14px; }

    div.stButton > button { width: 100%; border-radius: 8px; font-weight: 600; background-color: #00897B; color: white; border: none; padding: 10px; }
    div.stButton > button:hover { background-color: #00695C; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- PERSISTÊNCIA FICHEIROS CSV ---
ARQUIVO_DADOS = "dados_materiais.csv"
ARQUIVO_OBRAS = "dados_obras.csv"
ARQUIVO_FUNC = "dados_funcionarios.csv"

def carregar_csv(arquivo, colunas_default):
    if os.path.exists(arquivo):
        try:
            return pd.read_csv(arquivo)
        except Exception:
            return pd.DataFrame(columns=colunas_default)
    else:
        return pd.DataFrame(columns=colunas_default)

def guardar_csv(df, arquivo):
    df.to_csv(arquivo, index=False)

# Inicializar Estados de Sessão
if "idioma" not in st.session_state:
    st.session_state.idioma = "Português"

if "pagina_ativa" not in st.session_state:
    st.session_state.pagina_ativa = "Painel"

# Textos Multilingue (PT / FR)
t = {
    "Português": {
        "titulo": "CLIMA POSITIVO",
        "sub": "PAINEL DE CONTROLO",
        "painel": "📊 Painel",
        "registo": "➕ Registar",
        "inventario": "📋 Inventário",
        "obras": "🏗️ Obras",
        "func": "👥 Funcionários",
        "total_itens": "Total Itens",
        "total_qtd": "Total Qtd",
        "total_obras": "Obras Ativas",
        "total_func": "Funcionários",
    },
    "Français": {
        "titulo": "CLIMA POSITIVO",
        "sub": "PANNEAU DE CONTRÔLE",
        "painel": "📊 Tableau",
        "registo": "➕ Enregistrer",
        "inventario": "📋 Inventaire",
        "obras": "🏗️ Chantiers",
        "func": "👥 Employés",
        "total_itens": "Total Articles",
        "total_qtd": "Qté Totale",
        "total_obras": "Chantiers Actifs",
        "total_func": "Employés",
    }
}[st.session_state.idioma]

# --- CABEÇALHO COM SELEÇÃO DE IDIOMA ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown(f"""
        <div class="header-box" style="margin-bottom: 0px;">
            <div>
                <div style="font-size: 11px; color: #6B7280; font-weight: 600;">{t['sub']}</div>
                <div style="font-size: 20px; font-weight: 800; color: #111827;">{t['titulo']}</div>
            </div>
            <div style="background: #E6F4EA; color: #137333; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 12px;">
                ● Online
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.session_state.idioma = st.selectbox("🌐 Idioma", ["Português", "Français"], index=0 if st.session_state.idioma=="Português" else 1, label_visibility="collapsed")

st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)

# --- MENU DE NAVEGAÇÃO COMPLETO ---
menu_cols = st.columns(5)
with menu_cols[0]:
    if st.button(t['painel']): st.session_state.pagina_ativa = "Painel"
with menu_cols[1]:
    if st.button(t['registo']): st.session_state.pagina_ativa = "Registo"
with menu_cols[2]:
    if st.button(t['inventario']): st.session_state.pagina_ativa = "Inventario"
with menu_cols[3]:
    if st.button(t['obras']): st.session_state.pagina_ativa = "Obras"
with menu_cols[4]:
    if st.button(t['func']): st.session_state.pagina_ativa = "Funcionarios"

st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

# Carregar Dados
df_materiais = carregar_csv(ARQUIVO_DADOS, ["codigo", "material", "qtd", "local", "data"])
df_obras = carregar_csv(ARQUIVO_OBRAS, ["nome"])
if df_obras.empty:
    df_obras = pd.DataFrame({"nome": ["Armazém Central", "Obra Alpha", "Residencial Parque", "RENAULT", "BSPP", "MATHSTIC", "JEUNEURS", "HOPITAUX SACLAY"]})
    guardar_csv(df_obras, ARQUIVO_OBRAS)

df_func = carregar_csv(ARQUIVO_FUNC, ["nome", "funcao", "contacto", "estado"])

# ==========================================
# 1. PAINEL GERAL
# ==========================================
if st.session_state.pagina_ativa == "Painel":
    tot_itens = len(df_materiais)
    tot_qtd = int(df_materiais["qtd"].sum()) if tot_itens > 0 else 0
    tot_obras = len(df_obras)
    tot_func = len(df_func)

    st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card card-orange">
                <div class="metric-title">📦 {t['total_itens']}</div>
                <div class="metric-value">{tot_itens}</div>
            </div>
            <div class="metric-card card-green">
                <div class="metric-title">🍃 {t['total_qtd']}</div>
                <div class="metric-value">{tot_qtd}</div>
            </div>
            <div class="metric-card card-blue">
                <div class="metric-title">🏗️ {t['total_obras']}</div>
                <div class="metric-value">{tot_obras}</div>
            </div>
            <div class="metric-card card-purple">
                <div class="metric-title">👥 {t['total_func']}</div>
                <div class="metric-value">{tot_func}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='content-card'><h3>📊 Resumo Operacional</h3><p style='color: #6B7280;'>Sistema sincronizado e pronto para gerir materiais, sobras, obras e funcionários no terreno com total autonomia.</p></div>", unsafe_allow_html=True)

# ==========================================
# 2. REGISTO DE MATERIAIS / SOBRAS
# ==========================================
elif st.session_state.pagina_ativa == "Registo":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("<h3>➕ Registo de Material / Sobra</h3>", unsafe_allow_html=True)
    
    with st.form("form_reg", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            codigo = st.text_input("Código do Produto (Ex: P125)")
            material = st.text_input("Nome do Material / Descrição")
        with col_f2:
            qtd = st.number_input("Quantidade", min_value=1.0, step=1.0, value=1.0, format="%.0f")
            lista_locais = df_obras["nome"].tolist() if not df_obras.empty else ["Armazém Central"]
            local = st.selectbox("Localização / Obra", lista_locais)
        
        submitted = st.form_submit_button("💾 Guardar Registo no Inventário")
        if submitted:
            if not codigo or not material:
                st.error("❌ Preencha obrigatoriamente o código e o nome do material.")
            else:
                novo = {
                    "codigo": str(codigo).upper(),
                    "material": material,
                    "qtd": int(qtd),
                    "local": local,
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                df_materiais = pd.concat([df_materiais, pd.DataFrame([novo])], ignore_index=True)
                guardar_csv(df_materiais, ARQUIVO_DADOS)
                st.success("✅ Material / Sobra registado com sucesso!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. INVENTÁRIO
# ==========================================
elif st.session_state.pagina_ativa == "Inventario":
    st.markdown("<h3>📋 Inventário de Materiais e Sobras</h3>", unsafe_allow_html=True)
    if df_materiais.empty:
        st.info("ℹ️ Nenhum material registado até o momento.")
    else:
        pesquisa = st.text_input("🔍 Pesquisar por código, material ou obra...", "")
        df_ex = df_materiais
        if pesquisa:
            df_ex = df_materiais[
                df_materiais['codigo'].str.contains(pesquisa, case=False, na=False) |
                df_materiais['material'].str.contains(pesquisa, case=False, na=False) |
                df_materiais['local'].str.contains(pesquisa, case=False, na=False)
            ]
        
        for idx, row in df_ex.iterrows():
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

# ==========================================
# 4. GESTÃO DE OBRAS (ADICIONAR / ELIMINAR)
# ==========================================
elif st.session_state.pagina_ativa == "Obras":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🏗️ Gestão de Obras e Chantiers</h3>", unsafe_allow_html=True)
    
    with st.form("form_obra_nova", clear_on_submit=True):
        nova_obra = st.text_input("Nome da Nova Obra / Chantier")
        if st.form_submit_button("Adicionar Obra") and nova_obra:
            if nova_obra not in df_obras["nome"].values:
                df_obras = pd.concat([df_obras, pd.DataFrame({"nome": [nova_obra]})], ignore_index=True)
                guardar_csv(df_obras, ARQUIVO_OBRAS)
                st.success(f"✅ Obra '{nova_obra}' adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Esta obra já existe.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📌 Obras Ativas (Gerir / Eliminar)</h3>", unsafe_allow_html=True)
    for idx, row in df_obras.iterrows():
        col_o1, col_o2 = st.columns([4, 1])
        with col_o1:
            st.markdown(f"🏢 **{row['nome']}**")
        with col_o2:
            if st.button("🗑️ Apagar", key=f"del_obra_{idx}"):
                df_obras = df_obras.drop(idx).reset_index(drop=True)
                guardar_csv(df_obras, ARQUIVO_OBRAS)
                st.success("Obra eliminada!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. GESTÃO DE FUNCIONÁRIOS (CADASTRAR, BLOQUEAR, ALTERAR)
# ==========================================
elif st.session_state.pagina_ativa == "Funcionarios":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("<h3>👥 Cadastro de Funcionários / Employés</h3>", unsafe_allow_html=True)
    
    with st.form("form_func", clear_on_submit=True):
        f_nome = st.text_input("Nome Completo do Funcionário")
        f_cargo = st.text_input("Função / Cargo (Ex: Eletricista, Chefe de Equipa)")
        f_contacto = st.text_input("Contacto / Telefone")
        
        if st.form_submit_button("Cadastrar Funcionário"):
            if not f_nome:
                st.error("❌ Indique o nome do funcionário.")
            else:
                novo_f = {"nome": f_nome, "funcao": f_cargo, "contacto": f_contacto, "estado": "Ativo"}
                df_func = pd.concat([df_func, pd.DataFrame([novo_f])], ignore_index=True)
                guardar_csv(df_func, ARQUIVO_FUNC)
                st.success(f"✅ Funcionário '{f_nome}' cadastrado com sucesso!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📋 Lista de Funcionários Ativos e Acessos</h3>", unsafe_allow_html=True)
    if df_func.empty:
        st.info("ℹ️ Nenhum funcionário registado.")
    else:
        for idx, row in df_func.iterrows():
            col_e1, col_e2, col_e3 = st.columns([3, 1, 1])
            with col_e1:
                st.markdown(f"👤 **{row['nome']}**<br><span style='color: #6B7280; font-size: 12px;'>{row['funcao']} • {row['contacto']} • Estado: <b>{row['estado']}</b></span>", unsafe_allow_html=True)
            with col_e2:
                novo_estado = "Bloqueado" if row['estado'] == "Ativo" else "Ativo"
                label_btn = "🔒 Bloquear" if row['estado'] == "Ativo" else "🔓 Ativar"
                if st.button(label_btn, key=f"est_{idx}"):
                    df_func.loc[idx, 'estado'] = novo_estado
                    guardar_csv(df_func, ARQUIVO_FUNC)
                    st.rerun()
            with col_e3:
                if st.button("🗑️ Eliminar", key=f"del_func_{idx}"):
                    df_func = df_func.drop(idx).reset_index(drop=True)
                    guardar_csv(df_func, ARQUIVO_FUNC)
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
