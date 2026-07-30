import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da Página
st.set_page_config(page_title="CLIMA POSITIVO • Gestão", layout="centered", initial_sidebar_state="collapsed")

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

# --- PERSISTÊNCIA CSV ---
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

# Gestão de Idioma
if "idioma" not in st.session_state:
    st.session_state.idioma = "Português"

if "pagina_ativa" not in st.session_state:
    st.session_state.pagina_ativa = "Painel"

# Dicionário de Traduções Completas PT / FR
t = {
    "Português": {
        "sub": "PAINEL DE CONTROLO",
        "titulo": "CLIMA POSITIVO",
        "painel": "📊 Painel",
        "registo": "➕ Registar",
        "inventario": "📋 Inventário",
        "obras": "🏗️ Obras",
        "func": "👥 Funcionários",
        "t_itens": "Total Itens",
        "t_qtd": "Total Qtd",
        "t_obras": "Obras Ativas",
        "t_func": "Funcionários",
        "reg_titulo": "Registo de Material, Entrada, Saída ou Sobra",
        "lbl_cod": "Código do Produto (Ex: P125)",
        "lbl_mat": "Nome do Material / Descrição",
        "lbl_qtd": "Quantidade",
        "lbl_tipo": "Tipo de Movimento",
        "opt_tipo": ["Entrada / Stock", "Saída", "Sobra de Obra"],
        "lbl_local": "Localização / Obra",
        "btn_guardar": "💾 Guardar Registo no Inventário",
        "sucesso_reg": "✅ Movimento / Material registado com sucesso!",
        "pesquisa": "🔍 Pesquisar código, material ou obra...",
        "gestao_obras": "Gestão de Obras e Chantiers",
        "nova_obra": "Nome da Nova Obra / Chantier",
        "btn_add_obra": "Adicionar Obra",
        "obras_ativas": "Obras Ativas (Gerir / Eliminar)",
        "cad_func": "Cadastro de Funcionários / Employés",
        "nome_func": "Nome Completo do Funcionário",
        "cargo_func": "Função / Cargo (Ex: Eletricista, Chefe)",
        "contacto_func": "Contacto / Telefone",
        "btn_cad_func": "Cadastrar Funcionário",
        "lista_func": "Lista de Funcionários Ativos e Acessos"
    },
    "Français": {
        "sub": "PANNEAU DE CONTRÔLE",
        "titulo": "CLIMA POSITIVO",
        "painel": "📊 Tableau",
        "registo": "➕ Enregistrer",
        "inventario": "📋 Inventaire",
        "obras": "🏗️ Chantiers",
        "func": "👥 Employés",
        "t_itens": "Total Articles",
        "t_qtd": "Qté Totale",
        "t_obras": "Chantiers Actifs",
        "t_func": "Employés",
        "reg_titulo": "Enregistrement de Matériel, Entrée, Sortie ou Surplus",
        "lbl_cod": "Code Produit (Ex: P125)",
        "lbl_mat": "Nom du Matériel / Description",
        "lbl_qtd": "Quantité",
        "lbl_tipo": "Type de Mouvement",
        "opt_tipo": ["Entrée / Stock", "Sortie", "Surplus de Chantier"],
        "lbl_local": "Localisation / Chantier",
        "btn_guardar": "💾 Enregistrer dans l'Inventaire",
        "sucesso_reg": "✅ Mouvement / Matériel enregistré avec succès !",
        "pesquisa": "🔍 Rechercher code, matériel ou chantier...",
        "gestao_obras": "Gestion des Chantiers",
        "nova_obra": "Nom du Nouveau Chantier",
        "btn_add_obra": "Ajouter Chantier",
        "obras_ativas": "Chantiers Actifs (Gérer / Supprimer)",
        "cad_func": "Enregistrement des Employés",
        "nome_func": "Nom Complet de l'Employé",
        "cargo_func": "Fonction / Poste (Ex: Électricien, Chef)",
        "contacto_func": "Contact / Téléphone",
        "btn_cad_func": "Enregistrer l'Employé",
        "lista_func": "Liste des Employés Actifs et Accès"
    }
}[st.session_state.idioma]

