from model.esporteEG import EsporteEG

class ProfessoresEG:
    def __init__(self,
                 id_professor:int=None,
                 nome: str=None,
                 qtd_turmas: int=None,
                 esporte: EsporteEG=None
                 ):

        self.set_id_professor(id_professor)
        self.set_nome(nome)
        self.set_qtd_turmas(qtd_turmas)
        self.set_esporte(esporte)

    def set_id_professor(self, id_professor:int):
        self.id_professor = id_professor
    
    def set_nome(self, nome:str):
        self.nome = nome

    def set_qtd_turmas(self, qtd_turmas:int):
        self.qtd_turmas = qtd_turmas
    
    def set_esporte(self, esporte:EsporteEG):
        self.esporte = esporte

    def get_id_professor(self) -> int:
        return self.id_professor

    def get_nome(self) -> str:
        return self.nome

    def get_qtd_turmas(self) -> int:
        return self.qtd_turmas

    def get_esporte(self) -> EsporteEG:
        return self.esporte

    def to_string(self) -> str:
        return f"id professor: {self.get_id_professor()} | Nome: {self.get_nome()} | qtde turmas: {self.get_qtd_turmas()} | Esporte: {self.get_esporte().to_string()}"