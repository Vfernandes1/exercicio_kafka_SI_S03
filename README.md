## Descrição das Funcionalidades de acordo com a Criação de um Consumidor de Mensagens Local

### Configuração do Docker Compose para Kafka e Zookeeper

Para a configuração do Docker Compose há necessidade da criação de três serviços: Zookeeper, Kafka e `init-kafka`. Cada um dos desses serviços possui sua especificidade conforme a definição de ambiente, segue descrição das funcionalidades
*  **Zookeeper:**
    
    *   `image: wurstmeister/zookeeper` indica que este serviço usará a imagem Docker do Zookeeper.
    *   `container_name: zookeeper` especifica o nome do contêiner como "zookeeper".
    *   `ports: - "2181:2181"` mapeia a porta 2181 do host para a porta 2181 do contêiner Zookeeper, permitindo a comunicação com o Zookeeper.
*  **Kafka:**
    
    *   `image: wurstmeister/kafka` indica que este serviço usará a imagem Docker do Kafka.
    *   `container_name: kafka-exercicio` especifica o nome do contêiner como "kafka-exercicio".
    *   `ports: - "9092:9092"` mapeia a porta 9092 do host para a porta 9092 do contêiner Kafka, permitindo a comunicação com o Kafka.
    *   `environment:` define variáveis de ambiente para o serviço Kafka, incluindo a configuração do host e a conexão com o Zookeeper.
*  **Serviço init-kafka:**
    
    *   `image: wurstmeister/kafka` indica que este serviço usará a imagem Docker do Kafka (para executar comandos Kafka).
    *   `depends_on: - kafka` garante que este serviço seja iniciado após o serviço Kafka.
    *   `entrypoint: ['bin/sh', '-c']` define o ponto de entrada para o contêiner como um shell para execução de comandos.
    *   `command:` define o comando que será executado quando o contêiner for iniciado. Neste caso, o comando cria um tópico chamado "exercicio-vini" usando o utilitário `kafka-topics.sh`. O tópico é criado com um fator de replicação de 1 e 1 partição.

Nestas etapas, basicamente realizamos a definição padrão de ambiente do Kafka e Zookeeper para o desenvolvimento local. 

Apenas para contexto, o Zookeeper é um serviço de coordenação utilizado pelo Kafka para gerenciar a configuração do cluster. 

O mais importante aqui dentro das definições é a criação tópico "exercicio-vini" e a definição das portas de acesso pelo host.

## Producer
### Descrição da Funcionalidade

Nesta etapa realizamos a parte de envio das mensagens conforme a necessidade. A partir disso utilizamos a biblioteca `confluent_kafka` para criar um produtor. Para contexto, o produtor é responsável por enviar mensagens para um tópico específico no servidor, neste caso o 'exercicio-vini". 

ps: o código também utiliza a biblioteca `socket` (embora não esteja sendo usada neste script) para criar um produtor Kafka alternativo (comentado no código), foi deixado apenas como visualização de outra possibilidade de implementação.

### O que o Código Faz?

1.  O código configura o endereço do servidor Kafka para `localhost:9092`.
2.  Um produtor Kafka é inicializado com base na configuração fornecida.
3.  Um loop `for` é usado para gerar 10 mensagens de exemplo, cada uma com uma mensagem (string) diferente contendo "I have a dream!" seguido pelo número da iteração.
4.  Cada mensagem é enviada para o tópico chamado 'exercicio-vini' no servidor Kafka.
5.  O método `flush()` é chamado após cada mensagem para garantir que a mensagem seja enviada imediatamente para o Kafka.

### O que o Código Retorna?

O código não retorna explicitamente cada uma das mensagens, no entanto retorna um processo de validação, se a execução for bem-sucedida, ele imprimirá a seguinte mensagem no console:

`Mensagens enviadas com sucesso!`

### Resultado Esperado

Após a execução do código, 10 mensagens serão enviadas para o tópico 'exercicio-vini' no servidor Kafka configurado para `localhost:9092`. Sendo assim, estas mensagens estarão disponíveis para consumo por qualquer consumidor Kafka conectado ao mesmo tópico no servidor Kafka.

## Consumer

### Descrição da Funcionalidade

Nesta parta há implementação do consumidor. Para a implementação do consumidor, utilizei a biblioteca `confluent_kafka` para consumir mensagens do tópico especificado ('exercicio-vini'). Após isso, o consumidor é configurado para se conectar ao tópico 'exercicio-vini' no servidor, na porta `localhost:9092`. 

Quando executado, o consumidor fica em um loop contínuo, aguardando novas mensagens serem produzidas no tópico.

### O que o Código Faz

1.  O código configura o endereço do servidor Kafka para `localhost:9092` e o grupo de consumidores como 'exercicio\_ponderada'.
2.  A função `logica_consumer()` é definida para processar o consumidor.
3.  O consumidor é inicializado com base na configuração fornecida e se inscreve ("subscribe") no tópico 'exercicio-vini'.
4.  O consumidor fica em um loop contínuo (`while True`) e periodicamente (a cada segundo) verifica se há novas mensagens no tópico.
5.  Se uma nova mensagem é recebida, ela é impressa no console.
6.  O loop continua até que o programa seja interrompido por um sinal de teclado (Ctrl + C).
7.  Após interrompido, o consumidor é fechado usando o método `consumer.close()`.

### O que o Código Retorna

O código em si, após ser rodado (em python) e com o container já "buildado" retorna as 10 mensagens que foram enviadas, sendo assim é esperado que após a execução ser bem-sucedida, há a impressão no console das mensagens recebidas do tópico 'exercicio-vini'. 

ps: se houver qualquer erro durante a execução, o erro será impresso no console, a partir das informações implementadas

![image (34-1-1)](https://github.com/2023M8T4Inteli/grupo5/assets/99264567/8c4f97fa-ac40-4968-951c-39750c006e1e)

### Resultado Esperado

Quando o código é executado, ele permanece em execução, consumindo mensagens do tópico 'exercicio-vini' no servidor Kafka configurado para `localhost:9092`. À medida que novas mensagens são produzidas no tópico, o consumidor as imprime no console. O código continua a consumir mensagens indefinidamente até ser interrompido manualmente pelo usuário (pressionando Ctrl + C).
