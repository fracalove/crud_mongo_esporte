class EsporteEG:
    def __init__(self,
                 id_esporte:int=None,
                 nome:str=None,
                 coordenador:str=None
                 ):
        
        self.set_id_esporte(id_esporte)
        self.set_nome(nome)
        self.set_coordenador(coordenador)
        

    def set_id_esporte(self, id_esporte:int):
        self.id_esporte = id_esporte

    def set_nome(self, nome:str):
        self.nome = nome

    def set_coordenador(self, coordenador:str):
        self.coordenador = coordenador

    def get_id_esporte(self) -> int:
        return self.id_esporte

    def get_nome(self) -> str:
        return self.nome

    def get_coordenador(self) -> str:
        return self.coordenador

    def to_string(self) -> str:
        return f"id esporte: {self.get_id_esporte()} | Nome: {self.get_nome()} | Coordenador: {self.get_coordenador()}"