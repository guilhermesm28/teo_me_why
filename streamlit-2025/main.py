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

if file_upload is not None:
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

    exp1 = st.expander("Dados brutos")
    columns_fmt = {
        "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
    }
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    exp2 = st.expander("Instituições")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição", values="Valor")
    exp2.dataframe(df_instituicao)