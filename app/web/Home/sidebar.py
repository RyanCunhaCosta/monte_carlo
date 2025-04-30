import streamlit as st
from streamlit_option_menu import option_menu


class MultiApp:
    def __init__(self):
        self.apps = []

        st.set_page_config(
            page_title="PSE - SMCNS",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def add_app(self, title, func, icon):
        self.apps.append({"title": title, "function": func, "icon": icon})

        self.titles = [item["title"] for item in self.apps]
        self.functions = [item["function"] for item in self.apps]
        self.icons = [item["icon"] for item in self.apps]

    def page_select(self):
        with st.sidebar:
            selected = option_menu(
                menu_title=None,
                options=self.titles,
                icons=self.icons,
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
                styles={
                    "container": {
                        "padding": "0!important",
                        # "background-color": "#fafafa",
                    },
                    "nav-link": {
                        "font-size": "15px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#0077a3",
                    },
                    "nav-link-selected": {"background-color": "#004877"},
                },
            )

            app = {
                "title": selected,
                "function": self.functions[self.titles.index(selected)],
            }

            return app

    def run(self, app):
        st.sidebar.markdown(
            """
        <style>
        .st-emotion-cache-1jicfl2 {padding: 4rem 1rem;}
        </style>
        """,
            unsafe_allow_html=True,
        )

        app["function"]()

    def capa(self, disciplina, titulo, subtitulo):
        st.sidebar.markdown(
            """
        <style>
        .st-emotion-cache-1mi2ry5 {padding: 0rem 0rem;}
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.sidebar.markdown(
            """
        <style>
        .st-emotion-cache-qeahdt {padding: 0rem 1rem;}
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.sidebar.image(
            "app/web/Home/UFRJ.png",
            caption=disciplina,
        )

        st.sidebar.markdown(
            f"<h1 style='text-align: center;  padding: 0rem;'>{titulo}</h1>",
            unsafe_allow_html=True,
        )

        st.sidebar.markdown(
            f"<p style='text-align: center; '>{subtitulo}</p>",
            unsafe_allow_html=True,
        )

    def participantes(self, grupo, integrantes, professor):
        st.sidebar.write("---")

        st.sidebar.markdown(
            f"<h2 style='text-align: center;  padding: 0rem 0rem 1rem ;'>{grupo}</h2>",
            unsafe_allow_html=True,
        )

        for nome, dre in integrantes.items():
            st.sidebar.markdown(
                f"<h4 style='text-align: center;  padding:0 ;'>{nome}</h4>",
                unsafe_allow_html=True,
            )

            st.sidebar.markdown(
                f"<h6 style='text-align: center; padding: 0rem 0rem 1rem;'>{dre}</h6>",
                unsafe_allow_html=True,
            )

        st.sidebar.markdown(
            f"<p style='text-align: center; padding: 0rem 0rem 1rem; font-style: italic;'>{professor}</p>",
            unsafe_allow_html=True,
        )
