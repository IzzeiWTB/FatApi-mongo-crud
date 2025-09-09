API de Usuários com FastAPI, MongoDB e Docker
Este é um projeto de API REST para um CRUD (Create, Read, Update, Delete) de usuários, desenvolvido com FastAPI e persistência de dados em um banco de dados NoSQL, o MongoDB. A aplicação e o banco de dados são orquestrados utilizando Docker e Docker Compose.

Objetivos de Aprendizagem
Docker Compose: Orquestração de um ambiente de desenvolvimento com múltiplos contêineres (API + Banco de Dados).

FastAPI: Modelagem e exposição de endpoints RESTful de forma moderna e assíncrona.

MongoDB com Motor: Persistência de dados de forma assíncrona, ideal para aplicações de alta performance.

Pydantic V2: Validação robusta de dados de entrada e saída, garantindo a integridade dos dados.

Boas Práticas: Implementação de filtros, paginação, tratamento de erros específicos (como e-mail duplicado) e uso de índices para otimização de consultas.

Requisitos
Docker

Docker Compose

Como Executar o Projeto
Clone o repositório (ou salve os arquivos em uma pasta com a estrutura indicada).

Navegue até a raiz do projeto (a pasta fastapi-mongo-crud).

Suba os contêineres com Docker Compose:

docker compose up --build

Este comando irá construir a imagem da API, baixar a imagem do MongoDB e iniciar os dois serviços.

Acesse a documentação interativa (Swagger UI):
Abra seu navegador e acesse: http://localhost:8000/docs

Lá você poderá testar todos os endpoints de forma interativa.

Exemplos de Requisições (cURL)
Aqui estão alguns exemplos de como interagir com a API usando curl.

1. Criar um novo usuário
Requisição:

curl -X 'POST' \
  'http://localhost:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Maria Silva",
  "email": "maria.silva@example.com",
  "age": 28,
  "is_active": true
}'

Resposta (Sucesso 201):

{
  "name": "Maria Silva",
  "email": "maria.silva@example.com",
  "age": 28,
  "is_active": true,
  "id": "6724125b39a3f08969b7364b"
}

2. Listar usuários (com filtros e paginação)
Requisição (buscando por 'joão', idade entre 25 e 40, apenas ativos, na primeira página):

curl -X 'GET' \
  'http://localhost:8000/users?q=jo%C3%A3o&min_age=25&max_age=40&is_active=true&page=1&limit=10' \
  -H 'accept: application/json'

Resposta (Sucesso 200):

[
  {
    "name": "João da Silva",
    "email": "joao.silva@example.com",
    "age": 30,
    "is_active": true,
    "id": "672412e939a3f08969b7364c"
  }
]

3. Obter um usuário pelo ID
Requisição:

curl -X 'GET' \
  'http://localhost:8000/users/672412e939a3f08969b7364c' \
  -H 'accept: application/json'

Resposta (Sucesso 200):

{
  "name": "João da Silva",
  "email": "joao.silva@example.com",
  "age": 30,
  "is_active": true,
  "id": "672412e939a3f08969b7364c"
}

4. Atualizar um usuário
Requisição (atualizando a idade e o status):

curl -X 'PUT' \
  'http://localhost:8000/users/672412e939a3f08969b7364c' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 31,
  "is_active": false
}'

Resposta (Sucesso 200):

{
  "name": "João da Silva",
  "email": "joao.silva@example.com",
  "age": 31,
  "is_active": false,
  "id": "672412e939a3f08969b7364c"
}

5. Deletar um usuário
Requisição:

curl -X 'DELETE' \
  'http://localhost:8000/users/672412e939a3f08969b7364c' \
  -H 'accept: */*'

Resposta:
A resposta será um 204 No Content, sem corpo, indicando que o usuário foi removido com sucesso.