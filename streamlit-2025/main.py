import streamlit as st
import pandas as pd

def calc_general_stats(df):
    df_date = df.groupby(by="Data")[["Valor"]].sum()
    df_date["lag_1"] = df_date["Valor"].shift(1)
    df_date["Diferença Mensal Abs."] = df_date["Valor"] - df_date["lag_1"]
    df_date["Média 6M Diferença Mensal Abs."] = df_date["Diferença Mensal Abs."].rolling(6).mean()
    df_date["Média 12M Diferença Mensal Abs."] = df_date["Diferença Mensal Abs."].rolling(12).mean()
    df_date["Média 24M Diferença Mensal Abs."] = df_date["Diferença Mensal Abs."].rolling(24).mean()
    df_date["Diferença Mensal Rel."] = df_date["Valor"] / df_date["lag_1"] - 1
    df_date["Evolução 6M Total"] = df_date["Valor"].rolling(6).apply(lambda x: x[-1] - x[0])
    df_date["Evolução 12M Total"] = df_date["Valor"].rolling(12).apply(lambda x: x[-1] - x[0])
    df_date["Evolução 24M Total"] = df_date["Valor"].rolling(24).apply(lambda x: x[-1] - x[0])
    df_date["Evolução 6M Total Rel."] = df_date["Valor"].rolling(6).apply(lambda x: x[-1] / x[0] - 1)
    df_date["Evolução 12M Total Rel."] = df_date["Valor"].rolling(12).apply(lambda x: x[-1] / x[0] - 1)
    df_date["Evolução 24M Total Rel."] = df_date["Valor"].rolling(24).apply(lambda x: x[-1] / x[0] - 1)

    df_date = df_date.drop(["lag_1"], axis=1)

    return df_date

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

    exp3 = st.expander("Estatísticas gerais")

    df_stats = calc_general_stats(df)

    columns_config = {
        "Valor" : st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        "Diferença Mensal Abs." : st.column_config.NumberColumn("Diferença Mensal Abs.", format="R$ %.2f"),
        "Média 6M Diferença Mensal Abs." : st.column_config.NumberColumn("Média 6M Diferença Mensal Abs.", format="R$ %.2f"),
        "Média 12M Diferença Mensal Abs." : st.column_config.NumberColumn("Média 12M Diferença Mensal Abs.", format="R$ %.2f"),
        "Média 24M Diferença Mensal Abs." : st.column_config.NumberColumn("Média 24M Diferença Mensal Abs.", format="R$ %.2f"),
        "Evolução 6M Total" : st.column_config.NumberColumn("Evolução 6M Total", format="R$ %.2f"),
        "Evolução 12M Total" : st.column_config.NumberColumn("Evolução 12M Total", format="R$ %.2f"),
        "Evolução 24M Total" : st.column_config.NumberColumn("Evolução 24M Total", format="R$ %.2f"),
        "Diferença Mensal Rel." : st.column_config.NumberColumn("Diferença Mensal Rel.", format="percent"),
        "Evolução 6M Total Rel." : st.column_config.NumberColumn("Evolução 6M Total Rel.", format="percent"),
        "Evolução 12M Total Rel." : st.column_config.NumberColumn("Evolução 12M Total Rel.", format="percent"),
        "Evolução 24M Total Rel." : st.column_config.NumberColumn("Evolução 24M Total Rel.", format="percent"),
    }

    tab_stats, tab_abs, tab_rel = exp3.tabs(tabs=["Dados", "Histórico de evolução", "Crescimento relativo"])

    with tab_stats:
        st.dataframe(df_stats, column_config=columns_config)

    with tab_abs:
        abs_cols = [
            "Diferença Mensal Abs.",
            "Média 6M Diferença Mensal Abs.",
            "Média 12M Diferença Mensal Abs.",
            "Média 24M Diferença Mensal Abs.",
        ]
        st.line_chart(df_stats[abs_cols])

    with tab_rel:
        rel_cols = [
            "Diferença Mensal Rel.",
            "Evolução 6M Total Rel.",
            "Evolução 12M Total Rel.",
            "Evolução 24M Total Rel.",
        ]
        st.line_chart(df_stats[rel_cols])