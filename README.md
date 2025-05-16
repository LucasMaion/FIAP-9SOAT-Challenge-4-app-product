# FIAP-9SOAT-Challenge-1

## Sobre o projeto
O projeto se trata de uma implementação de backend em Python utilizando os frameworks Fast API e Peewee ORM.

Projetado utilizando os conceitos de Domain Driven Design.
Implementado utilizando conceitos de Hexagonal Architecture
Desenvolvimento utilizando conceitos de Test Driven Development

O objetivo do projeto de demonstrar as implementações técnicas dos conceitos citados acima, servindo como base de analise do aprendizado adquerido durante a Fase 1 do curso de Software Architecture turma 9 da FIAP.

### Meta Conceito

Uma solução de gerenciamento de pedidos de restaurante, com uma API para gerenciamento de produtos, clientes, pedidos e fila de preparo para cozinha (backoffice).

A empresa contratou a fabrica de software para desenvolver uma solução escalável em nuvem para criar terminais de auto atendimento presencial em seus estabelecimentos. Devido ao crescimento da empresa o controle 100% manual em papel não é mais viável, assim como manter o custo de uma equipe de atendimento em balcão.

## Realizando Build
## Utilizando Imagem Docker
Garanta que tenha o docker e docker-compose instalados em seu ambiente e execute o comando `docker-compose -f docker-compose.dev.yml up -d` e acesse [localhost:8000](http://localhost:8000) para abrir o projeto.

## Utilizando ambiente local
### Instalando dependências
Garanta que possua o [python ^3.12.6](https://www.python.org/) instalado, instale o [poetry](https://python-poetry.org/docs/#installing-with-pipx) execute o command ``poetry install`` na raiz do projeto.

Suba uma imagem local ou remota do [postgreSQL](https://www.postgresql.org/), configure o ambiente local clonando .env_dev para .env e preenchendo as variáveis de ambiente.



### Iniciando Ambiente Dev
Execute o comando ``poetry run uvicorn app:app --reload`` na raiz do projeto

## Executando Testes unitários
Execute o comando ``poetry run pytest`` na raiz do projeto.

## Infraestrutura
Para subir a infraestrutura completa em Kubernetes recomenda-se utilizar o [minikube](https://minikube.sigs.k8s.io/docs/)

Antes de subir os pods e serviços recomenda-se que o ambiente do minikube seja zerado com o comando:
``minikube delete --all``

Inicie o minikube:
``minikube start``

mude o contexto do seu docker para dentro do minikube:
``eval $(minikube docker-env)``

Confira que o seu ambiente docker está correto, o output dos seguintes comandos devem ser idênticos:
``minikube ssh docker images``
``docker images``

construa a imagem docker no ambiente do minikube:
``docker build -f ./docker/app.Dockerfile  --target dev -t fiap-9soat-challenge-2-main_app:latest .``

Aplique os recursos do Kubernetes:
``kubectl apply -f k8s/configmap.yaml``
``kubectl apply -f k8s/secret-template.yaml``
``kubectl apply -f k8s/postgre-deployment.yaml``
``kubectl apply -f k8s/postgre-service.yaml``
``kubectl apply -f k8s/app-deployment.yaml``
``kubectl apply -f k8s/app-service.yaml``
``kubectl apply -f k8s/hpa.yaml``

Verifique se todos os Pods e serviços foram inicializados corretamente:
``kubectl get pods,svc``
Iniciei o tunnel do minikube para ganhar acesso do seu ambiente local ao serviço app exposto no ambiente do minikube:
``minikube tunnel``
Copie o IP publico gerado pelo minikube

Em outro terminal, reinicie o deployment do app:
``kubectl rollout restart deployment app``

pode verificar se a execução esta ocorrendo corretamente coletando os logs do pod do app:
``kubectl logs <pod>``

O deployment do zero não alimenta o banco de dados, para isso execute as seguintes rotas no Postman, insomnia ou aplicativo de sua preferencia, sem nenhum argumento, ou corpo necessário:
``POST <tunnel ip>:30000/build_db``
``POST <tunnel ip>:30000/seed_db``

Agora basta acessar a documentação swagger:
``GET <tunnel ip>:30000/docs``

## Swagger / ReDoc

Quando estiver com o servidor rodando localmente, ou via container acesse [localhost:8000/docs](http://localhost:8000/docs) ou [localhost:8000/redoc](http://localhost:8000/redoc)

#### Webhook

Para o uso do webhook, a documentação disponibiliza um endpoint exemplo com o corpo de requisição que é enviado pelo webhook.


## Simulando o projeto

Para simular o uso comum do projeto, garanta que o banco esteja alimentado com os dados de teste
Abaixo seguem alguns passos com os endpoints correspondentes

#### Criando um produto
Lista as categorias de produtos para usar na criação:
``GET /produtos/categories``

Deleta um produto - Apenas produtos que não tem associação com algum pedido e que estejam inativos podem ser deletados
``DELETE /produto/{item_id}``

Cria um novo produto - Produtos sempre inciam inativos e sem componentes
``POST /produto``

Atualiza um produto, importante para expandir os componentes do produto
``PUT /produto``

Ativa um produto que esteja inativo - disponibiliza ele para ser adicionado a produtos
``Patch /produto/activate/{item_id}``

Inativa um produto ativo - impede que o produto para ser adicionado a novos pedidos
``Patch /produto/deactivate/{item_id}``

#### Criando um pedido
List produtos existentes e ativos pela listagem de produtos:
``GET /produto/index``

Inicie um novo pedido, todos pedido inicia vazio:
``POST /pedido``

Adicione quantos produtos desejar ao pedido ativo em criação:
``PATCH /pedido/{pedido_id}/add_product/{product_id}``

Adicione componentes aos produtos ja selecionados (Ex. queijo a um lanche já no pedido), aqui o componente deve ter a classificação correta entre os produtos:
``PATCH /pedido/{pedido_id}/{product_id}/add_component/{component_id}``

Concluir um pedido Ativo - Essa etapa só pode ocorrer se o pedido tiver um pagamento efetuado:
``PATCH /pedido/conclude/{pedido_id}``

Cancelar um pedido ativo - Essa etapa só pode ocorrer se o pedido não tiver um pagamento efetuado:
``PATCH /pedido/cancel/{pedido_id}``

#### Pagando um pedido
Liste os métodos de pagamentos disponíveis:
``GET /payment/methods``

Iniciei o processo de pagamento - Aqui repasse um webhook para receber o evento de finalização de pagamento:
``POST /payment``

#### Cadastrando um cliente

Inclua seus dados pessoais, CPFs não podem ser duplicados:
``POST /cliente``

#### Gerenciando a fila
Pega a lista completa de pedidos que estão na fila - aqui constam apenas pedidos pagos e finalizados que entraram em fase de preparo:
``GET /queue``

Atualiza um pedido um um novo status, conforme enumeração interna:
``PUT /queue``

Status válidos para atualizar na fila de pedidos:
- EM_PREPARO = 6
- PRONTO_PARA_ENTREGA = 7
- ENTREGUE = 8
- FINALIZADO = 9
## Anexo

[Documentação original da Fase 1](/documentation/Pos_tech%20-%20Fase%201%20-%20Tech%20Challenge%20Fast%20Food.pdf)
[Documentação original da Fase 2](/documentation/Postech%20-%20Fase%202%20-%20Tech%20Challenge.pdf)
[Event Storming E Refinamento Técnico](https://miro.com/app/board/uXjVLf9MJLo=/?share_link_id=933574423173)
[Outras documentações](https://www.notion.so/101117753c9f80cbb28dd5665c721433?v=101117753c9f800b95da000c73dea574&pvs=4)
[Arquitetura Simplificada](/documentation/arquiteturas%20simplificadas.png)
[Domain StoryTelling](/documentation/Domain%20Storytelling.png)
[Infraestrutura](/documentation/infraestrutura.png)
