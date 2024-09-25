import json
import os

from coderider_codereview import configs


class SastExplain:
    def _system_message(self):
        content = """
You are a Security master.
After scanning with the SAST tool, a set of vulnerabilities reports are obtained in the following json format:

```json
{
    "name": "vulnerability name",
    "description": "vulnerability details",
    "cve": "CVE ID",
    "severity": "severity level",
    "scanner": {
        "id": "scanner id",
        "name": "scanner name"
    },
    "location": {
        "file": "file path",
        "start_line": "line number"
    }
}
```
"""

        return {
            "role": "system",
            "content": content
        }

    def _user_command_message(self):
        content = """
针对每份漏洞报告进行下面的分析:
1. 简要描述漏洞位置
2. 简要描述漏洞原因和后果
3. 如何修复漏洞
            """

        return {
            "role": "user",
            "content": content
        }

    def _report_messages(self, report):
        msgs_generator = lambda content: [
            {
                "role": "user",
                "content": content
            },
            {
                "role": "assistant",
                "content": "Got it"
            }
        ]

        # https://semgrep.dev/docs/writing-rules/rule-syntax#required
        messages = []
        for v in report["vulnerabilities"]:
            if v["severity"] == "Medium" or v["severity"] == "High":
                item = {
                    "name": v["name"],
                    "description": v["description"],
                    "cve": v["cve"],
                    "scanner": v["scanner"],
                    "location": v["location"],
                }
                msgs = msgs_generator(json.dumps(item))
                messages.extend(msgs)

        return messages

    def all_messages(self, report_file_path: str = None):
        if report_file_path is None:
            report_file_path = configs.CR_ARTIFACT_SAST_REPORT_FILE_PATH

        if not os.path.exists(report_file_path):
            return []

        with open(report_file_path, 'r') as file:
            report = json.load(file)
            report_messages = self._report_messages(report)
            if not report_messages:
                return []

        messages = [self._system_message()]
        messages.extend(report_messages)
        messages.append(self._user_command_message())

        return messages


if __name__ == '__main__':
    prompt = SastExplain()
    all_messages = prompt.all_messages("../gl-sast-report.json")
    print("end")
