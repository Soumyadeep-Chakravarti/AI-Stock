default:
    @just --list

format:
    uv run ruff format .
    nixfmt .nix/flake.nix
    shfmt -w .envrc

lint:
    uv run ruff check .
    deadnix .nix/flake.nix
    statix check .nix
    shellcheck .envrc
    shfmt -d .envrc
    yamllint .pre-commit-config.yaml .github
    actionlint

typecheck:
    uv run basedpyright

test:
    uv run pytest -v

coverage:
    uv run pytest --cov=ai_stock --cov-report=term-missing

audit:
    uv export --locked --all-groups --no-emit-project --format requirements-txt | pip-audit --requirement /dev/stdin

nix-check:
    nix flake check ./.nix

check: lint typecheck test nix-check

pre-commit:
    uv run pre-commit run --all-files

environment:
    python --version
    uv --version
    nix --version
    just --version
