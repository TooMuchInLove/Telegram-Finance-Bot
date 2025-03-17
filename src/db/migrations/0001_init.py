"""Init."""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            CREATE TABLE account (
                id SERIAL PRIMARY KEY,
                telegram_user_id BIGINT NOT NULL UNIQUE,
                telegram_username TEXT NOT NULL UNIQUE,
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
                name text NOT NULL,
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
            CREATE TABLE custom_digital_accounts (
                id SERIAL PRIMARY KEY,
                account_id INT REFERENCES account(id),
                name TEXT NOT NULL,
                tag TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """,
        """
            DROP TABLE custom_digital_accounts;
        """,
    ),
    step(
        """
            CREATE TABLE fixate_expenses (
                id SERIAL PRIMARY KEY,
                account_id INT REFERENCES account (id),
                category_id TEXT REFERENCES category (name),
                custom_digital_account_id INT REFERENCES custom_digital_accounts (id),
                amount NUMERIC(100, 2) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """,
        """
            DROP TABLE fixate_expenses;
        """,
    ),
]
