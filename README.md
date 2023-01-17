# TARS-Outpost
### TARS Webhook Relay Server
___

## Getting Started
__When using this software, you must allow external HTTP communication in order to receive webhooks__
### System Requirements
- Docker Engine

### Set environment variable
Rename `.env.sample` to `.env` and fill in the required information

| Parameter          | Description                                   |
|--------------------|-----------------------------------------------|
| PORT               | Websocket Server listen port                  |
| TOKEN              | Server Token                                  |
| WEBHOOK_SIGNATURE  | Webhook Signature provided by Twitcasting App |

### Run Server
```shell
$ docker-compose up
```