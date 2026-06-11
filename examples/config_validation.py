from typewall import w

Settings = w.object(
    {
        "HOST": w.str(),
        "PORT": w.int(),
        "DEBUG": w.bool().default(False),
    }
)


def main() -> None:
    settings = Settings.parse_env(
        {"HOST": "127.0.0.1", "PORT": "8000", "DEBUG": "false"}
    )
    assert settings == {"HOST": "127.0.0.1", "PORT": 8000, "DEBUG": False}


if __name__ == "__main__":
    main()
