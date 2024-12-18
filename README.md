# SustenTerra - Backend

FastAPI Backend for SustenTerra APP.
It has two main big features:

#### Marketplace

- Users can create post and sell their products
- Users favorite products from other users

#### Courses

- Users can see the available courses
- Users can enroll in courses

## Pre requisites

- Poetry (https://python-poetry.org/docs/#installation)
- Docker (https://www.docker.com/get-started/)
  - Docker Compose (https://docs.docker.com/compose/install/)
- Make (https://www.gnu.org/software/make/)
  - If on windows, you can download Make from (https://gnuwin32.sourceforge.net/packages/make.htm)
  - Or you can use WSL (https://docs.microsoft.com/en-us/windows/wsl/install)

## Installation

- Clone the repository
- (Recommended) Set poetry environment in folder `poetry config virtualenvs.in-project true`
- Run `make install` to install dependencies
- Run `make db-up` to start the database
- Run `make db-upgrade` to run migrations
- (Optionally) Run `make db-seed` to run seed and fill database with fake data
- Run `make start` to run server for the first time and run migrations

## Run

- Run `make start` to run server
- Access (http://localhost:8000/docs) to see the documentation
- To run tests run `make test`
