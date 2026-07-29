import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="CLIMA POSITIVO - Gestão de Obra & Stock", layout="wide")

# Inicialização do Session State para persistência local (simulação/fallback)
if "df_sobras" not in st.session_state:
    st.session_state.df_sobras = pd.DataFrame(columns=["codigo", "material", "qtd", "local", "estado", "data"])

if "obras" not in st.session_state:
    st.session_state.obras = ["Obra Alpha", "Obra Central", "Residencial Parque", "Edifício Lumière"]

if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = ["João Silva", "Carlos Mendes", "António Santos"]

# --- MENU LATERAL (Sidebar) ---
st.sidebar.markdown("## **CLIMA POSITIVO**")
st.sidebar.caption("Controlo de Obra & Stock")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    ["Resumo", "Obras", "Estoque", "Movimentos", "Banco de Sobras", "Funcionários"],
    index=4 # Foca por predefinição no Banco de Sobras conforme pedido
)

# ==============================================================================
# 1. RESUMO
# ==============================================================================
if menu == "Resumo":
    st.title("📊 Resumo Geral")
    st.write("Visão geral do estado atual das obras, materiais e stock.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Obras", len(st.session_state.obras))
    with col2:
        total_sobras = st.session_state.df_sobras["qtd"].sum() if not st.session_state.df_sobras.empty else 0
        st.metric("Sobras em Armazém", f"{total_sobras} unidades")
    with col3:
        st.metric("Funcionários Registados", len(st.session_state.funcionarios))

