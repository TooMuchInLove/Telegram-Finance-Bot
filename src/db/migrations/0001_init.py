"""Init."""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            CREATE TABLE account (
                id SERIAL PRIMARY KEY,
                telegram_user_id BIGINT NOT NULL UNIQUE,
                telegram_username VARCHAR(100) NOT NULL UNIQUE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """,
        """
            DROP TABLE account;
        """,
        """
            CREATE INDEX index_telegram_user_id ON account(telegram_user_id);
        """,
        """
            DROP INDEX index_telegram_user_id;
        """,
    ),
    step(
        """
            CREATE TABLE category (
                name VARCHAR(100) NOT NULL CHECK (LENGTH(name) >= 3),
                account_id INT REFERENCES account(id),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (name, account_id)
            );
        """,
        """
            DROP TABLE category;
        """,
    ),
    step(
        """
            CREATE TABLE category_detail (
                name VARCHAR(100) NOT NULL CHECK (LENGTH(name) >= 3),
                category_name VARCHAR(100) NOT NULL CHECK (LENGTH(name) >= 3),
                account_id INT REFERENCES account(id),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_name, account_id) REFERENCES category(name, account_id),
                PRIMARY KEY (name, account_id)
            );
        """,
        """
            DROP TABLE category_detail;
        """,
    ),
    step(
        """
            CREATE TABLE wallet (
                name VARCHAR(100) NOT NULL CHECK (LENGTH(name) > 1),
                current_score DECIMAL NOT NULL DEFAULT 0.0,
                account_id INT REFERENCES account(id),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (name, account_id)
            );
        """,
        """
            DROP TABLE wallet;
        """,
    ),
]
