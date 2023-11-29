from conexion.mongo_queries import MongoQueries
from controller.controller_esporteEG import Controller_EsporteEG
from model.esporteEG import EsporteEG
from model.professoresEG import ProfessoresEG
import pandas as pd
from reports.relatorios import Relatorio

relatorio = Relatorio()

class Controller_ProfessorEG:
    def __init__(self):
        self.ctrl_esporte = Controller_EsporteEG()
        self.mongo = MongoQueries()

    def inserir_professor(self) -> ProfessoresEG:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_professores()
        # Solicita ao usuário o id_professor que deseja inserir
        id_professor = int(input("Digite o id_professor (NOVO): "))

        if self.verifica_existencia_professor(id_professor):
            # Solicita ao usuário os dados para preencher o novo professor
            nome = input("Nome do professor (NOVO): ")
            qtde_turmas = int(
                input("Quantidade de turmas do professor (NOVO): "))

            id_esporte = int(input("id_esporte que o professor da aula: "))

            esporte = self.valida_esporte(id_esporte)
            if esporte == None:
                return None

            self.mongo.db["professoresEG"].insert_one(
                {"id_professor": id_professor, "nome": nome, "qtde_turmas": qtde_turmas, "id_esporte": id_esporte})

            # Recupera os dados do novo Professor criando transformando em um DataFrame
            df_professor = self.recupera_professor(id_professor)

            # Cria um novo objeto Professor
            novo_professor = ProfessoresEG(
                id_professor, df_professor.nome.values[0], df_professor.qtde_turmas.values[0], esporte)

            # Exibe os atributos do Professor
            print(novo_professor.to_string())
            # Retorna o objeto novo_professor para utilização posterior, caso necessário
            return novo_professor
        else:
            print(
                f"Professor com id_professor = {id_professor} já cadastrado!")

    def atualiza_professor(self) -> ProfessoresEG:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_professores()
        # Solicita ao usuário o id_professor do professor a ser atualizado
        id_professor = int(
            input("id do professor que deseja alterar os dados: "))

        # Verifica a existencia do professor no banco
        if not self.verifica_existencia_professor(id_professor):
            # Solicita ao usuário os novos dados do professor
            nome = input("Nome do professor (NOVO): ")
            qtde_turmas = int(input("Quantidade de turmas do professor: "))
            id_esporte = int(input("Id do esporte que o professor da aula: "))

            # faz a validação para ver se o esporte existe na base de dados
            esporte = self.valida_esporte(id_esporte)
            if esporte == None:
                return None

            self.mongo.db["professoresEG"].update_one({"id_professor": id_professor}, {
                                                      "$set": {"nome": nome, "qtde_turmas": qtde_turmas, "id_esporte": id_esporte}})

            # Recupera os dados do novo professor criado transformando em um DataFrame
            df_professor = self.recupera_professor(id_professor)

            # Cria um novo objeto ProfessoresEG
            professor_atualizado = ProfessoresEG(
                id_professor, df_professor.nome.values[0], df_professor.qtde_turmas.values[0], esporte)

            # Exibe os dados do professor atualizado
            print(professor_atualizado.to_string())
            return professor_atualizado

        else:
            print(f"O professor de id = {id_professor} não existe no banco! ")
            return None

    def excluir_professor(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_professores()
        # Solicita ao usuário o id_professor que deseja excluir
        id_professor = int(input("Id do professor que deseja excluir: "))

        # Verifica a existencia do professor
        if not self.verifica_existencia_professor(id_professor):
            # Recupera os dados do professor transformando em um DataFrame
            df_professor = self.recupera_professor(id_professor)

            # Valida id_esporte
            esporte = self.valida_esporte(df_professor.id_esporte.values[0])

            opcao_excluir = input(
                f"Tem certeza que deseja excluir o professor {df_professor.nome.values[0]} [S ou N]: ")

            if opcao_excluir in "Ss":
                # Remove o professor da tabela
                self.mongo.db["professoresEG"].delete_one(
                    {"id_professor": id_professor})

                # faz a validação para ver se o esporte existe na base de dados
                esporte = self.valida_esporte(int(
                    df_professor.id_esporte.values[0]))
                if esporte == None:
                    return None

                # Cria um novo objeto ProfessoresEG
                professor_excluido = ProfessoresEG(
                    id_professor, df_professor.nome.values[0], df_professor.qtde_turmas.values[0], esporte)

                print("Professor removido! ")
                print(professor_excluido.to_string())

        else:
            print(
                f"O professor de id = {id_professor} não está na base de dados ")

    def valida_esporte(self, id_esporte: int = None) -> EsporteEG:
        if self.ctrl_esporte.verifica_existencia_esporte(id_esporte):
            print(f"O esporte {id_esporte} informado não existe na base de dados")
            return None
        else:
            self.mongo.connect()
            # recupera os dados do esporte transformando em um dataFrame
            df_esporte = self.ctrl_esporte.recupera_esporte(id_esporte)

            # Cria um novo objeto EsporteEG
            esporte = EsporteEG(
                df_esporte.id_esporte.values[0], df_esporte.nome.values[0], df_esporte.coordenador.values[0])
            return esporte

    def verifica_existencia_professor(self, id_professor: int = None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo professor criado transformando em um DataFrame
        df_professor = pd.DataFrame(self.mongo.db["professoresEG"].find(
            {"id_professor": f"{id_professor}"}, {"id_professor": 1, "nome": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_professor.empty

    def recupera_professor(self, id_professor: int = None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo professor criado transformando em um DataFrame
        df_professor = pd.DataFrame(list(self.mongo.db["esporteEG"].find(
            {"id_professor": f"{id_professor}"}, {"id_professor": 1, "nome": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_professor
