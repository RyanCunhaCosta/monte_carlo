from app.web.Home import sidebar
from app.web.Aplicacao import aplicacao

app = sidebar.MultiApp()

app.capa(
    disciplina = "Planejamento de Sistêmas Energéticos - EEE609",
    titulo = "Confiabilidade Composta",
    subtitulo = "Simulação de Monte Carlo Não Sequencial",
)

paginas = [
    {
        "title": "Aplicação",
        "import_path": aplicacao.app,
        "icon": "bi bi-graph-up",
    },
]

for pagina in paginas:
    app.add_app(pagina["title"], pagina["import_path"], pagina["icon"])

# selected_app = app.page_select()

app.participantes(
    grupo="Grupo 7",
    integrantes = {
        "Fernanda Quissak Bernardo": "118141641",
        "Pedro Henrique Guedes": "117251817",
        "Ryan Cunha Costa": "119153675",
        "Ravi Bueno Mendonça Fochi": "119160004",
    },
    professor="Carmen Lúcia Tancredo Borges D.Sc.",
)

# app.run(selected_app)
aplicacao.app()
