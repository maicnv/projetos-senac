import streamlit as st
from time import sleep
import requests


# titulo do site
st.title('QUAL ANIME É ESSE? 🤔')
st.write('*Você  já viu uma imagem de algum anime jogada pela internet, quis muito saber o nome dele mas não encontrou de jeito nenhum? Se sim, esse site vai te ajudar muito! Para usar nossa ferramenta, basta copiar a URL da cena que você achou no campo abaixo e ser feliz!*')



# cena do anime que o usuário deseja encontrar
imagem = st.text_input(label='Informe a URL da cena: ')


# usuário ainda não informou a URL
if imagem == '':

    # mostrando algumas dicas para o usuário
    st.title('DICAS')
    
    st.write('📄 Use cenas no formato ***.jpg*** ou ***.img***;')
    
    st.write('✨ Use cenas com uma ***boa qualidade***;')

    st.write('🎞️ Sempre ***confira o anime pela cena***, não apenas pelo nome.')


# usuário informou uma URL
else:

    # procurando a cena na API
    url = requests.get(f'https://api.trace.moe/search?url={imagem}')
    
    
    # informações da cena
    informacoes = url.json()    
    
    
    # adicionando todas as informações (de todos os possíveis animes) da cena em uma váriavel
    # tentando encontrar o anime na API
    try:
        resultados_gerais = informacoes['result']
    
    
    # a API não possui o anime  
    except KeyError:
        
        # mensagens de erro
        st.write('Me desculpa mas eu ***não conheço*** este anime... 😔')
        
        st.write('🔗 Talvez seja ***algum problema com a cena***, troque a URL e siga as dicas.')
        
        
    # a API possui o anime   
    else:
        
        
        # dicionario padrao
        anime = {
            'nome': '',
            'episodio': '',
            'cena em video': '',
            'similaridade': ''
        }
        
        
        similaridade_atual = 0
        
        
        # loop para analisar todos os possíveis animes
        for indice, dado in enumerate(resultados_gerais):
    
            if indice == 0:
        
                # passando os dados do anime mais semelhante
                anime['nome'] = dado['filename']
                anime['episodio'] = dado['episode']
                anime['cena em video'] = dado['video']
                anime['similaridade'] = dado['similarity']
                
                
        # inicializando algumas variaveis
        nome_atual = ''
        indice_traco = ''
        
        
        # o nome possui '[]'
        if '[' in anime['nome'] and ']' in anime['nome']:
            
            
            # inicializando alguumas variaveis
            quant_colchetes_fechados = 0
            lista_nomes = []


            # contando o tanto de ']' que o nome tem
            for caracter in anime['nome']:
                
                
                if caracter == ']':
                    
                    # contabilizando os ']'
                    quant_colchetes_fechados += 1
                    
                    
            # o nome tem 2 ou mais ']'
            if quant_colchetes_fechados >= 2:
                
                
                # separando o nome onde tem '['
                nome_separado = anime['nome'].split('[')
                
                
                # removendo o ']' que sobrou nos nomes
                for nome in nome_separado:
                    
                    
                    nome_sem_colchetes = nome.split(']')[0]
                    
                    # adicionando o nome sem nenhum dos colchetes, na lista
                    lista_nomes.append(nome_sem_colchetes)
                    
                    
                nome_atual = lista_nomes[2]


                # o nome tem '_'
                if '_' in nome_atual:
                    
                    
                    nome_atual = nome_atual.replace('_', ' ')


            elif quant_colchetes_fechados == 1:
                
                # separando a string em uma lista
                nome_separado = anime['nome'].replace(']', '').split()
                
                
                # verificando se tem '-' no nome
                if '-' in nome_separado:
                    
                    
                    # pegando a posição do '-'
                    indice_traco = nome_separado.index('-')
                    
                    # tirando os dados não necessários do nome
                    nome_atual = nome_separado[1:indice_traco]
                    
                    # juntando o nome
                    nome_atual = ' '.join(nome_atual)
                    
                    
            # trocando o nome do anime no dicionário
            anime['nome'] = nome_atual.strip().title()


        # o nome do anime não tem '[]'
        else:
            
            nome_separado = anime['nome']
            
            
            # loop para achar a posicao do '-'
            for caracter in nome_separado:
                
                if caracter == '-':
                    
                    
                    # pegando a posição do '-'
                    indice_traco = nome_separado.index('-')
                    
                    
            # tirando os dados não necessários do nome
            nome_atual = nome_separado[:indice_traco]


            # trocando o nome do anime no dicionário
            anime['nome'] = nome_atual.strip().title()


        # mostrando algumas informações sobre o anime
        st.title('SEU ANIME É... 📺')
        st.write(f' 🖋️ Nome: {anime['nome']}')
        st.write(f' 🎬 Episódio: {anime['episodio']}')


        # mostrando um pedaço da cena no site
        st.title('ESSA É A CENA?')
        st.video(anime['cena em video'])


        # verificando se é a cena correta
        # pegando a resposta do usuário
        resposta = st.radio(
            
            label= 'A cena está de acordo com o vídeo?',
            options=['Sim', 'Não'],
            index=None
        )


        
        sleep(1)
        if resposta:

            # o anime mostrado é o correto
            if resposta == 'Sim':
                
                st.write(f'Boa! Agora é assistir ***{anime['nome']}*** 😁')
    
    
            # o anime mostardo é o incorreto
            else:
    
                st.write(f'Poxa, acabei comentendo um erro... 😔')
    
                st.write('🔗 Por favor, ***confira a URL passada***, eu me dou melhor com cenas no formato ***.img*** e .***jpg***;')
    
                st.write('📷 Imagens com ***baixa qualidade*** são mais difíceis pra mim analisar;')
    
                st.write('🔒 ***Alguns sites me bloqueiam***, tente trocar a URL.')
