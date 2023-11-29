from utils import config


class SplashScreen:
    def __init__(self):
        # Nome(s) do(s) criador(es)
        self.created_by = "Daniel Vitor, Flavio Moreira, Gabriel Louzada, Gabriel Vianna"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_documents_count(self, collection_name):
        # Retorna o total de registros computado pela query
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA ESCOLAR                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - ALUNOS:         {str(self.get_documents_count(collection_name="alunosEG")).rjust(5)}
        #      2 - ESPORTES:         {str(self.get_documents_count(collection_name="esporteEG")).rjust(5)}
        #      3 - PROFESSORES:     {str(self.get_documents_count(collection_name="professoresEG")).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """
