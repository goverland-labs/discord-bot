# Goverland Discord Bot

The bot allows to subscribe for updates from different DAOs.

## Prerequisites

- Python 3.10+
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

## Code Formatting

In order to format the code, run:

```bash
black src
```

### Code contribution

1. Create an issue describing a bug or feature
2. Fork the repository and create a pull request to the `main` branch
3. Please use [Black](https://pypi.org/project/black/) code formatter

## Usage

TODO: update after docker file is ready

