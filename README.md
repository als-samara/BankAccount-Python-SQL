# Bank Account com Python e SQL

Desafio do Bootcamp "Python AI Backend Developer" que consiste em modelar um sistema bancário em POO com Python.

## Implementação

O projeto foi implementado utilizando o PyCharm, funções Python e MySQL connector para a execução de queries e mapeamento das entidades para objetos. Foi aplicado o padrão MVC (Model-View-Controller).

## Funcionalidades
- Cadastrar Usuário
- Cadastrar e Deletar Conta Corrente
- Sacar
- Depositar
- Transferir valor entre contas
- Listar Contas
- Listar Contas do Usuário
- Ver Extrato

## Requisitos

- PyCharm (versão mais recente) ou outra IDE de sua preferência
- Python versão 3 ou superior
- MySQL

## Executando o projeto

Para executar o projeto localmente, execute o comando git clone, navegue até a pasta do repositório e execute o comando:

```
pip install mysql-connector-python
```

No arquivo db-connection.py altere o usuário e a senha do MySQL na chamada da função create_server_connection e execute o arquivo. Após a primeira execução, o projeto irá criar o banco de dados e as tabelas. Para evitar erros nas demais execuções do projeto, comente as linhas 91 a 95 do arquivo db_connection.py.

## Contribuições

Encontrou algum erro ou gostaria de contribuir com melhorias ao projeto? Crie uma branch, commite as suas alterações e abra um pull request para a branch main.

## Entre em contato

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2)](https://www.linkedin.com/in/samara-almeida-als/)  [![Email](https://img.shields.io/badge/Email-EA4335)](mailto:samaraalmeida379@gmail.com)
