import random
import time
from Paciente import Paciente

class MedicException(Exception):
    def __init__(self,msg) -> None:
        super().__init__(f'MEDIC EXCEPTION: {msg}')

class Medico:
    
    def __init__(self,id,nome:str,especialidade:object) -> None:
        
        #assert ConsultasIntervalo >= 30 and ConsultasIntervalo<=150 , MedicException('INVALID TIME FOR A EXAM')
        self.__nome=nome
        self.__especialidade=especialidade
        self.__ConsultasIntervalo=random.randint(15,30)
        self.__id=id
    
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self,nome):
        self.__nome=nome

    @property
    def especialidade(self):
        return self.__especialidade
    
    @especialidade.setter
    #== == == Só insere se a especialidade estiver na lista de especialidades do hospital
    def especialidade(self,especialidade):
        #assert especialidade in Hospital.especialidadesLista, MedicException('SPECIALTY NOT REGISTERED IN HOSPITAL')
        self.__especialidade=especialidade
    
    @property
    def ConsultasIntervalo(self):
        return self.__tempoEstimadoConsultaMinutos
    
    @ConsultasIntervalo.setter
    def ConsultasIntervalo(self,novoIntervalo:int):
        try:
            assert novoIntervalo>=1 and type(novoIntervalo)==int
            self.__ConsultasIntervalo=novoIntervalo
        except AssertionError:
            raise MedicException('INVALID ENTERED TIME')

    
    def BuscarPaciente(self): #== == == O médico ficará esperando receber um paciente
        pass
    
    def AtenderPaciente(self,paciente:Paciente): #== == ==O médico deverá atender o paciente que contém a sua especialidade
        
        TempoConsulta= random.randint(0,20)
        print( f'O paciente:{paciente.nome}, acabou de entrar no consultório do médico: {self.__nome}, especialidade: {self.__especialidade}, a consulta levará: {TempoConsulta}')
        time.sleep(TempoConsulta) # momento do atendimento
        print( f'A consulta do paciente:{paciente.nome}, com o médico: {self.__nome}, especialidade: {self.__especialidade}, acabou!')
             
    
    def __str__(self) -> str:
        return f'|{self.__id}| {self.__nome}| {str(self.__especialidade)}|{self.__ConsultasIntervalo}'