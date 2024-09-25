from typing import Optional

import gitlab
from gitlab.v4 import objects as gl

from coderider_codereview import configs
from coderider_codereview.ai_bot_note import AiBotNote
from coderider_codereview.feature_types import FeatureTypes
from coderider_codereview.note_types import NoteTypes


class GitlabClient:
    def __init__(self):
        self._ai_bot_user = None
        self._mr = None
        self._project = None
        self._latest_version = None
        self._code_diffs = None
        self._discussions = None
        self._ai_bot_mr_discussions = None

        self._project_path = configs.CR_MR_PROJECT_PATH
        self._mr_iid = configs.CR_MR_IID
        self._gitlab_host = configs.CR_GITLAB_HOST
        self._bot_token = configs.CR_AI_BOT_TOKEN

        # Cache commits with commit sha
        self._commits_cache = {}

        self._client = gitlab.Gitlab(url=self._gitlab_host, private_token=self._bot_token, per_page=100)
        if configs.CR_DEBUG:
            self._client.enable_debug()

    @property
    def ai_bot_user(self) -> gl.CurrentUser:
        if not self._ai_bot_user:
            self._client.auth()
            self._ai_bot_user = self._client.user

        return self._ai_bot_user

    @property
    def project(self) -> gl.Project:
        if not self._project:
            self._project = self._client.projects.get(self._project_path)

        return self._project

    @property
    def mr(self) -> gl.ProjectMergeRequest:
        if not self._mr:
            self._mr = self.project.mergerequests.get(self._mr_iid)

        return self._mr

    @property
    def latest_version(self) -> gl.ProjectMergeRequestDiff:
        if not self._latest_version:
            versions = self.mr.diffs.list(order_by='id', sort='desc', page=1, per_page=1)
            self._latest_version = versions[0]

        return self._latest_version

    @property
    def mr_code_diffs(self) -> list:
        if not self._code_diffs:
            # There is an `unidiff` bug: mr.diffs.get
            # https://docs.gitlab.com/ee/api/merge_requests.html#list-merge-request-diffs
            path = f"/projects/{self.project.id}/merge_requests/{self._mr_iid}/diffs"
            self._code_diffs = self._client.http_list(path, unidiff=True, all=True)

        return self._code_diffs

    def create_mr_note(self, content) -> gl.ProjectMergeRequestNote:
        resp = self.mr.notes.create({'body': content})
        return resp

    def create_mr_discussion(self, content) -> gl.ProjectMergeRequestDiscussion:
        resp = self.mr.discussions.create({'body': str(content)})
        return resp

    @property
    def mr_discussions(self) -> list[gl.ProjectMergeRequestDiscussion]:
        if not self._discussions:
            self._discussions = self.mr.discussions.list(all=True)

        return self._discussions

    def _parse_ai_bot_discussion(self, discussion) -> Optional[AiBotNote]:
        try:
            notes = discussion.attributes["notes"]
            if not notes: return None

            note = notes[0]
            author = note["author"]
            content = note["body"]

            if author["id"] != self.ai_bot_user.id:
                return None

            ai_bot_note = AiBotNote.build(content)
            if not ai_bot_note: return None

            ai_bot_note.id = note["id"]
            ai_bot_note.discussion_id = discussion.id
            return ai_bot_note

        except KeyError as e:
            if configs.CR_DEBUG: print(e)
            return None

    @property
    def ai_bot_mr_discussions(self) -> dict[str, AiBotNote]:
        if not self._ai_bot_mr_discussions:
            self._ai_bot_mr_discussions = \
                {
                    ai_bot_note.unique_key: ai_bot_note
                    for discussion in self.mr_discussions
                    if (ai_bot_note := self._parse_ai_bot_discussion(discussion)) is not None
                }

        return self._ai_bot_mr_discussions

    def edit_or_create_mr_discussion(self, ai_bot_note: AiBotNote) -> AiBotNote:
        existing_note = self.ai_bot_mr_discussions.get(ai_bot_note.unique_key)

        if existing_note:
            existing_note.content = ai_bot_note.content
            _updated_note = self.mr.notes.update(existing_note.id, {'body': str(existing_note)})
            if configs.CR_DEBUG: print(f"Edit the note: {existing_note.id}")
            return existing_note

        # create
        new_discussion = self.create_mr_discussion(ai_bot_note)
        ai_bot_note.discussion_id = new_discussion.id
        ai_bot_note.id = new_discussion.attributes["notes"][0]["id"]
        if configs.CR_DEBUG: print(f"Create new discussion: {new_discussion.id}")
        return ai_bot_note

    def commit(self, commit_sha: str) -> gl.ProjectCommit:
        commit = self._commits_cache.get(commit_sha)

        if not commit:
            commit = self.project.commits.get(commit_sha)
            self._commits_cache[commit_sha] = commit

        return commit

    def ai_bot_commit_discussions(self, commit: gl.ProjectCommit, feature_type: FeatureTypes) -> dict[str, AiBotNote]:
        all_discussions = commit.discussions.list(all=True)

        discussion = {
            ai_bot_note.unique_key: ai_bot_note
            for discussion in all_discussions
            if ((ai_bot_note := self._parse_ai_bot_discussion(discussion)) is not None) and
               (ai_bot_note.feature_type == feature_type) and
               (ai_bot_note.note_type == NoteTypes.COMMIT_DISCUSSION)
        }

        return discussion

    def update_commit_comment(self, commit_sha: str, discussion_id: int | str, note_id: int | str, content: str):
        # https://docs.gitlab.com/ee/api/discussions.html#modify-an-existing-commit-thread-note
        path = f"/projects/{self.project.id}/repository/commits/{commit_sha}/discussions/{discussion_id}/notes/{note_id}"
        updated_note = self._code_diffs = self._client.http_put(path, body=content)

        return updated_note

    def edit_or_create_commit_discussion(self, ai_bot_note: AiBotNote) -> AiBotNote:
        commit = self.commit(ai_bot_note.commit_sha)
        commit_discussions = self.ai_bot_commit_discussions(commit, ai_bot_note.feature_type)
        existing_note = commit_discussions.get(ai_bot_note.unique_key)

        if existing_note:
            existing_note.content = ai_bot_note.content
            _updated_note = self.update_commit_comment(
                commit.id, existing_note.discussion_id, existing_note.id, str(existing_note))
            if configs.CR_DEBUG: print(f"Edit the commit note: {existing_note.id}")
            return existing_note

        # create
        _new_comment = commit.comments.create({
            'note': str(ai_bot_note),
            'line': ai_bot_note.position["line"],
            'line_type': ai_bot_note.position["line_type"],
            'path': ai_bot_note.position["path"],
        })  # -> gl.ProjectCommitComment

        refreshed_commit_discussions = self.ai_bot_commit_discussions(commit, ai_bot_note.feature_type)
        last_ai_bot_note = refreshed_commit_discussions[ai_bot_note.unique_key]
        if configs.CR_DEBUG: print(f"Create new commit note: {last_ai_bot_note.id}")
        return last_ai_bot_note


