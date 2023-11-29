from model.alunoEG import AlunoEg
from model.esporteEG import EsporteEG
from controller.controller_esporteEG import Controller_EsporteEG
from conexion.mongo_queries import MongoQueries
import pandas as pd
from reports.relatorios import Relatorio

relatorio = Relatorio()

class Controller_AlunoEG:
    def __init__(self):
        self.ctrl_esporte = Controller_EsporteEG()
        self.mongo = MongoQueries()

    def inserir_aluno(self) -> AlunoEg:

        # Cria uma no   va conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_alunos()
        # Solicita ao usuario o novo CPF
        cpf = input("CPF (NOVO): ")

        if self.verifica_existencia_aluno(cpf):
            # Solicita os dados do novo aluno ao usuario
            matricula = input("Matricula: ")
            nome = input("Nome do Aluno: ")
            relatorio.get_esportes()
            id_esporte = input("id do esporte: ")

            esporte = self.valida_esporte(id_esporte)
            if esporte == None:
                return None

            self.mongo.db["alunosEG"].insert_one(
                {"matricula": matricula, "nome": nome, "cpf": cpf, "id_esporte": id_esporte})

            # Recupera os dados do novo Aluno criando transformando em um DataFrame
            df_aluno = self.recupera_aluno(cpf)

            # Cria um novo objeto Aluno
            novo_aluno = AlunoEg(
                df_aluno.matricula.values[0], df_aluno.nome.values[0], df_aluno.cpf, esporte)

            # Exibe os atributos do Aluno
            print(novo_aluno.to_string())
            # Retorna o objeto novo_aluno para utilização posterior, caso necessário
            return novo_aluno
        else:
            print(f"Aluno com cpf {cpf} já está cadastrado!")

    def atualizar_aluno(self) -> AlunoEg:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_alunos()
        # Solicita ao usuário o cpf do Aluno a ser alterado
        cpf = input("Cpf do aluno que deseja alterar os dados: ")

        # se o aluno existir
        if not self.verifica_existencia_aluno(cpf):

            # solicita ao usuario os dados do aluno a ser atualizado
            nome = input("Nome (NOVO): ")
            id_esporte = input("id do esporte: (NOVO)")

            # faz a validação para ver se o esporte existe na base de dados
            esporte = self.valida_esporte(id_esporte)
            if esporte == None:
                return None

            # Atualiza os Dados do Aluno
            self.mongo.db["alunosEG"].update_one(
                {"cpf": cpf}, {"$set": {"nome": nome, "id_esporte": esporte.get_id_esporte()}})

            # Recupera os dados do novo aluno criado transformando em um DataFrame
            df_aluno = self.recupera_aluno(cpf)

            # Cria um novo objeto AlunosEG
            aluno_atualizado = AlunoEg(
                df_aluno.matricula.values[0], df_aluno.nome.values[0], df_aluno.cpf.values[0], esporte)

            # Exibe os atributos do aluno_atualizado
            print(aluno_atualizado.to_string())

            # Retorna o objeto aluno_atualizado para utilização posterior, caso necessário
            return aluno_atualizado
        else:
            print(f"O aluno de cpf {cpf} não está na base de dados")
            return None

    def excluir_aluno(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        relatorio.get_alunos()
        # Solicita ao usuário o cpf do aluno a ser excluído
        cpf = input("Cpf do aluno que deseja excluir: ")

        # Verifica se o Aluno existe na base de dados
        if not self.verifica_existencia_aluno(cpf):

            # Recupera os dados do aluno a ser excluido transformando em um DataFrame
            df_aluno = self.recupera_aluno(cpf)

            opcao_exlcuir = input(
                f"Tem certeza que deseja excluir o aluno {df_aluno.nome.values[0]}? [S OU N]: ")

            if opcao_exlcuir in "Ss":
                # Remove o aluno da tabela
                self.mongo.db["alunosEG"].delete_one({"cpf": cpf})

                # faz a validação para ver se o esporte existe na base de dados
                esporte = self.valida_esporte(int(df_aluno.id_esporte.values[0]))
                if esporte == None:
                    return None

                # Cria um novo objeto AlunoEg para informar que foi removido
                aluno_excluido = AlunoEg(
                    df_aluno.matricula.values[0], df_aluno.nome.values[0], df_aluno.cpf.values[0], esporte)

                # Exibe os dados do aluno Excluido
                print("Aluno excluido com sucesso!")
                print(aluno_excluido.to_string())

        else:
            print(f"O aluno de cpf = {cpf} não está na base de dados")

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

    def recupera_aluno(self, cpf: str = None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo aluno criado transformando em um DataFrame
        df_aluno = pd.DataFrame(list(self.mongo.db["alunosEG"].find(
            {"cpf": f"{cpf}"}, {"cpf": 1, "nome": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_aluno

    def verifica_existencia_aluno(self, cpf: str = None) -> bool:
        # Recupera os dados do aluno transformando em um DataFrame
        df_aluno = self.recupera_aluno(cpf)

        return df_aluno.empty
