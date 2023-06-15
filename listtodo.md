# Ideias e Recursos

## Servers e Hosts

* fly.io;
* vercel;
* railway.
* KingHost
* Oracle Server (Cloud/VPN)

## Features (Mais recursos para o crawler e bot)


- [ ] Cria banco de dado para salvar link/dados das notícias.
- [ ] Adicionar o site de noticias e negócios Epoca Negócios/Globo (https://epocanegocios.globo.com/)
- [ ] Adicionar notícias do portal do Jornal ["Folha de São Paulo"](https://www.folha.uol.com.br/). 
- [ ] Implementar o agendamento da mensagem de notíticia do dia. (usar modulo de agendamento de tarefa e de manipulação de data e hora(exemplo sched, e datetime para agendamentos e data/hora respectivamente). Usando _Rocketry_.
- [x] Adicionado site de noticias da TV Band.  
- [x] Uso de programação assincrona na execução de tarefas do bot (módulo asyncio, vide doc do python ).* [em analise]*
- [x] Dados salvos no formato json, csv e xlsx.

- [x] Criar uma classe base mais genérica que modela o crawler e scrapper.
- [x] Refatoração Etapa 1: Rescrita dos módulo crawler e criação do módulo tracker contendo funções para tratar conteúdo de cada site em especifico (no momento a saber BBC Brasil, Band, CNN Brasil, G1/Globo).
