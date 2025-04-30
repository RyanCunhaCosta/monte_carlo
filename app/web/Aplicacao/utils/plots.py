from streamlit_echarts import st_echarts
import pandas as pd
import streamlit as st


def plot_carga_geracao(dataframe):
    chartOptions = {
        "tooltip": {
            "trigger": "axis",
        },
        "legend": {
            "data": [
                "Carga Prevista",
                "Geração Nuclear",
                "Geração Eólica",
                "Geração Solar",
                "Geração Hidrotérmica",
            ],
        },
        "grid": {
            "left": "5%",
            "right": "5%",
            "bottom": "10%",
        },
        "xAxis": [
            {
                "name": "Horário",
                "nameLocation": "middle",
                "nameGap": 20,
                "type": "category",
                "data": dataframe.index.tolist(),
            }
        ],
        "yAxis": [
            {
                "name": "Gigawatts",
                "nameLocation": "middle",
                "nameGap": 30,
                "type": "value",
            }
        ],
        "series": [
            {
                "name": "Carga Prevista",
                "type": "line",
                "data": dataframe["Carga"].values.tolist(),
                "smooth": 0.3,
            },
            {
                "name": "Geração Nuclear",
                "type": "bar",
                "data": dataframe["G_Nuclear"].values.tolist(),
                "stack": "geracao",
                "itemStyle": {"color": "#2a9d8f"},
            },
            {
                "name": "Geração Eólica",
                "type": "bar",
                "data": dataframe["G_Eolica"].values.tolist(),
                "stack": "geracao",
                "itemStyle": {"color": "#264653"},
            },
            {
                "name": "Geração Solar",
                "type": "bar",
                "data": dataframe["G_Solar"].values.tolist(),
                "stack": "geracao",
                "itemStyle": {"color": "#f4a261"},
            },
            {
                "name": "Geração Hidrotérmica",
                "type": "bar",
                "data": dataframe["G_HT_Obj"].values.tolist(),
                "stack": "geracao",
                "itemStyle": {"color": "#E76F51"},
            },
        ],
    }

    st_echarts(
        options=chartOptions,
    )


def plot_preco_horario(dataframe):
    chartOptions = {
        "tooltip": {
            "trigger": "axis",
        },
        "legend": {
            "data": [
                "CMO",
                "PLD",
            ],
        },
        "grid": {
            "left": "5%",
            "right": "5%",
            "bottom": "10%",
        },
        "xAxis": [
            {
                "name": "Horário",
                "nameLocation": "middle",
                "nameGap": 20,
                "type": "category",
                "data": dataframe.index.tolist(),
            }
        ],
        "yAxis": [
            {
                "name": "Preço (BRL)",
                "nameLocation": "middle",
                "nameGap": 30,
                "type": "value",
            }
        ],
        "series": [
            {
                "name": "PLD",
                "type": "line",
                "data": dataframe["Carga"].values.tolist(),
                "smooth": 0.3,
                "markLine": {
                    "silent": True,
                    "data": [
                        {
                            "yAxis": 20,
                            "label": {"position": "end", "formatter": "PLD Min"},
                        },
                        {
                            "yAxis": 40,
                            "label": {"position": "end", "formatter": "PLD Max"},
                        },
                    ],
                },
            },
            {
                "name": "CMO",
                "type": "line",
                "data": dataframe["Carga"].values.tolist(),
                "smooth": 0.3,
            },
        ],
    }

    st_echarts(
        options=chartOptions,
    )


