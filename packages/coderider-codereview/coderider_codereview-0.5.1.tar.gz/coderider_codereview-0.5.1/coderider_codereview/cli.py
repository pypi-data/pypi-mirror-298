import asyncio
import time

from coderider_codereview import configs
from coderider_codereview.ai_bot_note import AiBotNote
from coderider_codereview.coderider_client import CoderiderClient
from coderider_codereview.exceptions import ConfigError
from coderider_codereview.feature_types import FeatureTypes
from coderider_codereview.gitlab_client import GitlabClient
from coderider_codereview.litellm_client import LitellmClient
from coderider_codereview.note_types import NoteTypes
from coderider_codereview.prompt.code_review import CodeReview
from coderider_codereview.prompt.sast_explain import SastExplain
from coderider_codereview.prompt.secret_detection import SecretDetection


def merge_request(llm_client, gitlab_client):
    messages = CodeReview().all_messages()
    llm_resp = llm_client.chat_completions(messages)
    llm_content = llm_resp["choices"][0]["message"]["content"]
    content = f"# Code Review\n{llm_content}"
    ai_bot_note = gitlab_client.edit_or_create_mr_discussion(
        AiBotNote(FeatureTypes.CODE_REVIEW, NoteTypes.MR_DISCUSSION, content))

    if configs.CR_DEBUG: print(f"Note: {ai_bot_note.metadata}")


def sast_explain(llm_client, gitlab_client):
    messages = SastExplain().all_messages()
    if not messages: return

    llm_resp = llm_client.chat_completions(messages)
    llm_content = llm_resp["choices"][0]["message"]["content"]
    content = f"# SAST Explain\n{llm_content}"
    ai_bot_note = gitlab_client.edit_or_create_mr_discussion(
        AiBotNote(FeatureTypes.SAST_EXPLAIN, NoteTypes.MR_DISCUSSION, content))

    if configs.CR_DEBUG: print(f"Note: {ai_bot_note.metadata}")


async def main():
    try:
        if configs.CR_LLM_MODEL.startswith("coderider/"):
            llm_client = CoderiderClient().login()
        else:
            llm_client = LitellmClient()

        gitlab_client = GitlabClient()

        ## Features
        # merge_request(llm_client, gitlab_client)
        # sast_explain(llm_client, gitlab_client)
        # SecretDetection(gitlab_client).send()
        event_loop = asyncio.get_event_loop()
        await asyncio.gather(
            event_loop.run_in_executor(None, merge_request, llm_client, gitlab_client),
            event_loop.run_in_executor(None, sast_explain, llm_client, gitlab_client),
            event_loop.run_in_executor(None, SecretDetection(gitlab_client).send),
        )

    except ConfigError as e:
        if configs.CR_DEBUG: print(e)
        exit(1)


def crcr():
    start_at = time.time()
    asyncio.run(main())
    delta = time.time() - start_at
    if configs.CR_DEBUG:
        print(f"Time consuming: {delta:.3f} s")


if __name__ == '__main__':
    crcr()
