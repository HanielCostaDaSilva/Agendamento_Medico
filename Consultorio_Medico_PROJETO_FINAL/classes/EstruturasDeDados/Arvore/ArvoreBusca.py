#== == == ==Criador da Exceções da Árvore binário
class SearchArborException(Exception):
        #-- -- Codes Error
        # 1, The arbor is empty
    def __init__(self, code, msg) -> None:
        super().__init__(f'Binary Arbor Exception {code}: {msg}')

#== == == ==Criador da Exceções dos Nós

class NodeException(Exception):
    #-- -- Codes Error
        # 1, key in use, use another key
        # 2, key not found, insert this key first.
    def __init__(self, code, msg) -> None:
        super().__init__(f'Node Exception {code}: ', msg)         

#== == == ==Aqui onde os nós são criados
class Node:
    def __init__(self, key:any, carga:any):
        self.__key=key
        self.carga = carga
        self.esq = None
        self.dir = None
    
    @property    
    def key(self):
        return self.__key
    
    @key.setter
    def key(self,key):
        self.__key=key
    
    def __str__(self):
        return f'| {str(self.carga)} | '
    
#== == == ==Classe que contém todos os métodos aárvore binária
class ArvoreBusca:
    #== == == Método que cria a raiz               
    def __init__(self, carga_da_raiz=None):
        self.__raiz=Node(carga_da_raiz) if carga_da_raiz  !=  None else carga_da_raiz#== == Caso não seja declarado um nó raiz, a árvore existirá, porém vazia.

    ''' Exemplo de árvore binária co busca
                    20
                11        24
             5         21     49
          3    8          23
    '''
    def __str__(self)->str:
        if self.estaVazia():
            return 'Empty'
        s= self.__stringuificarNodes(self.__raiz)
        return s
    
    @property
    def raiz(self):
        return self.__raiz
    
    #== == == Método que confere se a raiz está vazia            
    def estaVazia(self)->bool:
        if self.__raiz==None: return True
        else: return False
    
    #== == == Retorna o Nó raiz, caso ele exista            
    def getRaiz(self)->any:
        try:
            assert self.__raiz  !=  None 
            return self.__raiz
        except AssertionError:
            raise SearchArborException(1,'NO ROOT!')
    
    #== == == Retorna os elementos em préordem
     
    def preordem(self):
        try:
            assert not(self.estaVazia())
            self.__preordem(self.__raiz)
        except AssertionError:
            raise SearchArborException(1,'NO ROOT!')
    
    def __preordem(self, no:Node):
        if no==None:
            return
        print(no, end='=+=\n')
        self.__preordem(no.esq)
        self.__preordem(no.dir)
        
    #== == == Retorna os elementos em in-ordem
  
    def emordem(self):
        try:
            assert not(self.estaVazia())
            self.__emordem(self.__raiz)
        except AssertionError:
            raise SearchArborException(1,'NO ROOT!')


    def __emordem(self, no:Node):
        if no==None:
            return
        self.__emordem(no.esq)
        print(no, end='=+=\n')
        self.__emordem(no.dir)
        
    #== == == Retorna os elementos em pós-ordem 
    def posordem(self):
        try:
            assert not(self.estaVazia())
            self.__posordem(self.__raiz)
        except AssertionError:
            raise SearchArborException(1,'NO ROOT!')

    def __posordem(self, no:Node):
        if no==None:
            return
        self.__posordem(no.dir)
        self.__posordem(no.esq)
        print(no, end='=+=\n')
        

