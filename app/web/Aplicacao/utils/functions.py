import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import time
import pandas as pd
from millify import millify

def simular_lote(probabilidades, tamanho, criterio_falha):
    np.random.seed()
    falhas = np.random.rand(tamanho, len(probabilidades)) < probabilidades
    numero_falhas = np.sum(falhas, axis=1)
    eventos_de_falha = np.sum(numero_falhas >= criterio_falha)
    return eventos_de_falha, tamanho


def monte_carlo(probabilidades, erro_obj, max_sim, min_sim, threads, lote_tamanho, criterio_falha):

    start = time.time()
    total_simulacoes = 0
    eventos_de_falha = 0
    simulacoes_hist = []
    lolp_hist = []
    lole_hist = []
    
    with st.container(border=True):
        
        status = st.empty()
        status.markdown(
        """
        ### 🟡 Resultados da Simulação
        """
        )
        colA,colB = st.columns([2,1],vertical_alignment="center")
                
        plot_placeholder = colA.empty()
        
        with colB:
            n_sim = st.empty()
            t_sim = st.empty()
            vl_erro = st.empty()
            lolp = st.empty()
            lole = st.empty()
            
        with ThreadPoolExecutor(max_workers=threads) as executor:
            while total_simulacoes < max_sim:
                futures = [executor.submit(simular_lote, probabilidades, int(lote_tamanho), criterio_falha) for _ in range(threads)]
                for future in futures:
                    falhas_lote, simulacoes_lote = future.result()
                    eventos_de_falha += falhas_lote
                    total_simulacoes += simulacoes_lote

                    LOLP = eventos_de_falha / total_simulacoes
                    LOLE = LOLP * 8760
                    simulacoes_hist.append(total_simulacoes)
                    lolp_hist.append(LOLP)
                    lole_hist.append(LOLE)
                    
                    erro_padrao = np.sqrt(LOLP * (1 - LOLP) / total_simulacoes)
                    
                    
                    n_sim.metric(label="Simulações", value=millify(total_simulacoes, precision=2, drop_nulls=False))
                    vl_erro.metric(label="Erro Padrão", value=f"{erro_padrao:.2e}")
                    lolp.metric(label="LOLP (%)", value=f"{LOLP*100:.4}")
                    lole.metric(label="LOLE (horas/ano)", value=f"{LOLE:.2f}",delta=f"{round(LOLE/365,2)} (dias/ano)",delta_color="off")
                    t_sim.metric(label="Tempo de Execução (segundos)", value=f"{time.time() - start:.2f}")
                    
                    fig, ax = plt.subplots()
                    ax.plot(simulacoes_hist, lolp_hist, label="LOLP")
                    ax.set_xlabel("Simulações")
                    ax.set_ylabel("LOLP")
                    ax.set_title("Convergência LOLP")
                    ax.grid(True)
                    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
                    plot_placeholder.pyplot(fig,use_container_width=True)
                    plt.close(fig) 

                    if total_simulacoes >= min_sim and erro_padrao < erro_obj:
                        status.markdown(
                        """
                        ### 🟢 Resultados da Simulação
                        """
                        )
                        return



