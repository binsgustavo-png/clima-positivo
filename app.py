import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="CLIMA POSITIVO - Gestão de Obra & Stock", layout="wide")

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
    st.session_state.obras = ["Obra Alpha", "Obra Central", "Residencial Parque", "Edifício Lumière"]

if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = ["João Silva", "Carlos Mendes", "António Santos"]

st.sidebar.markdown("## **CLIMA POSITIVO**")
st.sidebar.caption("Controlo de Obra & Stock")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    ["Resumo", "Obras", "Estoque", "Movimentos", "Banco de Sobras", "Funcionários"],
    index=4
)

if menu == "Resumo":
    st.title("📊 Resumo Geral")
    df_atual = carregar_dados()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Obras", len(st.session_state.obras))
    with col2:
        total_sobras = df_atual["qtd"].sum() if not df_atual.empty else 0
        st.metric("Sobras em Armazém", f"{total_sobras} unidades")
    with col3:
        st.metric("Funcionários Registados", len(st.session_state.funcionarios))

elif menu == "Obras":
    st.title("🏗️ Gestão de Obras")
    with st.form("form_obra", clear_on_submit=True):
        nova_obra = st.text_input("Nome da Nova Obra")
        if st.form_submit_button("Adicionar Obra") and nova_obra:
            if nova_obra not in st.session_state.obras:
                st.session_state.obras.append(nova_obra)
                st.success("Obra adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("Esta obra já existe.")
    for o in st.session_state.obras:
        st.markdown(f"- 📌 {o}")

elif menu == "Estoque":
    st.title("📦 Gestão de Estoque")
    st.info("Consulte o **Banco de Sobras** para gerir os excedentes.")

elif menu == "Movimentos":
    st.title("🔄 Registo de Movimentos")
    st.info("Consulte o **Banco de Sobras** para dar baixa aos materiais.")

elif menu == "Banco de Sobras":
    st.title("♻️ Banco de Sobras e Materiais Excedentes")
    
    with st.expander("➕ Registar Novo Material / Sobra", expanded=True):
        with st.form("form_sobra", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                codigo_input = st.text_input("CÓDIGO DO PRODUTO")
                material_input = st.text_input("NOME DO MATERIAL")
            with col2:
                qtd_input = st.number_input("QUANTIDADE", min_value=0.0, step=1.0, value=1.0)
                local_input = st.selectbox("LOCALIZAÇÃO", ["Armazém Central"] + st.session_state.obras)
                
            if st.form_submit_button("Disponibilizar Sobra"):
                if not codigo_input or not material_input:
                    st.error("Preencha o código e o nome.")
                else:
                    df_atual = carregar_dados()
                    if not df_atual.empty and codigo_input in df_atual["codigo"].astype(str).values:
                        st.error(f"❌ O código '{codigo_input}' já está registado!")
                    else:
                        novo = {
                            "codigo": codigo_input,
                            "material": material_input,
                            "qtd": qtd_input,
                            "local": local_input,
                            "estado": "Disponível",
                            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        df_novo = pd.concat([df_atual, pd.DataFrame([novo])], ignore_index=True)
                        guardar_dados(df_novo)
                        st.success("Sobra registada e gravada com sucesso!")
                        st.rerun()

    st.markdown("---")
    st.subheader("Materiais Excedentes (Atuais e Histórico)")
    
    pesquisa_codigo = st.text_input("🔍 Procurar material por CÓDIGO:", "")
    df_dados = carregar_dados()
    
    if not df_dados.empty:
        if pesquisa_codigo:
            df_dados = df_dados[df_dados["codigo"].astype(str).str.contains(pesquisa_codigo, case=False, na=False)]
        
        if not df_dados.empty:
            df_agrupado = df_dados.groupby(["codigo", "material", "local", "estado"], as_index=False).agg({
                "qtd": "sum",
                "data": "max"
            })
            
            h = st.columns([1.2, 2.5, 1.2, 1.5, 1.2, 2.4])
            h[0].markdown("**CÓDIGO**")
            h[1].markdown("**MATERIAL**")
            h[2].markdown("**QTD TOTAL**")
            h[3].markdown("**LOCAL**")
            h[4].markdown("**ESTADO**")
            h[5].markdown("**AÇÃO**")
            
            for idx, row in df_agrupado.iterrows():
                c1, c2, c3, c4, c5, c6 = st.columns([1.2, 2.5, 1.2, 1.5, 1.2, 2.4])
                c1.text(row["codigo"])
                c2.text(row["material"])
                c3.text(f"{row['qtd']} un")
                c4.text(row["local"])
                c5.markdown('<span style="color:green; font-weight:bold;">Disponível</span>', unsafe_allow_html=True)
                
                with c6:
                    sub = st.columns([1.2, 1.5, 1.5])
                    q_baixa = sub[0].number_input("Q", min_value=0.0, max_value=float(row['qtd']), value=float(row['qtd']), key=f"q_{row['codigo']}_{idx}", label_visibility="collapsed")
                    o_baixa = sub[1].selectbox("O", st.session_state.obras, key=f"o_{row['codigo']}_{idx}", label_visibility="collapsed")
                    if sub[2].button("Dar Baixa", key=f"b_{row['codigo']}_{idx}"):
                        df_f = carregar_dados()
                        mask = df_f["codigo"].astype(str) == str(row['codigo'])
                        if any(mask):
                            total_q = df_f.loc[mask, "qtd"].sum()
                            restante = total_q - q_baixa
                            if restante <= 0:
                                df_f = df_f[~mask]
                            else:
                                idx_p = df_f[mask].index[0]
                                df_f.loc[idx_p, "qtd"] = restante
                                df_f = df_f.drop(df_f[mask].index[1:])
                            guardar_dados(df_f)
                            st.success("Baixa efetuada com sucesso!")
                            st.rerun()
        else:
            st.info("Nenhum material encontrado com esse código.")
    else:
        st.info("Ainda não existem sobras registadas.")

elif menu == "Funcionários":
    st.title("👥 Gestão de Funcionários")
    with st.form("form_func", clear_on_submit=True):
        novo_f = st.text_input("Nome do Funcionário")
        if st.form_submit_button("Registar") and novo_f:
            if novo_f not in st.session_state.funcionarios:
                st.session_state.funcionarios.append(novo_f)
                st.success("Funcionário registado!")
                st.rerun()
            else:
                st.warning("Funcionário já existe.")
    for f in st.session_state.funcionarios:
        st.markdown(f"- 👤 {f}")
