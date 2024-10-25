README.MD
# **1. Problema de negócio**
A Cury Company é uma empresa de tecnologia que criou um aplicativo
que conecta restaurantes, entregadores e pessoas na Índia.

Através desse aplicativo, é possível realizar o pedido de uma refeição, em
qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por
um entregador também cadastrado no aplicativo da Cury Company.

A empresa realiza negócios entre restaurantes, entregadores e pessoas,
e gera muitos dados sobre entregas, tipos de pedidos, condições
climáticas, avaliação dos entregadores e etc. Apesar da entrega estar
crescento, em termos de entregas, o CEO não tem visibilidade completa
dos KPIs de crescimento da empresa.

A Cury Company possui um modelo de negócio chamado Marketplace,
que fazer o intermédio do negócio entre três clientes principais:
Restaurantes, entregadores e pessoas compradoras. Para acompanhar o
crescimento desses negócios, o CEO gostaria de ver as seguintes
métricas de crescimento:

## Visão empresa:
1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
5. A quantidade de pedidos por entregador por semana.
6. A localização central de cada cidade por tipo de tráfego.

## Visão entregador:
1. A menor e maior idade dos entregadores.
2. A pior e a melhor condição de veículos.
3. A avaliação médida por entregador.
4. A avaliação média e o desvio padrão por tipo de tráfego.
5. A avaliação média e o desvio padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por cidade.
7. Os 10 entregadores mais lentos por cidade.

## Visão restaurantes:
1. A quantidade de entregadores únicos.
2. A distância média dos resturantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por cidade.
4. O tempo médio e o desvio padrão de entrega por cidade e tipo de
pedido.
5. O tempo médio e o desvio padrão de entrega por cidade e tipo de
tráfego.
6. O tempo médio de entrega durantes os Festivais.
   
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que
exibam essas métricas da melhor forma possível para o CEO.

## 2. Premissas assumidas para análise
1. A análise foi realizada com dados entre 11/02/2022 e 13/04/2022
2. O modele de negócio é um Marketplace
3. Foco em três principais visões: empresa, restaurante e entregadores

## 3. Estratégia de solução
O dashboard foi desenvolvido para mostrar as três áreas mais importantes da empresa.

Cada visão representa um conjunto de métricas.

1. Visão do crescimento da empresa
  a. Pedidos por dia
  b. Porcentagem de pedidos por condições de trânsito
  c. Quantidade de pedidos por tipo e por cidade.
  d. Pedidos por semana
  e. Quantidade de pedidos por tipo de entrega
  f. Quantidade de pedidos por condições de trânsito e tipo de cidade

2. Visão do crescimento dos restaurantes
  a. Quantidade de pedidos únicos.
  b. Distância média percorrida.
  c. Tempo médio de entrega durante festival e dias normais.
  d. Desvio padrão do tempo de entrega durante festivais e dias
  normais.
  e. Tempo de entrega médio por cidade.
  f. Distribuição do tempo médio de entrega por cidade.
  g. Tempo médio de entrega por tipo de pedido.
  
3. Visão do crescimento dos entregadores
  a. Idade do entregador mais velho e do mais novo.
  b. Avaliação do melhor e do pior veículo.
  c. Avaliação média por entregador.
  d. Avaliação média por condições de trânsito.
  e. Avaliação média por condições climáticas.
  f. Tempo médido do entregador mais rápido.
  g. Tempo médio do entregador mais rápido por cidade.

## 4. Top 3 Insights de dados
 1. Na Índia, no final de fevereiro, há um feriado nacional chamado Maha Shivaratri. 
 Sugiro que os restaurantes preparem pratos especiais e adicionem uma seção em destaque 
 no aplicativo antes do feriado. Além disso, seria interessante ampliar as parcerias com 
 restaurantes que já oferecem menus especiais para essa ocasião.

 2. Na visão dos entregadores, a avaliação média por tipo de trânsito mostra que os
 tipos de trânsito "engarrafamento" (jam) e "baixo" (low) têm praticamente a mesma média 
 de tempo de entrega, o que não faz sentido. Pode estar havendo um problema na mensuração 
 desse tempo de entrega ou nas rotas de entrega.

 3. Na visão dos restaurantes, ao avaliar a distância das entregas, o tempo médio de entrega 
 e o desvio padrão por cidade e tipo de pedido, observa-se que o semi-urbano apresenta o maior 
 tempo de espera com o menor desvio padrão. Isso indica que os clientes pedem comida em 
 restaurantes mais distantes. Uma possível solução seria ampliar as parcerias com restaurantes 
 no perímetro semi-urbano, o que reduzirá o tempo de entrega.


# 5. O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em
qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link:https://dashcurrycompany-3vhvcn5g7weyfedxj46sdk.streamlit.app/


# 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que
exibam essas métricas da melhor forma possível para o CEO.

# 7. Próximo passos
1. Reduzir o número de métricas.
2. Criar novos filtros.
3. Adicionar novas visões de negócio.