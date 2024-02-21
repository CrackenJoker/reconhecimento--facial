
# Reconhecimento Facial

Ao contrário de métodos tradicionais, como cartões de acesso ou senhas, o reconhecimento facial utiliza características únicas do rosto de uma pessoa para verificar sua identidade. Isso reduz a possibilidade de falsificação ou uso indevido de cartões de acesso.
Assim promovendo a segurança e divertidamente aprendendo mais sobre visão computacional criei este repositóro

## Referência

 - [Opencv:Orb](https://docs.opencv.org/3.4/d1/d89/tutorial_py_orb.html)


## Apêndice

Coloque qualquer informação adicional aqui


## Autores

- [@CrackenJoker](https://www.github.com/CrackenJoker)


## Documentação

[Documentação](https://docs.opencv.org/3.4/d1/d89/tutorial_py_orb.html)

Como entusiasta do OpenCV, o mais importante sobre o ORB é que ele veio do "OpenCV Labs". Este algoritmo foi criado por Ethan Rublee, Vincent Rabaud, Kurt Konolige e Gary R. Bradski em seu artigo ORB: Uma alternativa eficiente para SIFT ou SURF em 2011. Como o título diz, é uma boa alternativa para SIFT e SURF em computação custo, desempenho compatível e principalmente as patentes. Sim, SIFT e SURF são patenteados e você deve pagá-los pelo seu uso. Mas ORB não é!!!

ORB é basicamente uma fusão do detector de ponto-chave FAST e do descritor BRIEF com muitas modificações para melhorar o desempenho. Primeiro, use FAST para encontrar os pontos-chave e, em seguida, aplique a medida de canto de Harris para encontrar os N pontos principais entre eles. Ele também usa pirâmide para produzir recursos multiescala. Mas um problema é que o FAST não calcula a orientação. Então, e quanto à invariância de rotação? Os autores apresentaram a seguinte modificação.

Ele calcula o centróide ponderado pela intensidade do patch com o canto localizado no centro. A direção do vetor deste ponto de canto até o centróide fornece a orientação. Para melhorar a invariância da rotação, os momentos são calculados com xey que devem estar em uma região circular de raio , onde é o tamanho do patch.RR
Agora, para descritores, ORB usa descritores BRIEF. Mas já vimos que o BRIEF tem um desempenho ruim com rotação. Então o que o ORB faz é “dirigir” o BRIEF de acordo com a orientação dos pontos-chave. Para qualquer conjunto de recursos de testes binários no local , defina uma , que contém as coordenadas desses pixels. Então, usando a orientação do patch, , sua matriz de rotação é encontrada e gira o para obter a versão dirigida (girada) .n(xeu,simeu)2 × nSθSSθ
ORB discretiza o ângulo em incrementos de (12 graus) e constrói uma tabela de consulta de padrões BRIEF pré-computados. Contanto que a orientação do ponto-chave seja consistente entre as visualizações, o conjunto correto de pontos será usado para calcular seu descritor.2π _/ 30θSθ
BRIEF tem uma propriedade importante de que cada recurso de bit tem uma grande variância e uma média próxima de 0,5. Mas uma vez orientado ao longo da direção do ponto-chave, ele perde essa propriedade e se torna mais distribuído. A alta variância torna um recurso mais discriminativo, pois responde diferentemente às entradas. Outra propriedade desejável é ter os testes não correlacionados, pois assim cada teste contribuirá para o resultado. Para resolver tudo isso, o ORB executa uma busca gananciosa entre todos os testes binários possíveis para encontrar aqueles que possuem alta variância e médias próximas de 0,5, além de não serem correlacionados. O resultado é chamado rBRIEF .

Para correspondência de descritores, é usado o LSH multi-sonda, que melhora o LSH tradicional. O artigo diz que ORB é muito mais rápido que SURF e SIFT e o descritor ORB funciona melhor que SURF. ORB é uma boa escolha em dispositivos de baixo consumo para costura de panoramas, etc.

ORB em OpenCV
Como de costume, temos que criar um objeto ORB com a função cv.ORB() ou usando a interface comum feature2d. Possui vários parâmetros opcionais. Os mais úteis são nFeatures que denota o número máximo de recursos a serem retidos (por padrão 500), scoreType que indica se a pontuação de Harris ou pontuação FAST para classificar os recursos (por padrão, pontuação de Harris) etc. Outro parâmetro, WTA_K decide o número de pontos que produzem cada elemento do descritor BRIEF orientado. Por padrão são dois, ou seja, seleciona dois pontos por vez. Nesse caso, para correspondência, é usada a distância NORM_HAMMING. Se WTA_K for 3 ou 4, o que leva 3 ou 4 pontos para produzir o descritor BRIEF, então a distância correspondente é definida por NORM_HAMMING2.

Abaixo está um código simples que mostra o uso do ORB.