if __name__ == '__main__':
    c = GitlabClient()
    _u = c.ai_bot_user
    _p = c.project
    _mr = c.mr
    _v = c.latest_version
    # _new_note = c.create_mr_note("hi")
    # _new_discussion = c.create_mr_discussion("Hi")
    _mr_discussions = c.mr_discussions
    _parsed_ai_bot_discussion = c._parse_ai_bot_discussion(_mr_discussions[-1])
    _ai_bot_discussions = c.ai_bot_mr_discussions

    _diffs = c.mr_code_diffs

    # _code_review_note = c.edit_or_create_mr_discussion(
    #     AiBotNote(FeatureTypes.CODE_REVIEW, NoteTypes.MR_DISCUSSION, "HI+2"))
    # _sast_note = c.edit_or_create_mr_discussion(
    #     AiBotNote(FeatureTypes.SAST_EXPLAIN, NoteTypes.MR_DISCUSSION, "HELLO+2"))

    _sha = "c848b6e3317484b19d6f69e548b8d2fb9aabed28"
    _c = c.commit(_sha)
    _c_from_cache = c.commit(_sha)

    _secret_detection_note = (
        AiBotNote(FeatureTypes.SECRET_DETECTION,
                  NoteTypes.COMMIT_DISCUSSION,
                  "inline+6",
                  commit_sha=_sha,
                  position={
                      "line": 127,
                      "line_type": "new",
                      "path": "coderider_codereview/gitlab_client.py",
                  }))
    _created_updated_note = c.edit_or_create_commit_discussion(_secret_detection_note)
    _commit_secret_detection_discussions = c.ai_bot_commit_discussions(_c, FeatureTypes.SECRET_DETECTION)
    _last_note = _commit_secret_detection_discussions[_secret_detection_note.unique_key]
    print("end")