def plot_curva_custo_incremental(
    parcela_base,
    parcela_linear,
    parcela_quadratica,
    geracao_min,
    geracao_max,
    key,
):
    custo = {}

    for p in range(int(geracao_min), int(geracao_max) + 1):
        custo[p] = parcela_base + parcela_linear * p + parcela_quadratica * p**2

    option = {
        "tooltip": {
            "trigger": "none",
            "axisPointer": {"type": "cross"},
        },
        "grid": {
            "top": "5%",
            "left": "10%",
            "right": "20%",
            "bottom": "15%",
            "containLabel": True,
        },
        "xAxis": [
            {
                "name": "Potência (MW)",
                "nameLocation": "middle",
                "nameGap": 30,
                "type": "category",
                "data": list(custo.keys()),
                # "minInterval": 100,
                # "min": "dataMin",
                # "max": "dataMax",
                "splitNumber": "2",
                "scale": True,
            }
        ],
        "yAxis": [
            {
                "name": "Custo",
                "nameLocation": "middle",
                "nameGap": 50,
                "type": "value",
                # "min": "dataMin",
                # "max": "dataMax",
                "splitNumber": "1",
                # "minInterval": 1,
                "scale": True,
            }
        ],
        "series": [
            {
                "name": "P. Gerada",
                "type": "line",
                "data": list(custo.values()),
                "itemStyle": {"color": "#1f77b4"},  # Azul
            },
        ],
    }

    try:
        st.markdown(
            "<h6 style='text-align: center;  padding: 0rem;'>Curva de Custo Incremental</h6>",
            unsafe_allow_html=True,
        )
        st_echarts(options=option, height="150px", key=key)
    except Exception:
        pass


def plot_curva_eficiencia(geracao_min, geracao_max, cte_perdas, key):
    geracao_total = {}
    perdas = {}
    geracao_liquida = {}

    for p in range(int(geracao_min), int(geracao_max) + 1):
        geracao_total[p] = round(p, 2)
        perdas[p] = round(cte_perdas * p**2, 2)
        geracao_liquida[p] = round(p - perdas[p], 2)

    option = {
        "tooltip": {
            "trigger": "none",
            "axisPointer": {"type": "cross"},
        },
        "grid": {
            "top": "5%",
            "left": "10%",
            "right": "20%",
            "bottom": "15%",
            "containLabel": True,
        },
        "xAxis": [
            {
                "name": "Potência (MW)",
                "nameLocation": "middle",
                "nameGap": 30,
                "type": "category",
                "data": list(geracao_total.keys()),
                "minInterval": 100,
                # "min": "dataMin",
                # "max": "dataMax",
                "splitNumber": 2,
                "scale": True,
            }
        ],
        "yAxis": [
            {
                "name": "Rendimento",
                "nameLocation": "middle",
                "nameGap": 30,
                "type": "value",
                "minInterval": 10,
                # "min": "dataMin",
                # "max": "dataMax",
                "splitNumber": 2,
                "scale": True,
            },
        ],
        "series": [
            {
                "name": "Líquida",
                "type": "line",
                "data": list(geracao_liquida.values()),
                "itemStyle": {"color": "#2ca02c"},  # Verde
            },
            {
                "name": "Perdas",
                "type": "line",
                "data": list(perdas.values()),
                "itemStyle": {"color": "#ff7f0e"},  # Laranja
            },
        ],
        "legend": {
            "top": "top",
            "left": "center",
            "itemGap": 2,
            "itemHeight": 2,
            "textStyle": {"fontSize": 10},
        },
    }

    try:
        st.markdown(
            "<h6 style='text-align: center;  padding: 0rem;'>Curva de Eficiência</h6>",
            unsafe_allow_html=True,
        )

        st_echarts(options=option, height="150px", key=key)
    except Exception:
        pass


def plot_tomada(dataframe, keys):
    series = []

    series.append(
        {
            "name": "CMO",
            "type": "line",
            "yAxisIndex": 1,
            "data": dataframe["CMO"].to_list(),
        }
    )

    series.append(
        {
            "name": "Potência Demandada",
            "type": "line",
            "data": dataframe.index.to_list(),
        }
    )

    stack = st.checkbox("Empilhar Potências Geradas", value=True)

    for col in keys:
        serie = {
            "name": col,
            "type": "bar",
            "stack": "total" if stack else False,
            "data": dataframe[col].to_list(),
        }

        series.append(serie)

    option = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": ["P1", "P2", "P3", "CMO", "Potência Demandada"]},
        "xAxis": {
            "type": "category",
            "name": "Potência Demandada",
            "data": dataframe.index.to_list(),
        },
        "yAxis": [
            {
                "type": "value",
                "name": "Potência Gerada (MW)",
                "max": "dataMax",
            },
            {
                "type": "value",
                "name": "CMO (BRL)",
                "position": "right",
            },
        ],
        "series": series,
    }

    st_echarts(options=option, height="400px")
