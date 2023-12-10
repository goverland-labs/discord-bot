# Goverland Discord Bot

The bot allows to subscribe for updates from different DAOs.

## Prerequisites

- Python 3.11+
- Install [virtualenv](https://virtualenv.pypa.io/en/latest/index.html)
```bash
pip3 install virtualenv
```
- Create a virtual env and activate it
```bash
python3 -m virtualenv .venv
source .venv/bin/activate
```
- Install all dependencies
```bash
pip install -r requirements.txt
```

## Local Development

1. Create a local sqlite database
```
python -m src.database.create_db
```
2. Rename `.env.example` to `.env` and define a Discord token
3. Run the bot
```
python -m src.run
```

## Run Docker Locally

If yo want to test a Docker image, run the following:

1. Build a Docker image
```bash
./bin/docker_build.sh
```
2. Start the Docker image
```bash
./bin/docker_run.sh
```

## Code Linting

We lint code with flake8:

```bash
flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

## Code Formatting

In order to format the code, run:

```bash
black src
```

## Testing

We test code using pytest:
```bash
pytest
```

### Code contribution

1. Create an issue describing a bug or feature
2. Fork the repository and create a pull request to the `main` branch
3. Please use [Black](https://pypi.org/project/black/) code formatter

## Usage

TODO: update after docker file is ready
