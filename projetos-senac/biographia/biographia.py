# importando as bibliotecas
from deep_translator import GoogleTranslator
from requests import get
import streamlit as st

# função para limpar a datas
def limpar_data(data_misturada):
    '''
    Remove o nome da figura histórica da data de nascimento.
    data_misturada = string contendo o nome e a data de nascimento da peessoa
    return: retorna uma string apenas com a data de nascimento da pessoa
    '''
    
    # separando a data em uma lista
    data_formatada = data_misturada.split()

    # inicializando as variaveis
    ano_indice = None
    dia_indice = None

    # loop para remover o nome da data
    for indice, palavra in enumerate(data_formatada):

        palavra.strip()
        
        # encontrou o dia
        if palavra.isnumeric() and len(palavra) <= 2:


            dia_indice = indice

        # encontrou o ano
        if palavra.isnumeric() and len(palavra) == 4:


            ano_indice = indice

    # existe um ano com 4 algarismo
    if ano_indice is not None and dia_indice is not None:


        # transformando a data final em uma string
        data_final = ' '.join(data_formatada[dia_indice:ano_indice+1])


    # não existe um ano com 4 algarismo
    else:


        # transformando a data final em uma string
        data_final = ' '.join(data_formatada[dia_indice:])


    return data_final


# função para traduzir texto
def traduzir_para_portugues(texto):
    '''
    Traduz um texto do inglês para o português.
    texto: texto em inglês
    return: o texto em português
    '''

    # traduzindo o texto pra português
    texto_traduzido = GoogleTranslator(source='en', target='pt'). translate(texto)
    return texto_traduzido

# função para ver figura historica
def consultar_figura_historica(nome, traduzir_dados=True):
    '''
    Pega os dados de uma figura histórica na api.
    nome: nome da figura histórica
    traduzir_dados: parâmetro que permite, ou não, a tradução dos dados
    return: retorna um dicionário com os dads [titulo, data de nasciemnto, data da morte e causa da morte] da figura histórica
    '''

    # buscando a pessoa na API
    url_padrao = get(

        url=f'https://api.api-ninjas.com/v1/historicalfigures?name={nome}',
        headers={'X-Api-Key': st.secrets["API-KEY"]}
    )
   
    # conseguiu achar a pessoa
    if url_padrao and url_padrao.json():


        # procurando a pessoa na API
        try:
                # pegando os dados da pessoa
                dados = url_padrao.json()


                # pegando o nome da propria API
                nome = dados[0]['name']


                # pegando o titulo da pessoa
                titulo = dados[0]['title']


                # pegando o nascimento da pessoa
                nasciemnto = dados[0]['info']['born']
                nasciemnto = limpar_data(nasciemnto)


                # pegando a morte da pessoa
                morte = dados[0]['info']['died']
                morte = limpar_data(morte)

        # API não conseguiu achar a pessoa
        except KeyError:
             
            return f'Não consegui achar todos os dados do(a) {nome}...'
       
        else:
             
                # tentando pegar causa da morte
                try:
                        # causa da morte
                        causa_morte = dados[0]['info']['cause_of_death']

                # não tem causa da morte
                except KeyError:
               
                        causa_morte = 'Unknown'

                # usuario quer os daados em português
                if traduzir_dados:


                        titulo = traduzir_para_portugues(titulo)
                        nasciemnto = traduzir_para_portugues(nasciemnto)
                        morte = traduzir_para_portugues(morte)
                        causa_morte = traduzir_para_portugues(causa_morte)


                # dicionario com os dados da pessoa
                dados_completos = {
                       
                'nome': nome,
                'titulo': titulo.title(),
                'nascimento': nasciemnto,
                'morte': morte,
                'causa_da_morte': causa_morte


                }
        return dados_completos

# função para ver celebridade
def consultar_celebridade(nome, traduzir_dados=True):
    '''
    Pega os dados de uma celebridade na api.
    nome: nome da celebridade
    traduzir_dados: parâmetro que permite, ou não, a tradução dos dados
    return: retorna um dicionário com os dads [nome, ocupação, idade, gênero, nacionalidade e se tá vivo ou não] da celebridade
    '''

    # pedindo os dados pra API
    url = get(
        url= f'https://api.api-ninjas.com/v1/celebrity?name={nome}',
        headers= {'X-Api-Key': st.secrets["API-KEY"]}
    )

    # conseguiu acessar a API
    if url.status_code == 200 and url.json():


        # pegando todos os dados da celebridade
        informacoes = url.json()


        # separaando os dados da celebridade
        try:
            
            # nome
            nome = informacoes[0]['name']

            # genêro
            genero = informacoes[0]['gender']

            # modificando o genero
            if genero == 'female':
                genero = 'Feminine'
                
            else:
                genero = 'Masculine'


            # nacionalidade
            nacionalidade = informacoes[0]['nationality']

            # ocupação
            ocupacao = informacoes[0]['occupation']

            # idade
            idade= informacoes[0]['age']

            # situação
            situacao = informacoes[0]['is_alive']

            # verificando se a pessoa ta viva ou morta
            # ta viva
            if  situacao:
                situacao = 'Alive'


            # ta morta
            else:
                situacao = 'Dead'

            # verfificando se tem '_'
            for profissao in ocupacao:
               
                # a profissão tem '_'
                if '_' in profissao:
                   
                    # pegando a posiçaõ da profissao na lista
                    indice = ocupacao.index(profissao)
                   
                    # trocando o removendo o '_' da profisão
                    ocupacao[indice]= profissao.replace('_', ' ')
               
                # transformando a lista em uma str
                ocupacao_final = ',  '.join(ocupacao)

        except KeyError:
            st.warning('Eu não consegui acessar as informações dessa pessoa... 😞')

        else:

            # usuário que traduzir os dados
            if traduzir_dados:


                genero = traduzir_para_portugues(genero)
                situacao = traduzir_para_portugues(situacao)
                ocupacao_final = traduzir_para_portugues(ocupacao_final)

            pessoa = {
                'nome': nome,
                'idade': idade,
                'genero': genero,
                'nacionalidade': nacionalidade.upper(),
                'ocupacao': ocupacao_final.title(),
                'situacao': situacao
            }
            return pessoa

