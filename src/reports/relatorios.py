from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING


class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_alunos_esporte(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Realiza uma consulta no mongo e retorna o esporter resultante para a variável
        query_result = mongo.db.esporteEG.aggregate([{
            '$lookup': {'from': 'esporteEG',
                        'localField': 'id_esporte',
                        'foreignField': 'id_esporte',
                        'as': 'esporte'
                        }
        },
            {
            '$unwind': {"path": "$alunosEG"}
        },
            {'$project': {'id_esporte': 1,
                          'matricula': 1,
                          'nome': 1,
                          'cpf': 1,
                          'coordenador': 1,
                          '_id': 0
                          }}
        ])

        # Converte o esportes em lista e em DataFrame
        df_alunos_esporte = pd.DataFrame(list(query_result))

        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_alunos_esporte[["id_esporte", "matricula", "nome",
                               "cpf", "coordenador"]])
        input("Pressione Enter para Sair do Relatório de alunos por esporte")

    def get_alunos(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db['alunosEG'].find()

        df_alunos = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_alunos[["matricula", "nome", "cpf", "id_esporte"]])

    def get_esportes(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db['esporteEG'].find()

        df_esportes = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_esportes[["id_esporte", "nome", "coordenador"]])

    def get_professores(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db['professoresEG'].find()

        df_professores = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_professores[["id_professor",
              "nome", "qtde_turmas", "id_esporte"]])
