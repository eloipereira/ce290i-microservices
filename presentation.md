---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# Large-scale systems using microservices

CE290I - Control and information management
Systems Engineering, UC Berkeley


Elói Pereira, PhD
Head of Data Science, Car IQ Inc.
eloi@berkeley.edu
eloi@gocariq.com
[eloipereira.com](https://www.eloipereira.com)

November, 2023


---

# Microservices Architectures

* Independently developed, deployed, and managed
* Easy to maintain and evolve
* Scalable and reliable
* Containerization makes them agnostic to the infrastructure
* Easy to deploy in the cloud
* Flexible and agile

---
 # A simple example - GPS Replay

* A simulator reads vehicle data (e.g. GPS location) from a csv file and replays it
* The current location of the vehicle needs to be served to a variety of other applications, e.g.:
  * a web app for visualization
  * an app that monitors and computes metrics

---

# What you need to run GPS Replay

- [Git](https://git-scm.com/downloads)
- [Docker Engine](https://docs.docker.com/engine/install/)
- A command line interface (e.g. bash, terminal)


---
# Installation and execution

- Clone the git repo
  - [https://github.com/eloipereira/ce290i-microservices](https://github.com/eloipereira/ce290i-microservices)
- From your favorite CLI:
- Run `docker-compose up -d` to build and turn on the microservices
- Run `docker-compose down`  to turn them off

---

# Programming Language

Python

* Version: 3.12
* Libraries:

  - FastAPI
  - Pydantic
  - Uvicorn

---

# Database and message broker

Redis

* Version: 7.2

---
# Development tools (optional)

- [Pyenv](https://github.com/pyenv/pyenv): Python version management
- [VSCode](https://code.visualstudio.com/download): Editor
- Pylance: python support for VSCode
- Flake8 linter
- Black formatter
- Pre-commit
- Marp to build this presentation

---

# REST API

- Access the Swagger API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)
