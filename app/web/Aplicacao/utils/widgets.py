import streamlit as st
import numpy as np

def inputs_ex():
    with st.container(border=True):
        st.markdown(
        """
        ###### Configurações de Execução
        """
    )
        
        colA, colB = st.columns([3, 3], vertical_alignment="center")
        
        min_sim = colA.number_input("Minimo de Simulações",
                        min_value=1e6,
                        value=1e6,
                        step=1e6,
                        format="%.2e",
                        help="Número mínimo de simulações para o critério de parada.",
                        key="min_simulacoes",
                        )
        
        max_sim = colB.number_input("Máximo de Simulações",
                                min_value=1e6,
                                value=1e24,
                                step=1e6,
                                format="%.2e",
                                help="Número máximo de simulações para o critério de parada.",
                                key="num_simulacoes",
                        )
        
        
        threads = int(colA.number_input("Paralelismo (Threads)",
                        min_value=1,
                        max_value=16,
                        value=4,
                        step=1,
                        help="Número de threads para processamento paralelo.",
                        key="threads",
                        ))
        
        lote_tamanho = colB.number_input("Tamanho do Lote",
                        min_value=1e6,
                        value=1e6,
                        step=1e6,
                        format="%.2e",
                        help="Número de simulações por lote.",
                        key="lote_tamanho",
                        )
        
        

        
        
    return threads, lote_tamanho, min_sim, max_sim

def inputs_mc(n_comp):
    with st.container(border=True):
        st.markdown(
        """
        ###### Critérios de Simulação
        """
    )   
        
        colA, colB = st.columns([3, 3], vertical_alignment="center")
        
        stop_type = colA.selectbox("Critério de Parada",
                    options=["Erro Absoluto"],
                    index=0,
                    help="Critério de parada para a simulação.",
                    key="criterio_parada",
                    )
        
        match stop_type:
            case "Erro Absoluto":
                erro_obj = colB.number_input("Erro Absoluto",
                                min_value=1e-10,
                                value=1e-7,
                                step=1e-10,
                                format="%.2e",
                                help="Erro absoluto para o critério de parada.",
                                key="erro_absoluto",
                                )
                
        fail_type = colA.selectbox("Critério de Falha Crítica",
                    options=["Percentual de Falha"],
                    index=0,
                    help="Condição de falha crítica para o sistema.",
                    key="tipo_parada",
                    )
                
        match fail_type:
            case "Percentual de Falha":
                criterio_falha = colB.number_input("Falha Crítica (%)",
                        min_value=1.0,
                        max_value=100.0,
                        value=5.0,
                        step=1.0,
                        help="Critério de falha para o sistema em porcentagem.",
                        key="criterio_falha",
                        )
                
                criterio_falha =int(criterio_falha/n_comp)
        
    return erro_obj, criterio_falha

def add_component():
    st.session_state.inputs.append(st.session_state.inputs[-1])

def remove_component():
    st.session_state.inputs.pop(-1)

def inputs_probabilidades():
    """
    Função para criar inputs dinâmicos para componentes de geração.
    """

    ctgs = {
    "Gerador": 1.1e-2,
    "Linha": 8.3e-4,
    "Trafo": 5.0e-4,
    }
    
    if "inputs" not in st.session_state:
        st.session_state["inputs"] = [{"componente": "Gerador", "quantidade": 5, "contingencia": ctgs["Gerador"]},
                                      {"componente": "Linha", "quantidade": 17, "contingencia": ctgs["Linha"]},
                                      {"componente": "Trafo", "quantidade": 3, "contingencia": ctgs["Trafo"]}]

    with st.container(border=True):
        st.markdown(
        """
        ### Componentes do Sistema
        """
    )
        for item in range(len(st.session_state.inputs)):
            colA,colB,colC,colD,colE = st.columns([4, 4, 5, 3, 1],vertical_alignment="bottom")
            
            componente = colA.selectbox(
                "Tipo de Componente",
                options=["Gerador", "Linha", "Trafo"],
                index=["Gerador", "Linha", "Trafo"].index(st.session_state.inputs[item]["componente"]),
                key=f"componente_{item}",
                help="Selecione o tipo de componente que será considerado na análise de contingência.",
            )
            
            ctg = colB.number_input(
                "Risco de Contingência",
                min_value=0.0,
                key=f"contingencia_{item}",
                value=ctgs[componente],
                format="%.2e",
                help=f"Probabilidade estimada de falha para um {componente}: {ctgs[componente]:.2e}.",
            )

            identificador = colC.text_input(
                "Identificador",
                value=f"{componente}_{item}",
                key=f"identificador_{item}",
                help="Nome ou código que identifica unicamente o grupo no sistema.",
            )

            qtd = colD.number_input(
                "Quantidade",
                min_value=1,
                step=1,
                value=st.session_state.inputs[item]["quantidade"],
                key=f"quantidade_{item}",
                help=f"Número total de componentes do tipo '{componente}' incluídos na análise.",
            )
            
            st.session_state.inputs[item] = {
                "componente": componente,
                "identificador": identificador,
                "quantidade": qtd,
                "contingencia": ctg,
            }
            
            if item == len(st.session_state.inputs) - 1:
                colE.button("", key=f"remove_{item}", disabled=item==0, on_click=remove_component,icon="➖",help="Remover Componente.")
        
        centered = st.columns([3, 2, 3])
        centered[1].button("Adicionar Componente", key="add_item", on_click=add_component, icon="➕")

    return [val for item in st.session_state.inputs for val in [item["contingencia"]] * item["quantidade"]], len(st.session_state.inputs)


    