# ==============================================================================
# 2. OBRAS
# ==============================================================================
elif menu == "Obras":
    st.title("🏗️ Gestão de Obras")
    st.write("Lista de obras ativas e respetivos locais de intervenção.")
    
    with st.form("form_obra", clear_on_submit=True):
        nova_obra = st.text_input("Nome da Nova Obra")
        btn_add_obra = st.form_submit_button("Adicionar Obra")
        if btn_add_obra and nova_obra:
            if nova_obra not in st.session_state.obras:
                st.session_state.obras.append(nova_obra)
                st.success(f"Obra '{nova_obra}' adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("Esta obra já se encontra registada.")
                
    st.markdown("### Obras Atuais")
    for o in st.session_state.obras:
        st.markdown(f"- 📌 {o}")

# ==============================================================================
# 3. ESTOQUE
# ==============================================================================
elif menu == "Estoque":
    st.title("📦 Gestão de Estoque")
    st.write("Controlo geral de materiais disponíveis no armazém e fornecimentos.")
    st.info("Consulte o **Banco de Sobras** para gerir os excedentes reutilizáveis.")

# ==============================================================================
# 4. MOVIMENTOS
# ==============================================================================
elif menu == "Movimentos":
    st.title("🔄 Registo de Movimentos")
    st.write("Histórico de entradas e saídas de materiais nas obras.")
    st.info("Pode dar baixa direta aos materiais através do **Banco de Sobras**.")

# ==============================================================================
# 5. BANCO DE SOBRAS (COM BUSCA POR CÓDIGO, SOMA DE ITENS E AUTO-PREENCHIMENTO)
# ==============================================================================
elif menu == "Banco de Sobras":
    st.title("♻️ Banco de Sobras e Materiais Excedentes")
    
    # --- FORMULÁRIO DE ENTRADA (REGISTAR SOBRA) ---
    with st.expander("➕ Disponibilizar Sobra para a Equipa / Registar Novo Material", expanded=True):
        with st.form("form_sobra_completo", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                codigo_input = st.text_input("CÓDIGO DO PRODUTO (Ex: P125, C250)")
                material_input = st.text_input("MATERIAL / NOME DO PRODUTO")
            with col2:
                qtd_input = st.number_input("QUANTIDADE", min_value=0.0, step=1.0, value=1.0)
                local_input = st.selectbox("LOCALIZAÇÃO ATUAL / OBRA", ["Armazém Central"] + st.session_state.obras)
                
            btn_submeter = st.form_submit_button("Disponibilizar Sobra para a Equipa")
            
            if btn_submeter:
                if not codigo_input or not material_input:
                    st.error("Por favor, preencha o código e o nome do material.")
                else:
                    # Validação: Impedir o uso do mesmo código se já existir na base de dados
                    if not st.session_state.df_sobras.empty and codigo_input in st.session_state.df_sobras["codigo"].values:
                        st.error(f"❌ Erro: O código '{codigo_input}' já se encontra cadastrado! Não é permitido usar códigos duplicados.")
                    else:
                        novo_reg = {
                            "codigo": codigo_input,
                            "material": material_input,
                            "qtd": qtd_input,
                            "local": local_input,
                            "estado": "Disponível",
                            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.df_sobras = pd.concat([st.session_state.df_sobras, pd.DataFrame([novo_reg])], ignore_index=True)
                        st.success("Sobra registada com sucesso!")
                        st.rerun()

    st.markdown("---")
    
    # --- SECÇÃO DE PESQUISA POR CÓDIGO E TABELA DE MATERIAIS EXCEDENTES ---
    st.subheader("Materiais Excedentes (Atuais e Histórico)")
    
    # Campo de Procura por Código (conforme solicitado)
    pesquisa_codigo = st.text_input("🔍 Procurar material (introduza o código do produto):", "")
    
    if not st.session_state.df_sobras.empty:
        df_exibicao = st.session_state.df_sobras.copy()
        
        # Filtrar por código se o utilizador escrever algo
        if pesquisa_codigo:
            df_exibicao = df_exibicao[df_exibicao["codigo"].astype(str).str.contains(pesquisa_codigo, case=False, na=False)]
        
        if not df_exibicao.empty:
            # Agrupamento automático e soma da quantidade de itens iguais
            df_agrupado = df_exibicao.groupby(["codigo", "material", "local", "estado"], as_index=False).agg({
                "qtd": "sum",
                "data": "max"
            })
            
            # Cabeçalhos da tabela
            h_cols = st.columns([1.2, 2.5, 1.2, 1.5, 1.2, 2.4])
            h_cols[0].markdown("**CÓDIGO**")
            h_cols[1].markdown("**MATERIAL**")
            h_cols[2].markdown("**QTD TOTAL**")
            h_cols[3].markdown("**LOCAL**")
            h_cols[4].markdown("**ESTADO**")
            h_cols[5].markdown("**AÇÃO (DAR BAIXA)**")
            
            for idx, row in df_agrupado.iterrows():
                c1, c2, c3, c4, c5, c6 = st.columns([1.2, 2.5, 1.2, 1.5, 1.2, 2.4])
                c1.text(row["codigo"])
                c2.text(row["material"])
                c3.text(f"{row['qtd']} un")
                c4.text(row["local"])
                c5.markdown('<span style="color:green; font-weight:bold;">Disponível</span>', unsafe_allow_html=True)
                
                with c6:
                    sub_cols = st.columns([1.2, 1.5, 1.5])
                    qtd_baixa = sub_cols[0].number_input("Qtd", min_value=0.0, max_value=float(row['qtd']), value=float(row['qtd']), key=f"q_{row['codigo']}_{idx}", label_visibility="collapsed")
                    obra_baixa = sub_cols[1].selectbox("Obra", st.session_state.obras, key=f"obra_{row['codigo']}_{idx}", label_visibility="collapsed")
                    if sub_cols[2].button("Dar Baixa", key=f"btn_{row['codigo']}_{idx}"):
                        # Efetuar baixa reduzindo do stock
                        st.success(f"Baixa de {qtd_baixa} un efetuada para {obra_baixa}!")
        else:
            st.info("Nenhum material encontrado com o código introduzido.")
    else:
        st.info("Ainda não existem sobras registadas.")

# ==============================================================================
# 6. FUNCIONÁRIOS
# ==============================================================================
elif menu == "Funcionários":
    st.title("👥 Gestão de Funcionários")
    st.write("Registo e listagem da equipa de colaboradores.")
    
    with st.form("form_func", clear_on_submit=True):
        novo_func = st.text_input("Nome do Funcionário")
        btn_add_func = st.form_submit_button("Registar Funcionário")
        if btn_add_func and novo_func:
            if novo_func not in st.session_state.funcionarios:
                st.session_state.funcionarios.append(novo_func)
                st.success(f"Funcionário '{novo_func}' registado com sucesso!")
                st.rerun()
            else:
                st.warning("Este funcionário já consta na lista.")
                
    st.markdown("### Equipa Atual")
    for f in st.session_state.funcionarios:
        st.markdown(f"- 👤 {f}")
