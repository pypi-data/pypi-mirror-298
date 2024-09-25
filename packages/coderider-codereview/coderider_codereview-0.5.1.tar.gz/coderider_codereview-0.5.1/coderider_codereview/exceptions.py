class ConfigError(Exception):
    def __init__(self, env: str, msg: str = None):
        self._env = env
        self._msg = msg

    def __str__(self) -> str:
        if self._msg:
            return self._msg

        return f"Missing required ENV: {self._env}"
