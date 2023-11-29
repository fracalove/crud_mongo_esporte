from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_alunoEG import Controller_AlunoEG
from controller.controller_esporteEG import Controller_EsporteEG
from controller.controller_professorEG import Controller_ProfessorEG


tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_aluno = Controller_AlunoEG()
ctrl_esporte = Controller_EsporteEG()
ctrl_professor = Controller_ProfessorEG()


def reports(opcao_relatorio: int = 0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_alunos_esporte()
    elif opcao_relatorio == 2:
        relatorio.get_alunos()
    elif opcao_relatorio == 3:
        relatorio.get_professores()
    elif opcao_relatorio == 4:
        relatorio.get_esportes()


def inserir(opcao_inserir: int = 0):

    if opcao_inserir == 1:
        novo_aluno = ctrl_aluno.inserir_aluno()
    elif opcao_inserir == 2:
        novo_esporte = ctrl_esporte.inserir_esporte()
    elif opcao_inserir == 3:
        novo_professor = ctrl_professor.inserir_professor()


def atualizar(opcao_atualizar: int = 0):
    if opcao_atualizar == 1:
        aluno_atualizado = ctrl_aluno.atualizar_aluno()
    elif opcao_atualizar == 2:
        esporte_atualizado = ctrl_esporte.atualizar_esporte()
    elif opcao_atualizar == 3:
        professor_atualizado = ctrl_professor.atualiza_professor()


def excluir(opcao_excluir: int = 0):
    if opcao_excluir == 1:
        ctrl_aluno.excluir_aluno()
    elif opcao_excluir == 2:
        ctrl_esporte.excluir_esporte()
    elif opcao_excluir == 3:
        ctrl_professor.excluir_professor()


def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)

        if opcao == 1:  # Relatórios

            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-2]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2:  # Inserir Novos Registros

            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3:  # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:  # Remover Registros

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)


if __name__ == "__main__":
    run()