# --- CABEÇALHO ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
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

with col_h2:
    st.session_state.idioma = st.selectbox("🌐 Idioma", ["Português", "Français"], index=0 if st.session_state.idioma=="Português" else 1, label_visibility="collapsed")

st.markdown("<div style='margin: 10px 0;'></div>", unsafe_allow_html=True)

# --- MENU DE NAVEGAÇÃO ---
m_cols = st.columns(5)
with m_cols[0]:
    if st.button(t['painel']): st.session_state.pagina_ativa = "Painel"
with m_cols[1]:
    if st.button(t['registo']): st.session_state.pagina_ativa = "Registo"
with m_cols[2]:
    if st.button(t['inventario']): st.session_state.pagina_ativa = "Inventario"
with m_cols[3]:
    if st.button(t['obras']): st.session_state.pagina_ativa = "Obras"
with m_cols[4]:
    if st.button(t['func']): st.session_state.pagina_ativa = "Funcionarios"

st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

# Carregar dados
df_materiais = carregar_csv(ARQUIVO_DADOS, ["codigo", "material", "qtd", "tipo", "local", "data"])
df_obras = carregar_csv(ARQUIVO_OBRAS, ["nome"])
if df_obras.empty:
    df_obras = pd.DataFrame({"nome": ["Armazém Central", "Obra Alpha", "Residencial Parque", "RENAULT", "BSPP", "MATHSTIC", "JEUNEURS", "HOPITAUX SACLAY"]})
    guardar_csv(df_obras, ARQUIVO_OBRAS)

df_func = carregar_csv(ARQUIVO_FUNC, ["nome", "funcao", "contacto", "estado"])

