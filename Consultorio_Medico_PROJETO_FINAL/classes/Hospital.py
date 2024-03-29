from classes.EstruturasDeDados.Lista.ListaEncadeada import Lista,ListException
from classes.EstruturasDeDados.Arvore.ArvoreBusca import ArvoreBusca, SearchArborException

from classes.Medico import Medico
from classes.Paciente import Paciente, PatientException
from classes.Especialidade import Especialidade

import random
from threading import Semaphore
from unicodedata import normalize #!! !! !! !! Precisa importar a biblioteca unide code:  $pip install unidecode



class ClinicException(Exception):
    
    def __init__(self, code:int, msg:str) -> None:
        '''
            0: Não foi possível inserir os dados em uma Lista, cheque a mensagem da Exception e tente novamente
            1: Não foi possível encontrar uma determinade chave.
            2: Não foi possível encontrar determinado médico, verifique a chave inserida
            4: Não foi  possível inserir um paciente.
            3: Foi inserida uma especialidade que não foi cadastrada na clínica.
        '''
        super().__init__(f'Clinic Exception {code}: {msg}')
        

class Consultorio:   
    __types={
        'MEDICO':1,
        'PACIENTE':2,   
        'ESPECIALIDADE':3
        }
    def __init__(self) -> None:
        self.__Especialidades=Lista() #possui uma lista com todas as especialidades
        self.__Pacientes=ArvoreBusca()#possui uma Arvore de busca com todos pacientes
        self.__Medicos= ArvoreBusca()# possui uma Arvore de busca com todos os médicos
        self.__mutexClinicaPaciente=Semaphore(1)
    
    #== == == -- Métodos Relacionados Com A Especialidade
    
    def __str__(self) -> str:

        s=''
        s+=f'{("==="*15 +"Pacientes" + "==="*15):^30}\n'
        s+=str(self.__Pacientes)
        s+='\n'

        s+=f'{("==="*15 +"Medicos" + "==="*15):^30}\n'
        s+=str(self.__Medicos)
        s+='\n'

        s+=f'{("==="*15 +"Especialidades" + "==="*15):^30}\n'
        s+=str(self.__Especialidades)
        s+='\n'
        return s
    
    def verificarEspecialidade(self,key:any)->bool: #Confere se existe uma determinada especialidade no hospital         
        return self.__Especialidades.autenticarChave(key)
    
    def inserirEspecilidade(self,nomeclatura:str)->None: # Insere uma especialidade na Lista de especialidades na clínica
        try:
            newEspeciality = Especialidade(str.upper(nomeclatura),self)
            self.__Especialidades.inserir(nomeclatura.upper(), newEspeciality) # por enquanto, a chave será o próprio nome da lista

        except ListException as LE:
            raise ClinicException(0,LE)
    
    def removerEspecialidade(self,key:any)->None:# Remove uma especialidade na Lista de especialidades na clínica        
        try:
            posicao=self.__Especialidades.busca(key)
            self.__Especialidades.remover(posicao)
        except ListException as LE:
            raise ClinicException(0,LE)
    
    def captarEspecialidade(self,key:any)->Especialidade:# Retorna uma especialidade  contida na Lista de especialidades
        try:
            posicao=self.__Especialidades.busca(key)
            return self.__Especialidades.elemento(posicao)
        except ListException as LE:
            raise ClinicException(0,LE)
        
    def exibirEspecialidades(self)->bool: #Confere se existe uma determinada especialidade no hospital             
        s=''
        s+=f'{("==="*15 +"Especialidades" + "==="*15):^30}\n'
        s+=str(self.__Especialidades)
        s+='\n'
        return s
    #== == == -- Métodos relacionados ao Médico    
    def inserirMedico(self, nome:str,especialidadeMedica:str)->None: #== == Adiciona um novo médico a Árvore de médicos
        try:
            id=self.__gerarID(nome,self.__types['MEDICO'])
   
            especialidadeCheck= self.captarEspecialidade(especialidadeMedica.upper())
                     
            NewMedic=Medico(id,nome.upper(),especialidadeCheck)
            
            self.__Medicos.InserirNode(id,NewMedic)

        except ClinicException:
                raise ClinicException(3,'SPECIALITY NOT FOUND')       
    
    def RemoverMedico(self, key:any)->None: # Remove um médico da lista
        '''
        Precisa ser ajeitado, O médico pode continuar consultando pacientes mesmo que demitido!!!!!!!!!
        '''
        try:
            self.__Medicos.removerNo(key)
            print('\033[31m'+'O médico com o id ',key,' foi demitido'+'\033[0;0m')
        except Exception:
            raise ClinicException(2,'MEDIC NOT FOUND')
            
            
    def exibirMedicos(self): #Método que mostra todos os Médicos no consultório
        return str(self.__Medicos)
    
    def ConsultarMedico(self,key): #Método que mostra todos os Médicos no consultório
        try:
            return self.__Medicos.elemento(key)
        
        except SearchArborException as SAE:
            raise ClinicException(0,SAE)
    
    #== == == -- Metodos relacionados ao paciente
    def inserirPaciente(self,cpf:str,nome:str,especialidade:str,gravidade:str):
        try:
            if not(self.verificarEspecialidade(especialidade)):#Primeiro, checa se a especialidade  que deseja inserilo existe
                raise ClinicException(3,'SPECIALITY NOT FOUND')
            #== == -- -- Entra na zona crítica
            self.__mutexClinicaPaciente.acquire()
            especialidadeListaEspera= self.captarEspecialidade(especialidade)# Depois, Busca a especialidade no qual o paciente será inserido

            NewPaciente=Paciente(cpf,nome,especialidade,gravidade) #Adiciona os pacientes na arvóre de pacientes

            self.__Pacientes.InserirNode(cpf,NewPaciente)# Por fim, adiciona ele na lista dos pacientes do hospital 
            
            especialidadeListaEspera.inserirPaciente(cpf,NewPaciente) #Adiciona o paciente na Lista da especialidade que ele deseja
            self.__mutexClinicaPaciente.release()
            #== == -- -- Sai da zona crítica
            
            return f'+Ok Sucess! {nome}'
        
        #== == -- -- Se ocorrer um erro, ele precisa liberar a área crítica
        except SearchArborException as SAE:
            self.__mutexClinicaPaciente.release()
            raise(ClinicException(0,SAE))
        
        except PatientException as PE:
            self.__mutexClinicaPaciente.release()
            raise ClinicException(4,PE)
    
    
    def removerPaciente(self,key:any)->Paciente:
        '''Não funciona se o paciente estiver sendo atendido.'''
        try:
            self.__mutexClinicaPaciente.acquire()
            pacienteRemover=self.__Pacientes.removerNo(key) # Remove o paciente do consultório e faz a coleta do objeto             
            especialidadePaciente=self.captarEspecialidade(pacienteRemover.especialidadeDesejada)#em seguida, obtem qual a especialidade ele está inserido.
            especialidadePaciente.RemoverPaciente(key) #Por fim, remove ele da fila de espera
            self.__mutexClinicaPaciente.release()
            return f'+Ok, {key} removed'

        except SearchArborException as SAE:
            self.__mutexClinicaPaciente.release()# sai da zona crítica rapidamente
            raise ClinicException(0,SAE)
    
    def removerPacienteConsultado(self,cpf:str):
        try:
            #== == -- -- Entra na zona crítica
            self.__mutexClinicaPaciente.acquire()
        
            self.__Pacientes.removerNo(cpf)
        
            self.__mutexClinicaPaciente.release()
            #== == -- -- sai da zona crítica
        
        except SearchArborException as SAE:
            self.__mutexClinicaPaciente.release()# sai da zona crítica rapidamente
            raise ListException(0,SAE)
            
         

    def exibirPacientes(self)->str: #Método que mostra todos os pacientes no consultório
        '''Retorna uma string contendo a informação de todos os paciente'''
        self.__mutexClinicaPaciente.acquire()
        pacientes=str(self.__Pacientes)
        self.__mutexClinicaPaciente.release()
        return pacientes
    
    def ConsultarPaciente(self,key) ->Paciente: #Método que mostra todos os Médicos no consultório
        '''Retorna um Paciente, através da chave'''
        try:
            
            self.__mutexClinicaPaciente.acquire()
            
            paciente= self.__Pacientes.elemento(key)
            
            self.__mutexClinicaPaciente.release()
            return paciente
    
        except SearchArborException as SAE:
            self.__mutexClinicaPaciente.release()
            raise ClinicException(0,SAE)
    #== == == -- Métodos para solucionar problemas
    
    def __gerarID(self,nome:str,type:str)-> str: # a função gera um id aleatório e confirma se n existe na estrutura de dados 5 vezes
        '''os 3 primeiros caracteres do ID é o nome do objeto, os cinco depois é aleatório e o os dois últimos caracteres do nome.
       obj.nome= "André Caio Sousa"
       obj.id= "ANDXYFYSSA" '''
        
        nome= nome.split()
        nome= ''.join(nome)
        
        for i in range(5):
            idAutentico= self.__trueGerarID(nome)

            if type == 1: #tipo MÉDICO
                if not(self.__Medicos.autenticarChave(idAutentico)):break # Caso n ache o id na estrutura de dados do médico
    
            elif type == 2: #tipo PACIENTE
                if not(self.__Pacientes.autenticarChave(idAutentico)): break # Caso n ache o id na estrutura de dados do médico
    
        return idAutentico
    
    def __trueGerarID(self,nome:str):
        tamanhoId=10
        idGerado=''
        finalValor=2
        nomeSemAcento = normalize('NFD',nome)
        nomeSemAcento = nomeSemAcento.encode('ascii','ignore')
        nomeSemAcento = nomeSemAcento.decode('utf-8')
     
        for i in range(tamanhoId): # controla o tamanho do id    
                
            if i < 3:
                idGerado+= str.upper(nomeSemAcento[i])
                    
            elif i > 7:
                idGerado+= str.upper(nomeSemAcento[-(finalValor)])
                finalValor-=1
                
            else: 
                idGerado+=str(chr(random.randrange(65, 90)))
        
        return idGerado        