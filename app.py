import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Gestão de Sobras - Obra", layout="wide")

# --- SIMULAÇÃO DE BASE DE DADOS EM SESSION STATE (Substitua pela ligação ao Supabase se preferir) ---
if "sobras" not in st.session_state:
    st.session_state.sobras = pd.DataFrame(columns=["codigo", "material", "qtd", "local", "estado", "data"])

if "obras" not in st.session_state:
    st.session_state.obras = ["Obra A", "Obra B", "Obra C"]

# --- MENU LATERAL ---
st.sidebar.title("Navegação")
menu = st.sidebar.radio("Ir para:", ["Banco de Sobras", "Funcionários"])

# ==========================================
# 1. BANCO DE SOBRAS
# ==========================================
if menu == "Banco de Sobras":
    st.title("📦 Banco de Sobras e Materiais Excedentes")
    
    with st.expander("➕ Disponibilizar Sobra para a Equipa", expanded=False):
        with st.form("form_nova_sobra", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                codigo_input = st.text_input("Código do Produto / Material")
                nome_input = st.text_input("Nome do Material")
            with col2:
                qtd_input = st.number_input("Quantidade", min_value=0.0, step=1.0)
                local_input = st.text_input("Local de Armazenamento", value="Armazém Central")
                
            btn_salvar = st.form_submit_button("Registar Sobra")
            
            if btn_salvar:
                if not codigo_input or not nome_input:
                    st.error("Por favor, preencha o código e o nome do material.")
                else:
                    # Validação: Impedir o uso do mesmo código se já existir
                    if not st.session_state.sobras.empty and codigo_input in st.session_state.sobras["codigo"].values:
                        st.error(f"Erro: O código '{codigo_input}' já se encontra cadastrado! Utilize um código único.")
                    else:
                        nova_linha = {
                            "codigo": codigo_input,
                            "material": nome_input,
                            "qtd": qtd_input,
                            "local": local_input,
                            "estado": "Disponível",
                            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.sobras = pd.concat([st.session_state.sobras, pd.DataFrame([nova_linha])], ignore_index=True)
                        st.success("Sobra registada com sucesso!")
                        st.rerun()

    st.markdown("---")
    
    # --- CAMPO DE BUSCA POR CÓDIGO ---
    st.subheader("Materiais Excedentes (Atuais e Histórico)")
    pesquisa_codigo = st.text_input("🔍 Procurar material (introduza o código do produto):", "")
    
    df_dados = st.session_state.sobras.copy()
    
    if not df_dados.empty:
        # Filtrar por código se houver texto na busca
        if pesquisa_codigo:
            df_dados = df_dados[df_dados["codigo"].astype(str).str.contains(pesquisa_codigo, case=False, na=False)]
        
        # --- AGRUPAMENTO AUTOMÁTICO E SOMA DE QUANTIDADES ---
        # Agrupa por código e nome, somando a quantidade dos itens iguais
        if not df_dados.empty:
            df_agrupado = df_dados.groupby(["codigo", "material", "local", "estado"], as_index=False).agg({
                "qtd": "sum",
                "data": "max"
            })
            
            # Exibição interativa em tabela com ações de baixa
            for index, row in df_agrupado.iterrows():
                col_info1, col_info2, col_info3, col_info4, col_acao1, col_acao2, col_acao3 = st.columns([1, 2, 1, 1, 1, 1, 1])
                
                with col_info1:
                    st.text(f"Cód: {row['codigo']}")
                with col_info2:
                    st.text(row['material'])
                with col_info3:
                    st.text(f"{row['qtd']} un")
                with col_info4:
                    st.text(row['local'])
                
                with col_acao1:
                    qtd_baixa = st.number_input("Qtd", min_value=0.0, max_value=float(row['qtd']), value=float(row['qtd']), key=f"qtd_{row['codigo']}", label_visibility="collapsed")
                with col_acao2:
                    obra_escolhida = st.selectbox("Obra", st.session_state.obras, key=f"obra_{row['codigo']}", label_visibility="collapsed")
                with col_acao3:
                    if st.button("Dar Baixa", key=f"btn_{row['codigo']}"):
                        st.success(f"Baixa de {qtd_baixa} un de {row['material']} registada para {obra_escolhida}!")
        else:
            st.info("Nenhum material encontrado com este código.")
    else:
        st.info("Ainda não existem sobras registadas.")

# ==========================================
# 2. FUNCIONÁRIOS
# ==========================================
elif menu == "Funcionários":
    st.title("👥 Gestão de Funcionários")
    st.write("Área dedicada ao registo e controlo de colaboradores.")
