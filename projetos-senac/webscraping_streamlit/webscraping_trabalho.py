# importando as funções e as bibliotecas
from bs4 import BeautifulSoup
from requests import get
import streamlit as st
import pandas as pd




# atribuindo o site a uma variavel
url_estante_virtual = 'https://www.estantevirtual.com.br/lst/mais-vendidos'


# me passando por navegador
navegador = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}


# fazendo as requisições
dados = get(url=url_estante_virtual, headers=navegador, verify=False)


# pegando as respostas das requisições
dados_texto =  BeautifulSoup(dados.text, 'html.parser')


# lista oficial dos livros
biblioteca = []


# pegando todos os dados de cada livro
livros_dados = dados_texto.find_all(class_='product-item')



todos_livros = list(livros_dados)
# loop para separar as informações de cada livro
for informacao in todos_livros:


  # dicionario padrao
  livro = {


      'título': '',
      'autor': '',
      'novos': '0 novos',
      'usados': '             0 usados',


  }




  # pegando cada informação do livro separadamente
  titulo = informacao.find('h2', class_='product-item__title')
  autor = informacao.find('p', class_='product-item__author')
  categorias = informacao.find_all('p', class_='product-item__variations__item')






  # loop para separar as quantidades em novos e usados
  for categoria in categorias:


    # transformando as quantidades/categorias em texto
    categoria_texto = categoria.text


    # modificando a quantidade de usados
    if 'usados' in categoria_texto:
      livro['usados'] = categoria_texto


    # modificando a quantidade de novos
    else:
      livro['novos'] =  categoria_texto






  # modificando os outros dados do dicionario
  livro['título'] = titulo.text
  livro['autor'] = autor.text.title()






  # fazendo um copia do livro e adicionando ela na lista de livros
  biblioteca.append(livro.copy())
  livro.clear()




# transformando o dicionario em um dataframe
biblioteca_df = pd.DataFrame(
  data = biblioteca
)


# titulo da página
st.title('LIVROS POPULARES')
st.write('*Tabela dos livros mais populares do **Estante Virtual***')


# mostrando o dicionario tabulado
st.dataframe(
  data = biblioteca_df)