# cabeçalho do site
st.markdown(
    '''
    #  BIOGRA*PHIA*


    A '*BiograPHIA*' é uma plataforma onde você pode buscar informações sobre diversas pessoas de todo o mundo! Seja essa pessoa um ***imperador da roma antiga*** ou uma ***celebridade dos dias atuais***.
    '''
)


# lista de assunto
assuntos = ['Figuras Históricas 🏛️', 'Celebridades ⭐']
pagina1, pagina2, = st.tabs(
    tabs=assuntos,
)


# usuario deseja ver as figuras historicaas
with pagina1:

    # idioma dos dados
    idioma_figura_historica = st.radio(
       
       label='Em que idioma deseja ver os dados da figura?',
       options=['Português', 'Inglês'],
       index=None,
       key='idioma_figura_historica'
    )  

    # usuario já informou o idioma
    if idioma_figura_historica:


        # verificando se o usuário quer traduzir os dados
        # usuário quer traduzir os dados
        if idioma_figura_historica == 'Português':
               
            resposta = True

        # usuaário não quer traduzir os dados
        else:
               
            resposta = False

        # pegando o nome da figura
        nome_figura_historica = st.text_input(
            
            label='Informe o nome da figura histórica',
            key='nome_figura_historica'
        ).title()


        #  usuário já informou o nome
        if nome_figura_historica:
                       
            # pegando os dados da figura escolhida
            pessoa = consultar_figura_historica(
                
                nome=nome_figura_historica, 
                traduzir_dados=resposta
            )

            # consegui conhece a pessoa
            if pessoa:

                    # separando os dados da pessoa
                    try:
                        nome_titulo = pessoa['nome'].upper()
                        titulo_pessoa = pessoa['titulo']
                        dia_nascimento_pessoa = pessoa['nascimento']
                        dia_morte_pessoa = pessoa['morte']
                        causa_da_morte_pessoa = pessoa['causa_da_morte']

                        st.title(f'{nome_titulo}')
                        
                        st.markdown(
                            f'''
                                🌟 Título: {titulo_pessoa}

                                👶 Nascimento: {dia_nascimento_pessoa}

                                💀 Morte: {dia_morte_pessoa}

                                🔪 Causa da morte: {causa_da_morte_pessoa}
                            '''
                        )
                    # não consegui pegar os dados da pessoa
                    except TypeError:
                        st.warning('Eu ***não consegui achar as informações*** sobre essa pessoa 😞')

            # API não conhece a pessoa
            elif pessoa == None:
                st.warning('Parece que ***não conheço essa pessoa***... 😞')

# usuario quer ver eventos históricos
with pagina2:
     
    # idioma dos dados
    idioma_celebridade = st.radio(
        
       label='Em que idioma deseja ver os dados da celebirdade?',
       options=['Português', 'Inglês'],
       index=None,
       key='idioma_celebridade'
    )

    # verificando se o usuário quer traduzir os dados
    # usuário quer traduzir os dados
    if idioma_celebridade == 'Português':       
        resposta = True

    # usuaário não quer traduzir os dados
    else:      
        resposta = False

    # usuario já informou o idioma
    if idioma_celebridade:
         
        # pergunatando qual evento o usuário quer
        nome_celebridade = st.text_input(
             
            label='Informe o nome da celebridade',
            key='nome_celebridade'
        )

        # usuário informou o nome do evento
        if nome_celebridade:
                  
            # pegando os dados da celebridade
            celebridade = consultar_celebridade(
                
                nome=nome_celebridade, 
                traduzir_dados=resposta
            )
            
            # seprando os dados da celebridade
            try:
                
                ocupacao = celebridade['ocupacao']
                idade_celebridade = celebridade['idade']
                nacionalidade_celebridade = celebridade['nacionalidade']
                situacao_celebridade = celebridade['situacao']
                genero_celebridade = celebridade['genero']

            except TypeError:
                 
                st.warning('Parece que eu ***não tenho informações sobre essa pessoa***... 😞')
                
            else:
                 
                st.title(celebridade['nome'].upper())

                st.markdown(
                    f'''
                        📊 Ocupação: {ocupacao}

                        ❔ Gênero: {genero_celebridade}

                        🎂 Idade, em anos: {idade_celebridade}

                        🗺️ Nacionalidade: {nacionalidade_celebridade.upper()}

                        🧟 Status: {situacao_celebridade}
                    '''
                )
