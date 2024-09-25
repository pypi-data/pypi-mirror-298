from litellm import completion

from coderider_codereview import configs
from coderider_codereview.exceptions import ConfigError


class LitellmClient:

    def chat_completions(self, messages: list):
        model = configs.CR_LLM_MODEL
        if not model:
            raise ConfigError("CR_LLM_MODEL")

        api_key = configs.CR_LLM_API_KEY
        base_url = configs.CR_LLM_BASEURL
        options = configs.CR_LLM_OPTIONS

        options.pop("model", None)
        options.pop("messages", None)
        options.pop("api_key", None)
        options.pop("base_url", None)

        response = completion(model=model, messages=messages, api_key=api_key, base_url=base_url, **options)
        return response
