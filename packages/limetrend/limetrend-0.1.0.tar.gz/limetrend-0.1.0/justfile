set shell := ["bash", "-uc"]

default:
    @just --list

format:
    just --unstable --fmt
    ruff format .
    ruff check --fix .

costs:
    limetrend dynamodb

costs-custom:
    python -m limetrend dynamodb --days 60
