import json

from coderider_codereview import configs
from coderider_codereview.ai_bot_note import AiBotNote
from coderider_codereview.feature_types import FeatureTypes
from coderider_codereview.gitlab_client import GitlabClient
from coderider_codereview.note_types import NoteTypes


class SecretDetection:
    def __init__(self, gitlab_client):
        self._gitlab_client = gitlab_client
        self._report_file = configs.CR_ARTIFACT_SECRET_DETECTION_REPORT_FILE_PATH

    @property
    def report(self):
        try:
            with open(self._report_file, 'r') as file:
                report = json.load(file)
                return report
        except FileNotFoundError as _e:
            return {}

    def send(self) -> list:
        vulnerabilities = self.report.get("vulnerabilities", [])

        ai_bot_notes = []
        for vulnerability in vulnerabilities:
            try:
                if vulnerability["severity"] != "Critical": continue

                description = vulnerability["description"]
                commit_sha = vulnerability["location"]["commit"]["sha"]
                line = vulnerability["location"]["start_line"]
                path = vulnerability["location"]["file"]

                ai_bot_note = AiBotNote(FeatureTypes.SECRET_DETECTION,
                                        NoteTypes.COMMIT_DISCUSSION,
                                        description,
                                        commit_sha=commit_sha,
                                        position={
                                            "line": line,
                                            "line_type": "new",
                                            "path": path,
                                        })
                created_updated_note = self._gitlab_client.edit_or_create_commit_discussion(ai_bot_note)
                ai_bot_notes.append(created_updated_note)
            except Exception as _e:
                if configs.CR_DEBUG: print(_e)
                continue

        if configs.CR_DEBUG: print(f"Found {len(ai_bot_notes)} Critical Vulnerabilities.")
        return ai_bot_notes


if __name__ == '__main__':
    gitlab_client = GitlabClient()
    _sd = SecretDetection(gitlab_client)
    _r = _sd.report
    _notes = _sd.send()
    print("end")