#== == == INSERIR NÒ
    '''
        A parte crucial de uma Árvore binária de busca, 
        Ela deverá inserir um nó a direita caso NewNodeKey > NodeKey 
        Ou a esquerda caso o NewNodeKey < NodeKey
        Não deverá ser permitido este caso: NewNodeKey == NodeKey      
    '''
    
    def InserirNode(self,key:any,carga:any):
        newNode=Node(key,carga)
        if self.__raiz==None:
            self.__raiz=newNode
            return
        self.__InserirNode(self.__raiz,newNode)

    def __InserirNode(self,Node:Node,newNode:Node):
        if newNode.key==Node.key: #== A key já foi usada na árvore:
            raise NodeException(1,'AUTHENTICATION KEY ERROR')
        
        elif newNode.key > Node.key: # caso a key do Nó seja maior que a key do Nó atual
            if Node.dir==None: # Não há sub-árvores a direita do nó
                Node.dir=newNode
                return # encerra a recursão
            else: #Caso haja algum(uns) nó(s) a direita, terá a tentativa de inserir o nó lá
                self.__InserirNode(Node.dir,newNode)
        
        elif newNode.key < Node.key: # caso a key do Nó a ser criado seja menor que a key do Nó atual
            if Node.esq==None: # Não há sub-árvores a esquerda do nó
                Node.esq=newNode
            else:#Caso haja algum(uns) nó(s) a esquerda, terá a tentativa de inserir o nó lá
                self.__InserirNode(Node.esq,newNode)
                return # encerra a recursão
            
    #== == == Retorna a quantiade de Nós
        
    def __len__(self):
        return self.__count(self.__raiz)
    
    def __count(self, no:Node)->int:
        if no==None:
            return 0 #== == Chegou ao fim.
        
        quantidadeNo= 1 +self.__count(no.esq) # quantidade nó é criado e é somado com a quantiade de nós a sua  do nó a esquerda
        quantidadeNo+= self.__count(no.dir) # quando não há nós a esquerda, ele tentará a sua direita.
        return quantidadeNo #finalizado, ele retornará a soma.

    #Procura a existência de um Nó
    def busca(self, key:any)->bool:
        try:
            assert not(self.estaVazia())
            return self.__busca(key,self.__raiz)
        except AssertionError:
            raise SearchArborException(1,'NO ROOT!')
    
    #== == == == procura se existe um determinado. se orientando pelo cursor
    def __busca(self, key:any, node:Node) ->bool:
        
        if node==None: # chegou ao final da sub-árvore
            return False
        
        elif node.key==key: #testa se esta é a chave 
            return True 
        
        elif key < node.key:  #testa se a chave está a esquerda do nó
            return self.__busca(key, node.esq)
        
        elif key < node.key:  #se a chave não está a esquerda, então testa se está a direita
            return self.__busca(key, node.esq)
        
    def elemento(self,key:any):
        try:
            assert not(self.estaVazia())
        
            return self.__elemento(key,self.__raiz)
        
        except AssertionError:
            raise SearchArborException(1,'NO ROOT!')
    
    def __elemento(self,key:any,node:Node):     
        if node==None: # chegou ao final da sub-árvore
            return -1
        
        elif node.key==key: #testa se esta é a chave 
            return node.carga 
        
        elif key < node.key:  #testa se a chave está a esquerda do nó
            return self.__elemento(key, node.esq)
        
        elif key < node.key:  #se a chave não está a esquerda, então testa se está a direita
            return self.__elemento(key, node.esq)
        
    #== == == Método para remover Nós em uma árvore de busca

    def removerNo(self,key:any)->Node:
        try:
            '''
            # 1º caso: O Node é um nó folha
            # 2º caso: O Node possui um Nó ou a direita ou a esquerda 
            # 3º caso: O Node possui uma sub-árvore
            # 4º caso: O Node é a raiz
            # o 4º é o que precisa de mais atenção pois a raiz não pode ser removida com um método convencional.
            '''
            assert not(self.estaVazia())
            if key == self.__raiz.key: # testa se é o 4° caso
                nodeRemoved=self.__raiz

                if nodeRemoved.esq == None and nodeRemoved.dir is None:#só há a raiz
                    self.__raiz=None
                    
                if nodeRemoved.esq != None and nodeRemoved.dir != None: #caso haja elementos tanto do lado esquerdo, quando no diretio.
                    NodeChanged=self.__the_smaller(self.raiz.dir)# o menor elemento do lado esquerdo vai ser caçado para substituir a
                    nodeRemoved.carga=NodeChanged.carga#seus conteudo serão trocados
                    nodeRemoved.key=NodeChanged.key

                    self.__raiz.dir=self.__removerNo(NodeChanged.key,self.__raiz.dir)# agora que o nó a ser removido não é mais a raiz, e sim um folha, será removido de uma vez

                #caso um dos lado estaja vazio.
                elif nodeRemoved.esq != None:
                    NodeChanged=self.__the_bigger(self.__raiz.esq)
                    
                    self.__raiz.carga=NodeChanged.carga
                    nodeRemoved.key=NodeChanged.key
                    self.__raiz.dir=self.__removerNo(NodeChanged.key,self.__raiz.dir)

                elif nodeRemoved.dir != None:
                    #nesse caso haverá um tratamento especial, como se trata do nó esquerdo, onde os menores numeros relativos
                    #a raiz ficam armazenados, teriamos que caçar o maior nó desse hemisfério.
                    NodeChanged=self.__the_smaller(self.__raiz.dir)
                    self.__raiz.carga,nodeRemoved.key=NodeChanged.carga,NodeChanged.key
                    self.__raiz.esq=self.__removerNo(NodeChanged.key,self.__raiz.esq)

            else:    
                nodeRemoved= self.__removerNo(key,self.__raiz)
            return nodeRemoved.carga
   
        except AssertionError:
            raise SearchArborException(1,'NO ROOT!')
    
    #== == método que faz toda a chama recurssiva
    def __removerNo(self,key:any,node:Node)->Node:
        if node is not None:
            #essas duas condições, naturalmente, fará a verificação se o node está na árvore.
            if key < node.key:
                node.esq=self.__removerNo(key,node.esq)
            
            elif key > node.key:
                node.dir=self.__removerNo(key,node.dir)
            #neste cenário, o nó em questão foi achado, e entrará no processo de remoção sem afetar os demais nós
            else:
                if node.esq is None:
                    aux=node.dir
                    node=None
                    return aux
                
                elif node.dir is None:
                    aux=node.esq
                    node=None
                    return aux
                #aqui o seu substituto será copiado para o lugar do nó removido
                aux=self.__the_smaller(node.dir)
                
                node.carga=aux.carga
                #aqui a versão original será removida
                node.dir=self.__removerNo(aux.key,node.dir)
                return node
            return node
        else:
            return None
        
    def smaller(self):
        return self.__the_smaller(self.__raiz)
   
    def __the_smaller(self,node:Node)->Node:
        if node is None:
            return
        aux = node
        while aux.esq is not None:#se houver um nó a esquerda do nó atual, significa que há um nó menor
            aux=aux.esq
        return aux
    
    def bigger(self):
        return self.__the_bigger(self.__raiz)

    def __the_bigger(self,node:Node)->Node:
        if node is None:
            return node
        aux = node
        while aux.dir is not None:#se houver um nó a direita do nó atual, significa que há um nó maior
            aux=aux.dir
        return aux
    
    def __changeNode(self, node:Node): #Checado, tá tranquilo  eu acho...
        lowerNode=node #O node é atribuido como o menor node daquela sub-árvore
        '''Caso o node possua uma sub-árvore, ele deverá trocado pelo menor nó a sua direita, ou seja, o node mais a esquerda da sua direita'''
        
        if node.esq==None: #caso ele seja o node que possua a menor chave daquela sub-árvore
            node=None # Ele irá se tornar vazio, pois irá ser movido para a posição do nó que será removido.
            return lowerNode
        
        elif node.esq.esq==None: # caso ele não seja o menor, mas o seu próximo seja.
            lowerNode=node.esq # o Menor nó será considerado a sua esquerda
            
            if lowerNode.dir != None: # Checa se há algo a direita do menor nó
                node.esq= lowerNode.dir #o Nó que aponta para o menor nó, passará a apontar para a direita desse.
        
            return lowerNode
        
        return self.__changeNode(node.esq) #se houver algum nó a esquerda deste, ele irá fazer o teste naquele.
            
        
    #== == == Método que remove todos os nós de maneira que não deixe vestígios na memória 
    def esvazia(self):
        try:
            assert not(self.estaVazia())
            self.__raiz=self.__libera(self.__raiz)
            
        except AssertionError:
            raise SearchArborException(1,'NO ROOT!')
        
    def libera(self,proximoNo)->None:
        
        if ( not self.estaVazia() and proximoNo  !=  None):
            
            proximoNo.esq= self.libera(proximoNo.esq)
    
            proximoNo.dir= proximoNo=self.libera(proximoNo.dir)
        return None
    
    
    def __stringuificarNodes(self, node:Node):
        cargaString=''
        
        if node==None:
            return cargaString #retorna uma string vazia
        
        cargaString+=self.__stringuificarNodes(node.esq)
        cargaString+= f' {node}\n{ "===" * 30 }\n'
        
        cargaString+=self.__stringuificarNodes(node.dir)
        
        return cargaString
    
    def autenticarChave(self,key)->bool: #Este método percorerá toda a lista a fim de conferir se já existe a chave
        try:
            if self.busca(key):
                return True
        except SearchArborException:
            return False
    