# ==========================================
# 1. PAINEL
# ==========================================
if st.session_state.pagina_ativa == "Painel":
    tot_i = len(df_materiais)
    tot_q = int(df_materiais["qtd"].sum()) if tot_i > 0 else 0
    tot_o = len(df_obras)
    tot_f = len(df_func)

    st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card card-orange">
                <div class="metric-title">📦 {t['t_itens']}</div>
                <div class="metric-value">{tot_i}</div>
            </div>
            <div class="metric-card card-green">
                <div class="metric-title">🍃 {t['t_qtd']}</div>
                <div class="metric-value">{tot_q}</div>
            </div>
            <div class="metric-card card-blue">
                <div class="metric-title">🏗️ {t['t_obras']}</div>
                <div class="metric-value">{tot_o}</div>
            </div>
            <div class="metric-card card-purple">
                <div class="metric-title">👥 {t['t_func']}</div>
                <div class="metric-value">{tot_f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 2. REGISTO (Com Entrada, Saída e Sobra de Obra bem definidos)
# ==========================================
elif st.session_state.pagina_ativa == "Registo":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>➕ {t['reg_titulo']}</h3>", unsafe_allow_html=True)
    
    with st.form("form_reg", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            codigo = st.text_input(t['lbl_cod'])
            material = st.text_input(t['lbl_mat'])
        with col2:
            qtd = st.number_input(t['lbl_qtd'], min_value=1.0, step=1.0, value=1.0, format="%.0f")
            tipo_mov = st.selectbox(t['lbl_tipo'], t['opt_tipo'])
            
        locais = df_obras["nome"].tolist() if not df_obras.empty else ["Armazém Central"]
        local = st.selectbox(t['lbl_local'], locais)
        
        if st.form_submit_button(t['btn_guardar']):
            if not codigo or not material:
                st.error("❌ Preencha todos os campos obrigatórios.")
            else:
                novo = {
                    "codigo": str(codigo).upper(),
                    "material": material,
                    "qtd": int(qtd),
                    "tipo": tipo_mov,
                    "local": local,
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                df_materiais = pd.concat([df_materiais, pd.DataFrame([novo])], ignore_index=True)
                guardar_csv(df_materiais, ARQUIVO_DADOS)
                st.success(t['sucesso_reg'])
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. INVENTÁRIO
# ==========================================
elif st.session_state.pagina_ativa == "Inventario":
    st.markdown(f"<h3>{t['inventario']}</h3>", unsafe_allow_html=True)
    if df_materiais.empty:
        st.info("ℹ️ Sem registos.")
    else:
        pesquisa = st.text_input(t['pesquisa'], "")
        df_ex = df_materiais
        if pesquisa:
            df_ex = df_materiais[
                df_materiais['codigo'].str.contains(pesquisa, case=False, na=False) |
                df_materiais['material'].str.contains(pesquisa, case=False, na=False) |
                df_materiais['local'].str.contains(pesquisa, case=False, na=False)
            ]
        
        for _, row in df_ex.iterrows():
            tipo_txt = row.get('tipo', 'Stock')
            st.markdown(f"""
                <div class="item-row">
                    <div>
                        <span class="item-code">{row['codigo']}</span>
                        <div class="item-name">{row['material']} <span style="font-size: 11px; color: #0284C7; background: #E0F2FE; padding: 2px 6px; border-radius: 4px;">{tipo_txt}</span></div>
                        <div class="item-meta">📍 {row['local']} • 📅 {row['data']}</div>
                    </div>
                    <div class="item-qty">{int(row['qtd'])} un</div>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 4. OBRAS
# ==========================================
elif st.session_state.pagina_ativa == "Obras":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>🏗️ {t['gestao_obras']}</h3>", unsafe_allow_html=True)
    
    with st.form("form_obra_nova", clear_on_submit=True):
        nova_obra = st.text_input(t['nova_obra'])
        if st.form_submit_button(t['btn_add_obra']) and nova_obra:
            if nova_obra not in df_obras["nome"].values:
                df_obras = pd.concat([df_obras, pd.DataFrame({"nome": [nova_obra]})], ignore_index=True)
                guardar_csv(df_obras, ARQUIVO_OBRAS)
                st.success("✅ Obra adicionada com sucesso!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>📌 {t['obras_ativas']}</h3>", unsafe_allow_html=True)
    for idx, row in df_obras.iterrows():
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"🏢 **{row['nome']}**")
        with c2:
            if st.button("🗑️", key=f"del_obra_{idx}"):
                df_obras = df_obras.drop(idx).reset_index(drop=True)
                guardar_csv(df_obras, ARQUIVO_OBRAS)
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. FUNCIONÁRIOS
# ==========================================
elif st.session_state.pagina_ativa == "Funcionarios":
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>👥 {t['cad_func']}</h3>", unsafe_allow_html=True)
    
    with st.form("form_func", clear_on_submit=True):
        f_nome = st.text_input(t['nome_func'])
        f_cargo = st.text_input(t['cargo_func'])
        f_contacto = st.text_input(t['contacto_func'])
        
        if st.form_submit_button(t['btn_cad_func']):
            if not f_nome:
                st.error("❌ Indique o nome.")
            else:
                novo_f = {"nome": f_nome, "funcao": f_cargo, "contacto": f_contacto, "estado": "Ativo"}
                df_func = pd.concat([df_func, pd.DataFrame([novo_f])], ignore_index=True)
                guardar_csv(df_func, ARQUIVO_FUNC)
                st.success("✅ Funcionário registado!")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>📋 {t['lista_func']}</h3>", unsafe_allow_html=True)
    if df_func.empty:
        st.info("ℹ️ Sem funcionários.")
    else:
        for idx, row in df_func.iterrows():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.markdown(f"👤 **{row['nome']}**<br><span style='color: #6B7280; font-size: 12px;'>{row['funcao']} • {row['contacto']} • <b>{row['estado']}</b></span>", unsafe_allow_html=True)
            with c2:
                est = "Bloqueado" if row['estado'] == "Ativo" else "Ativo"
                lbl = "🔒" if row['estado'] == "Ativo" else "🔓"
                if st.button(lbl, key=f"est_{idx}"):
                    df_func.loc[idx, 'estado'] = est
                    guardar_csv(df_func, ARQUIVO_FUNC)
                    st.rerun()
            with c3:
                if st.button("🗑️", key=f"del_func_{idx}"):
                    df_func = df_func.drop(idx).reset_index(drop=True)
                    guardar_csv(df_func, ARQUIVO_FUNC)
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
