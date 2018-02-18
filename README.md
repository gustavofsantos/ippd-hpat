# Repositório contendo a implementação para o trabalho 3 da disciplina de Introdução ao Processamento Paralelo e Distribuído.

## Autores: Gustavo Santos, Eduardo Model

Uma sequência de passos é necessária para a utilização da solução desenvolvida. Após clonar este repositório, deve ser baixado os pacotes do NojeJS necessários, bem como o arquivo de dados bruto. Esta etapa é completada ao executar o comando ```npm install``` na pasta raiz do projeto. Em seguida é necessário criar o cache, executando o comando ```python ./python/criar_cache.py```. Se não houver erros, o programa estará pronto para uso.


Um exemplo real de execução pode ser visto a seguir.

```
(HPAT) root@e0db17fa358d:~/ippd/python# python pesquisar.py react native
[02:05:26] INICIO
[02:05:26] PESQUISANDO POR: 'react native'
[02:05:26] PROCESSANDO PESQUISA
[02:05:30] RESULTADOS DA PESQUISA
[ ('babel-preset-react-native', 6198.156287999999) ]
[ ('react', 5612.868431999999) ]
[ ('react-native', 4557.560742) ]
[ ('react-dom', 4302.453024000002) ]
[ ('eslint-plugin-react', 3800.0495519999968) ]
[ ('babel-preset-react', 2247.7264290000003) ]
[ ('react-native-vector-icons', 1946.28096) ]
[ ('eslint-plugin-react-native', 1624.396032) ]
[ ('react-native-mock', 1449.0828800000002) ]
[ ('react-test-renderer', 1323.3922559999996) ]
[02:05:30] FIM
```
