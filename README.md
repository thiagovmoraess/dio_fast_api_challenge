# Desafio FastAPI

API bancária assíncrona desenvolvida para estudo de arquitetura, boas práticas, testes e evolução incremental.

## O que o projeto faz

A aplicação permite:

- cadastrar usuários
- autenticar usuários com JWT
- criar automaticamente uma conta corrente para cada usuário cadastrado
- consultar os dados da conta autenticada
- realizar depósitos
- realizar saques
- listar as transações do usuário autenticado

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy 2.x com suporte assíncrono
- SQLite
- aiosqlite
- Alembic
- Poetry
- JWT
- pwdlib com Argon2
- Pydantic / pydantic-settings
- Pytest
- pytest-asyncio
- HTTPX

## Estrutura do projeto

O projeto está organizado em camadas simples:

- `core`: configurações, banco de dados e segurança
- `models`: entidades ORM
- `schemas`: contratos de entrada e saída
- `services`: regras de negócio
- `api/routers`: endpoints da aplicação

## Objetivo

O foco do projeto é praticar:

- desenvolvimento assíncrono com FastAPI
- organização de código em camadas
- autenticação com JWT
- persistência com SQLAlchemy
- migrations com Alembic
- testes unitários e de integração