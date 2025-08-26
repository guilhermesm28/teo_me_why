import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Finanças",
    page_icon="💰",
)

st.markdown(
    """
    # Boas-vindas!

    Bem-vindo ao aplicativo de finanças pessoais!

    Este aplicativo foi desenvolvido com o objetivo de auxiliar na gestão financeira pessoal, permitindo o controle de gastos, receitas e investimentos.
    """
)

file_upload = st.file_uploader("Selecione um arquivo CSV", type=["csv"])

# Verifica se o arquivo foi carregado
if file_upload is not None:
    # Lê o arquivo CSV
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

    # Visão dos dados brutos
    exp1 = st.expander("Dados brutos")
    columns_fmt = {
        "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
    }
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    # Visão das instituições
    exp2 = st.expander("Instituições")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição", values="Valor")

    #  Abas para diferentes visualizações
    tab_data, tab_history, tab_share = exp2.tabs(["Dados", "Histórico", "Distribuição"])

    with tab_data:
        st.dataframe(df_instituicao)

    with tab_history:
        st.line_chart(df_instituicao)

    with tab_share:
        date = st.date_input("Data para distribuição", min_value=df_instituicao.index.min(), max_value=df_instituicao.index.max())

        if date not in df_instituicao.index:
            st.warning("Entre com uma data válida")
        else:
            st.bar_chart(df_instituicao.loc[date])

    df_date = df.groupby(by="Data")[["Valor"]].sum()
    df_date["lag_1"] = df_date["Valor"].shift(1)
    df_date["Diferença mensal"] = df_date["Valor"] - df_date["lag_1"]
    st.dataframe(df_date)