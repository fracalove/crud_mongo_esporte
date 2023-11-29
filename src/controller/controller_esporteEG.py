import pandas as pd
from model.esporteEG import EsporteEG
from conexion.mongo_queries import MongoQueries
from reports.relatorios import Relatorio

relatorio = Relatorio()

class Controller_EsporteEG:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_esporte(self) -> EsporteEG:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_esportes()
        id_esporte = input("id do esporte (NOVO): ")

        # Verifica se o esporte existe na base de dados
        if self.verifica_existencia_esporte(id_esporte):
            nome = input("nome do esporte (novo): ")
            coordenador = input("nome do coordenador: ")

            self.mongo.db["esporteEG"].insert_one(
                {"id_esporte": id_esporte, "nome": nome, "coordenador": coordenador})

            df_esporte = self.recupera_esporte(id_esporte)

            novo_esporte = EsporteEG(
                id_esporte, df_esporte.nome.values[0], df_esporte.coordenador.values[0])

            print(novo_esporte.to_string())
            self.mongo.close()
            # Retorna o objeto novo_esporte para utilização posterior, caso necessário
            return novo_esporte
        else:
            self.mongo.close()
            print(f"O esporte de id {id_esporte} ja esta cadastrado")
            return None

    def atualizar_esporte(self) -> EsporteEG:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_esportes()
        id_esporte = input("Id do esporte que deseja atualizar os dados: ")

        # Verifica se o esporte existe na base de dados
        if not self.verifica_existencia_esporte(id_esporte):
            # solicita a nova descriçao do esporte
            novo_nome_esporte = input("Novo nome do Esporte: ")
            novo_nome_coordenador = input("Novo nome do coordenador: ")

            # Atualiza o nome do esporte existente
            self.mongo.db["esporteEG"].update_one({"id_esporte": f"{id_esporte}"}, {
                                                "set": {"nome": novo_nome_esporte}})

            self.mongo.db["esporteEG"].update_one({"id_esporte": f"{id_esporte}"}, {
                                                "set": {"coordenador": novo_nome_coordenador}})

            # Recupera os dados do novo esporte criado transformando em um DataFrame
            df_esporte = self.recupera_esporte(id_esporte)

            # Cria um novo obejto esporte
            esporte_atualizado = EsporteEG(
                id_esporte, df_esporte.nome.values[0], df_esporte.coordenador.values[0])

            # Exibe os atributos do novo esporte
            print(esporte_atualizado.to_string())
            # Retorna o objeto esporte_atualizado para utilização posterior, caso necessário
            return esporte_atualizado
        else:
            print(f"O id_esporte {id_esporte} não existe.")
            return None

    def excluir_esporte(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_esportes()
        id_esporte = input("Id do esporte que deseja excluir: ")

        # Verifica se o esporte existe na base de dados
        if not self.verifica_existencia_esporte(id_esporte):

            # Recupera os dados do novo esporte criado transformando em um DataFrame
            df_esporte = self.recupera_esporte(id_esporte)

            opcao_excluir = input(
                f"Tem certeza que deseja excluir o esporte {df_esporte.nome.values[0]} [S ou N]: ")

            if opcao_excluir in "Ss":
                # Pede uma confirmação ao usuário
                print(
                    "Atenção, caso o esporte possua professores ou alunos vinculados, também serão excluídos")
                opcao_excluir = input(
                    f"Tem certeza que deseja excluir o esporte {df_esporte.nome.values[0]} [S ou N]: ")

                if opcao_excluir in "Ss":

                    # Remove o esporte da tabela e as entidades que possuem alguma referência com o esporte
                    self.mongo.db["AlunosEG"].delete_one(
                        {"id_esporte": f"{id_esporte}"})

                    self.mongo.db["ProfessoresEG"].delete_one(
                        {"id_esporte": f"{id_esporte}"})

                    self.mongo.db["EsporteEG"].delete_one(
                        {"id_esporte": f"{id_esporte}"})

                    # Cria um novo obejto esporte exlcuido
                    esporte_excluido = EsporteEG(
                        id_esporte, df_esporte.nome.values[0], df_esporte.coordenador.values[0])

                    # Exibe os atributos do esporte excluido
                    print(esporte_excluido.to_string())
        else:
            print(f"O id_esporte {id_esporte} não existe.")

    def verifica_existencia_esporte(self, id_esporte: int = None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo esporte criado transformando em um DataFrame
        df_esporte = pd.DataFrame(self.mongo.db["esporteEG"].find(
            {"id_esporte": f"{id_esporte}"}, {"id_esporte": 1, "nome": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_esporte.empty

    def recupera_esporte(self, id_esporte: int = None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo esporte criado transformando em um DataFrame
        df_esporte = pd.DataFrame(list(self.mongo.db["esporteEG"].find(
            {"id_esporte": f"{id_esporte}"}, {"id_esporte": 1, "nome": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_esporte
