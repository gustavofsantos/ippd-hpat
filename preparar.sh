#!/bin/bash
npm install

# cria as pastas necessárias
mkdir pacotes
mkdir pacotes-hpat
mkdir cache 

# separa os arquivos nas suas devidas pastas
node separar-arquivos.js
node separar-arquivos-hpat.js

# cria o cache de execução
python ./python/criar_cache.py
