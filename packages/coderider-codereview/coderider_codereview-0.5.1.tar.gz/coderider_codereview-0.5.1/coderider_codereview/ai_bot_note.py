import base64
import binascii
import json
import re
import time
from typing import Optional

import coderider_codereview
from coderider_codereview import configs
from coderider_codereview.feature_types import FeatureTypes
from coderider_codereview.note_types import NoteTypes
from coderider_codereview.utils import calc_digest


class AiBotNote:

    def __init__(self,
                 feature_type: str | FeatureTypes,
                 note_type: str | NoteTypes,
                 content: str,

                 model: str = None,
                 version: str = None,
                 content_digest: str = None,
                 created_at: int = None,
                 updated_at: int = None,

                 commit_sha: str = None,
                 position: dict = None,
                 ):

        self.id = None
        self.discussion_id = None
        self._feature_type = feature_type if isinstance(feature_type, FeatureTypes) else FeatureTypes(feature_type)
        self._note_type = note_type if isinstance(note_type, NoteTypes) else NoteTypes(note_type)
        self._content = content

        self._model = model or configs.CR_LLM_MODEL
        self._version = version or coderider_codereview.__version__
        self._content_digest = content_digest or calc_digest(content)
        self._created_at = created_at or time.time()
        self._updated_at = updated_at or time.time()
        self._commit_sha = commit_sha
        self._position = position

    @property
    def feature_type(self) -> FeatureTypes:
        return self._feature_type

    @property
    def note_type(self) -> NoteTypes:
        return self._note_type

    @property
    def commit_sha(self) -> str:
        return self._commit_sha

    @property
    def position(self) -> None | dict:
        return self._position

    @property
    def is_pure(self) -> bool:
        return self._content_digest == calc_digest(self._content)

    @property
    def is_persistent(self) -> bool:
        return self.id is not None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, new_content: str):
        self._model = configs.CR_LLM_MODEL
        self._version = coderider_codereview.__version__
        self._content = new_content
        self._content_digest = calc_digest(new_content)
        self._updated_at = time.time()

    @property
    def metadata(self) -> dict:
        return {
            "feature_type": self._feature_type.value,
            "note_type": self._note_type.value,
            "model": self._model,
            "version": self._version,
            "content_digest": self._content_digest,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
            "commit_sha": self._commit_sha,
            "position": self._position,
        }

    @property
    def header(self) -> str:
        metadata_str = json.dumps(self.metadata, sort_keys=True)
        encoded_data = base64.b64encode(metadata_str.encode()).decode()
        header = f"<!-- CR: {encoded_data} -->"

        if configs.CR_DEBUG:
            header += f"\n<!-- CR-DEBUG: {metadata_str} -->"

        return header

    def __str__(self):
        text = f"{self.header}\n{self._content}"

        return text

    @property
    def unique_key(self) -> str:
        if self.note_type == NoteTypes.MR_DISCUSSION:
            return self.feature_type.value
        elif self.note_type == NoteTypes.COMMIT_DISCUSSION:
            return f"{self.feature_type.value}:{calc_digest(self.position)}"

    @staticmethod
    def build(note_text: str) -> Optional['AiBotNote']:
        if not isinstance(note_text, str): return None

        try:
            first_line, _, content_partition = note_text.partition("\n")
            match = re.match(r'^<!-- CR: (.+) -->$', first_line)
            if not match: return None

            metadata = json.loads(base64.b64decode(match[1]).decode())
            instance = AiBotNote(content=content_partition, **metadata)

            return instance
        except (TypeError, binascii.Error, json.decoder.JSONDecodeError) as _e:
            return None


if __name__ == '__main__':
    new_note = AiBotNote(feature_type=FeatureTypes.CODE_REVIEW,
                         note_type=NoteTypes.MR_DISCUSSION,
                         content="OK",
                         model="maas")
    note_str = str(new_note)
    print("---")

    invalid_metadata = AiBotNote.build("""<!-- CR: eyJjb250ZW50X2RpZ2VzdCI6ICJlOTM3NmEyODFhYWM1N2JiNzhlMmM3Njk1ODRlNWVkYTliYjkzNjk5ZDI5OWMzYTQyYWRjNDZiN2I4ZTFjY2Q2IiwgImZlYXR1cmUiOiAiY29kZV9yZXZpZXciLCAibW9kZWwiOiAiZGVlcHNlZWsvZGVlcHNlZWstY2hhdCIsICJ2ZXJzaW9uIjogIjAuMy4wIiwgImNyZWF0ZWRfYXQiOiAxNzI2ODc2MTQ2Ljg5Mzk5NSwgInVwZGF0ZWRfYXQiOiAxNzI2ODg5Mjg4LjcyNjk4Nn0= -->
Morning""")
    valid_note = AiBotNote.build("""<!-- CR: eyJjb250ZW50X2RpZ2VzdCI6ICI1NjUzMzliYzRkMzNkNzI4MTdiNTgzMDI0MTEyZWI3ZjVjZGYzZTVlZWYwMjUyZDZlYzFiOWM5YTk0ZTEyYmIzIiwgImNyZWF0ZWRfYXQiOiAxNzI3MDc5MjE5LjQxNDQzNywgImZlYXR1cmVfdHlwZSI6ICJjb2RlX3JldmlldyIsICJtb2RlbCI6ICJtYWFzIiwgIm5vdGVfdHlwZSI6ICJtcl9kaXNjdXNzaW9uIiwgInBvc2l0aW9uIjogbnVsbCwgInVwZGF0ZWRfYXQiOiAxNzI3MDc5MjE5LjQxNDQzNzgsICJ2ZXJzaW9uIjogIjAuMy4wIn0= -->
<!-- CR-DEBUG: {"content_digest": "565339bc4d33d72817b583024112eb7f5cdf3e5eef0252d6ec1b9c9a94e12bb3", "created_at": 1727079219.414437, "feature_type": "code_review", "model": "maas", "note_type": "mr_discussion", "position": null, "updated_at": 1727079219.4144378, "version": "0.3.0"} -->
OK""")
    print("---")
