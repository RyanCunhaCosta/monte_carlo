import streamlit as st
from app.web.Aplicacao.utils.widgets import *
from app.web.Aplicacao.utils.functions import *

def app():
    colA, colB = st.columns([3,7])
    
    with colB:
        probabilidades, tamanho = inputs_probabilidades()
        
    with colA:
        erro_obj, criterio_falha= inputs_mc(tamanho)
        threads, lote_tamanho, min_sim,max_sim = inputs_ex()
        
    if colA.button(
        "**EXECUTAR SIMULAÇÃO**",
        help="Executar Simulação de Monte Carlo Não Sequencial.",
        use_container_width=True,
        type="primary"
    ):
        with colB:
            
            monte_carlo(
                probabilidades=probabilidades,
                erro_obj=erro_obj,
                max_sim=max_sim,
                min_sim=min_sim,
                threads=threads,
                lote_tamanho=lote_tamanho,
                criterio_falha=criterio_falha,
            )