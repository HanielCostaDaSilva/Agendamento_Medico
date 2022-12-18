import random
import time
#from Consultorio import Consultorio
#from Especialidade import Especialidade
from threading import Thread
from Paciente import Paciente
#from Consultorio import Consultorio

class MedicException(Exception):
    def __init__(self,code,msg) -> None:
        '''1: Entrada de dados inválida'''
        super().__init__(f'MEDIC EXCEPTION {code}: {msg}')

class Medico:
    
    def __init__(self,matricula,nome:str,especialidade, consultorio) -> None:
        
        self.__matricula=matricula
        self.__nome=nome.upper()
        self.__especialidade=especialidade
        self.__consultorio=consultorio
        self.__ConsultasIntervalo=random.randint(15,30)
        self.consultar=Thread(target=self.BuscarPaciente)
        self.consultar.start()

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
    #== == == Só insere se a especialidade estiver na lista de especialidades no consultório
    def especialidade(self,especialidade):
        #assert especialidade in Hospital.especialidadesLista, MedicException('SPECIALTY NOT REGISTERED IN HOSPITAL')
        self.__especialidade=especialidade
    
    @property
    def ConsultasIntervalo(self):
        return self.__ConsultasIntervalo
    
    @ConsultasIntervalo.setter
    def ConsultasIntervalo(self,novoIntervalo:int):
        try:
            assert novoIntervalo>=1 and type(novoIntervalo)==int
            self.__ConsultasIntervalo=novoIntervalo
        except AssertionError:
            raise MedicException(1,'INVALID ENTERED TIME')

    
    #== == == -- Metodos do Médico
    
    def BuscarPaciente(self): #== == == O médico ficará esperando receber um paciente
        paciente=self.__especialidade.RemoverPrimeiroPaciente()
        self.AtenderPaciente(paciente)
        self.__consultorio.removerPaciente(paciente.cpf)
        time.sleep(2)
    
    def AtenderPaciente(self,paciente:Paciente): #== == ==O médico deverá atender o paciente que contém a sua especialidade
        TempoConsulta= random.randint(0,20)

        print( f'O paciente:{paciente.nome}, acabou de entrar no consultório do médico: {self.__nome}, especialidade: {self.__especialidade}, a consulta levará: {TempoConsulta}')
        time.sleep(TempoConsulta) # momento do atendimento

        print( f'A consulta do paciente:{paciente.nome}, com o médico: {self.__nome}, especialidade: {self.__especialidade}, acabou!')
        

    def __str__(self) -> str:
        return f' | matrícula: {self.__matricula}|  nome:{self.__nome}| especialide: {str(self.__especialidade.nomeclatura)}| consultas sequenciais: {self.__ConsultasIntervalo}'