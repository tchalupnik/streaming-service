# streaming-service

## How to start
1.  Download docker-compose 
2.  Create config file `.env`
3.  Build with `docker-compose build`
4.  Start with `docker-compose up`

## Endpoints
- HTTP: `/docs` - Open
- HTTP: `/notify` - You can start streaming
- WS: `/ws/{key}` - Establish websocket connection

## Configuration envs
Hint: Example vars you can find in `.env.example`

##### MQ config
    MQ_URL - MQ url (includes port)
    MQ_USERNAME - username
    MQ_PASSWORD - password
    DEFAULT_EXCHANGE_NAME - default exchange that will be created 

##### others envs
    RELOAD - if changing code causes reload
    PORT - port for webapp to be open

