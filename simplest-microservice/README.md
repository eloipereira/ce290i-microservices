# TCP Listener and Publisher with `socat` in Docker

This project demonstrates how to use `socat` to implement a TCP listener and publisher in Docker. The listener container listens for incoming TCP connections, and the publisher containers send messages to the listener every second. The messages are interleaved and displayed in the listener’s terminal.

## Prerequisites

- Docker installed on your system.
- Basic knowledge of Docker and Docker networks.

## Setup Instructions

### 1. Build the Docker Images

#### Build the Listener Image

To build the listener Docker image, run the following command:

```bash
docker build -t listener -f dockerfile.listener .
```

#### Build the Publisher Image

To build the publisher Docker image, run this command:

```bash
docker build -t publisher -f dockerfile.publisher .
```

### 2. Create a Docker Network

Create a custom Docker network so that the containers can communicate with each other:

```bash
docker network create my-network
```

### 3. Run the Listener Container

Start the listener container, which will listen for incoming TCP connections on port 12345:

```bash
docker run --rm --name listener --network my-network -t listener
```

This container will continuously print messages it receives from the publisher(s).

### 4. Run Publisher Containers

Start one or more publisher containers. Each publisher will send a message to the listener every second.

**Example: Start Publisher 1**

```bash
docker run --rm --name publisher1 --network my-network -t publisher
```

**Example: Start Publisher 2**

```bash
docker run --rm --name publisher2 --network my-network -t publisher
```

You can start as many publishers as needed. Each publisher will send messages to the listener, and the listener will print the interleaved messages.

### 5. Expected Output

The listener container will display messages from all active publishers. For example:Hello from Publisher1! Fri Nov 17 12:34:56 UTC 2024

```
Hello from Publisher2! Fri Nov 17 12:34:57 UTC 2024
Hello from Publisher1! Fri Nov 17 12:34:58 UTC 2024
Hello from Publisher2! Fri Nov 17 12:34:59 UTC 2024
```

### 6. Stopping the Containers
You can stop any running containers by pressing Ctrl+C in their terminal, or by running:

```bash
docker stop publisher1
docker stop publisher2
docker stop listener
```

This will stop the respective containers.

### 7. Using docker-compose

To simplify building and running the microservices we provide a docker-compose file named `docker-compose.yml`.

To build all the services type:

```bash
docker-compose build
```

and

```bash
docker-compose run
```

to run them.

To stop the services use:
```bash
docker-compose down
```

and

```bash
docker-compose rm
```

ro release the resources.

### 7. Using volumes

To demonstrate the use of volumes we create another version of the listener service (`dockerfile.listen_and_dump`) that, instead of printing into `stdout` it dumps the messages to a file named `messages.log`.

We also create a new service that share a volume with the new listener where the file is saved, reads the file and prints the results.

To build the new listener type:

```bash
docker build -t listen-and-dump -f dockerfile.listen_and_dump .
```

and

```bash
docker build -t reader -f dockerfile.reader .
```

to build the new reader service.

We also need to create a new volume using the following command:

```bash
docker volume create shared-volume
```

To run the containers execute the following commands:

```bash
docker run --rm --name listener --network my-network --volume shared-volume:/shared -t listen-and-dump
```

```bash
docker run --rm --name reader1 --volume shared-volume:/shared -t reader
```

```bash
docker run --rm --name publisher1 --network my-network -t publisher
```

```bash
docker run --rm --name publisher2 --network my-network -t publisher
```

You can also use the following docker-compose file:

```bash
docker-compose -f docker-compose-shared.yml build
```

```bash
docker-compose -f docker-compose-shared.yml up
```

Notes:

Note that we do not need to mount the volumes in the publishers since they don't use it.

Also, we do not need to need to attach the network to the reader since it doesn't need it. It communicates with the listener by a shared state, i.e. the file `messages.log`.

Using plain text files to share state between microservices is not a common practice. Usually one would use cache database (e.g. redis) for this effect. We are solely demonstrating the use of volumes to share files between docker containers.
