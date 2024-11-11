from dotenv import dotenv_values
from neo4j.exceptions import ServiceUnavailable
from neomodel import config, db
from rich.console import Console


def main():
    env = dotenv_values("./.env")
    config.DATABASE_URL = env.get("DATABASE_URL")

    try:
        results, meta = db.cypher_query("RETURN 'Hello World' as message")
        Console(style="green").print(results, meta)
    except KeyboardInterrupt:
        Console(style="bold red").print()
        Console(style="bold red").print("Quitting!")
        exit(1)
    except ServiceUnavailable:
        Console(style="bold red").print("Database Unavailable!")
        exit(1)


if __name__ == "__main__":
    main()
