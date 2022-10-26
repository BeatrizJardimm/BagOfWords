# Paula Beatriz Louback Jardim

# ------------------------------------------------------
### Enunciado ###

# Sua tarefa será gerar a matriz termo documento, dos documentos recuperados da internet e imprimir esta matriz na tela. Para tanto:
# a) Considere que todas as listas de sentenças devem ser transformadas em listas de vetores, onde cada item será uma das palavras da sentença.
# b) Todos os vetores devem ser unidos em um corpus único formando uma lista de vetores, onde cada item será um lexema.
# c) Este único corpus será usado para gerar o vocabulário.
# d) O resultado esperado será uma matriz termo documento criada a partir da aplicação da técnica bag of Words em todo o corpus.

# ------------------------------------------------------
# Realizando os imports:
#!python -m spacy download en_core_web_sm

from bs4 import BeautifulSoup
from requests import get
from spacy import load
import string

# ------------------------------------------------------
# Guardando as referências para todos os artigos em uma lista:

artigos = ["https://aliz.ai/en/blog/natural-language-processing-a-short-introduction-to-get-you-started/",
           "https://medium.com/nlplanet/two-minutes-nlp-python-regular-expressions-cheatsheet-d880e95bb468",
           "https://hbr.org/2022/04/the-power-of-natural-language-processing",
           "https://www.activestate.com/blog/how-to-do-text-summarization-with-python/",
           "https://towardsdatascience.com/multilingual-nlp-get-started-with-the-paws-x-dataset-in-5-minutes-or-less-45a70921d709"]

# ------------------------------------------------------
# Esse código percorre todos os documentos, criando uma lista com as sentenças de cada documento
# e ao final, une todas essas listas em uma matriz.
# Ao mesmo tempo, o código abaixo realiza a mesma atividade descrita acima para o vocabulário de cada documento,
# criando uma lista de palavras para cada um e juntando essas listas no final. 

matriz_palavras = [[], [], [], [], []]
matriz_sentencas = []

i = 0
for site in artigos:
  sents_list = []
  document_words = set()

  r = get(site)
  r = r.content

  soup = BeautifulSoup(r, 'html.parser')
  text = soup.find_all('p')
  nlp = load("en_core_web_sm")

  for paragraph in text:
    content = paragraph.get_text()
    sentences = nlp(content).sents

    for sent in sentences:
      sent = sent.text.strip(string.punctuation)
      sent = sent.strip(string.digits)
      sent = sent.strip('\n')
      sents_list.append(sent)
      words = sent.split(" ")
      
      for word in words:
        word = word.strip(string.punctuation)
        word = word.strip(string.digits)
        word = word.strip('\n')
        document_words.add(word)

  matriz_sentencas.append(sents_list)
  for w in document_words:
    matriz_palavras[i].append(w)

  i += 1

# ------------------------------------------------------
# O trecho abaixo cria um Bag of words unindo todas as palavras de todos os documentos.
# Neste trabalho estou considerando uppercases e lowcases como caracteres diferentes.

corpus = set()

for lists in matriz_palavras:
  for word in lists:
    corpus.add(word)

# ------------------------------------------------------
# Logo abaixo está a criação da header da matriz-termo.

header = []

for each in corpus:
  if each != "":
    header.append(each)

header = sorted(header)

# ------------------------------------------------------
# Agora, vamos criar a matriz-termo.
# Essa matriz está sendo criada em um dicionário, onde cada sentença é uma key e o valor de cada key é uma lista
# na qual os elementos correspondem a quantidade de vezes que cada termo da header aparece nessa sentença.

dict_matriz= {}
dict_matriz["Sentenças"] = header[1:]

for doc in matriz_sentencas:
  for sent in doc:
    values_list = []
    termos = sent.split(" ")
    for palavra in dict_matriz["Sentenças"]:
      contador = 0
      for cada_plv in termos:
        if cada_plv == palavra:
          contador += 1
      values_list.append(contador)
    dict_matriz[sent] = values_list

# ------------------------------------------------------
# Para demonstrar o funcionamento do código, escolhi uma sentença de exemplo
# que contém a primeira palavra da lista de palavras além de conter uma palavra que se repete.

key = "A parent word and its children will represent a phrase, a meaningful, independent structure within the sentence"

print(dict_matriz["Sentenças"])
print(dict_matriz[key])

qnt = 0
for count in dict_matriz[key]:
  if count >= 2:
    qnt += 1
print("Quantidade de palavras que se repetem na sentença: ", qnt)

# ------------------------------------------------------
# Como o Colab limita o output por conta do tamanho do dicionario, abaixo estou printando apenas as 50 primeiras linhas da matriz.

loop = 0
for sent in dict_matriz:
  if loop <= 50:
    print(dict_matriz[sent])
  loop += 1