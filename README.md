# Hackathon - Pós Tech Software Architecture

Projeto criado com o objetivo de entregar o desafio proposto pelo Curso de Software Architecture FIAP + Alura.

Neste projeto tivemos o objetivo de consolidar todos os conhecimentos adquiridos durante o curso, criando um sistema de folha de ponto em nuvem, utilizando as melhores práticas de desenvolvimento e arquitetura cloud.

## Autores
- Rafael Perin - RM349501
- Lucas Gabriel - RM349527

## Stack
- Python 3.8.16
- FastAPI
- PostgreSQL 
- Docker
- Compose

## Pré-requisitos
Para executar o projeto, é necessário ter instalado:

- [Docker version >= 20.10.7](https://www.docker.com/get-started)
- [Docker-compose version >= 1.29.2](https://docs.docker.com/compose/install/)

## Rodando com docker-compose

1. Clonar o repositório e executar o comando abaixo na raiz do projeto:

```bash
$ docker compose up -d
```

As variáveis de ambiente devem ser preenchidas para que o projeto funcione corretamente.
 
## Rodando FastAPI

Após rodar o docker-compose, executar o seguinte endereço no navegador:

```
http://localhost:8000/docs
```

Caso tenha o desejo de executar a aplicação via Insomnia ou Postman, é possível capturar os dados em http://localhost:8000/openapi.json e transformar em arquivo .json para ser importado.

## Arquitetura

Dada a simplicidade do MVP, foi escolhida a arquitetura monolítica, com o deploy feito em um cluster ECS:

<p>
    <img  src=content/arquitetura-mvp-hacka.drawio.png>
</p>

Para uma segunda fase em que será feita a evolução deste projeto, optamos por dividir o sistema em 3 serviços, através da arquitetura de microsserviços:

<p>
    <img  src=content/arquitetura-fase2-hacka.drawio.png>
</p>