# Goverland Discord Bot

The bot allows to subscribe for updates from different DAOs.

## Configuration

A Python 3.10+ environment.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Code contribution

1. Create an issue describing a bug or feature
2. Fork the repository and create a pull request to the `main` branch
3. Please use [Black](https://pypi.org/project/black/) code formatter

## Usage

TODO: update after docker file is ready

### Create a local sqlite database

```
python -m src.database.create_db
```

### Run the bot

```
python -m src.run
```
