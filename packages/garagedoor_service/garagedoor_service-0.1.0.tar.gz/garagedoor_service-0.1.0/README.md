# garagedoor-service

This project implements a simple webservice that can be used to open/close a garagedoor 
with a typical Chamerlain or equivalent motor. It relies on a Raspberry Pi's GPIO pins 
to drive a (solid-state) relay to short-cirquit the motor terminals that initiate motion.
Additionally, two pins are used to detect the garage door being fully opened or closed. 

## Configuration

The service is configured in `config.yaml` in the working directory. This path can be
overwritten with the `GARAGEDOOR_SERVICE_CONFIG` environment variable.

Note that all fields in `config.yaml` are mandatatory and should contain some sane value.

### Operation mode

By setting mode to `development`, the GPIO interface will not be used and the state will
only be printed to stdout.

```yaml
mode: development
```

Set this variable to `production` if you want to drive the actual GPIO pins. Note, this
will require that the code is run on a Rasberry Pi or analog.

### Bind address and port

Define to which host and port uvicorn should bind.

```yaml
bind:
  port: 8000
  host: 127.0.0.1
```

### GPIO

This section defines the GPIO pins used for toggling the motor relay, and reading the sensors 
for the door's position.

```yaml
gpio:
  toggle_pin: 11
  open_pin: 21
  closed_pin: 22
```

The numers should match the labeling on the board's GPIO spec. Not the numbers defined by the
chipset (which is prone to change between different versions of RPis).

### API Keys

Defines a list of API keys that should have access to this service. API keys should be hashed
with bcrypt.

```yaml
api_keys:
  - $2y$10$3lHF35DW58Cse5gtU9DBMukIcUkQNNclSk3SDLArd4g2/8xC12Qb2
```

## Routes

The following routes are available:

 - POST /toggle

   ```json
   {
     "result": "ok"
   }
   ```

   Toggle the door motor. This call requires a valid api-key that should be specified in the
   `x-api-key` header.

- GET /state
  ```json
  {
    "result": "ok",
    "state": "closed"
  }
  ```

  Get the door's state. This can either be `open`, `closed` or `unknown`. This call requires 
  a valid api-key that should be specified in the `x-api-key` header.

- GET /healthz
  GET /readyz
  ```json
  {
    "result": "ok"
  }
  ```

  Basic health and readiness checks. These require no authentication.

## Running

Run this service with the following command.

```bash
garagedoor-service
```
