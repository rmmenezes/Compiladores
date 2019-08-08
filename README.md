# Compilador TPP
  O seguinte trabalho faz parte da disciplina de Compiladores do curso de ciência da computação, e resulta no estudo e implementação de compilador para a linguagem T++.

## Introdução
  Um compilador de forma simplificada nada mais é do que um tradutor de um código fonte em uma linguagem de programação de alto nível para uma linguagem de programação de baixo nível. As linguagens de alto nível são muito utilizadas no desenvolvimento de aplicações, porém a maioria dos computadores processam instruções mais simples e elementares e o compilador tem exatamente este papel de transformar o código para algo mais próximo da linguagem da máquina.

  O processo de compilação é dividido em várias etapas bem definidas, cada etapa gera uma saída de dados correspondente a entrada da próxima etapa a ser executada, se assemelhando aos famosos Pipelines. Cada etapa deve ser encarregada de tratar possíveis erros ou notificá-los antes de passar para as próximas fases.


## Linguagem de Estudo T++
  A linguagem de programação escolhida para o trabalho foi a T++ linguagem essa inventada para fins acadêmicos e não é utilizada em meios comerciais. A linguagem T++ se assemelha bastante com as principais linguagem de programação compiladas do mercado por conter uma lógica de programação muito bem estruturada e familiar porém com algumas certas limitações.

  Se trata de uma linguagem considerada quase fortemente tipada pois toda e qualquer variável criada deve ser atribuída a algum tipo de dado reconhecido pela linguagem e este deve ser persistente durante toda a execução do código. Por se tratar de uma linguagem quase fortemente tipada nem todos os erros são especificados mas sempre
  deve ocorrer avisos. O código pode ser estruturado por meio de funções que se relacionam podendo ou não retornar algum valor, no caso de não retornar nada assumimos que a função em questão é do tipo void.  

  A linguagem conta com dois tipos de dados básicos sendo eles “inteiro” e “flutuante” suporta também estruturas de dados unidimensional (array) e bidimensional (matriz). Com tudo isso é possível realizar uma série de operações aritméticas e lógicas, assim com em outras linguagem como por exemplo C/C++.
