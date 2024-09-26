import os
from dataclasses import dataclass

from github import Github
from github.Issue import Issue
from github.PullRequest import PullRequest
from github.Repository import Repository

from bigeye_sdk.log import get_logger
from bigeye_sdk.generated.com.bigeye.models.generated import DeltaInfo
from bigeye_cli.model.vendor_report import (
    VendorReport,
    _format_report,
    _format_group_report,
)

log = get_logger(__file__)


@dataclass
class GitHubReport(VendorReport):
    github_token: str
    git: Github = None
    repo: Repository = None
    pr: PullRequest = None
    issue: Issue = None

    def __post_init__(self):
        self.git = Github(self.github_token)
        self.repo = self.git.get_repo(os.environ["CURRENT_REPO"])
        self.pr = self.repo.get_pull(int(os.environ["PR_NUMBER"]))

    def publish(
        self, base_url: str, source_table_name: str, target_table_name: str, di: DeltaInfo
    ) -> int:

        dti = di.comparison_target_infos[0]
        url = f"{base_url}/{di.delta.id}"
        if dti.alerting_metric_count != 0 or dti.failed_metric_count != 0:
            log.info(
                "Delta has alerting metrics. A grouped delta will run, if columns have been specified."
            )
            log.error("The process will exit as failed.")
            report = _format_report(url, source_table_name, target_table_name, dti)
            body = f"Bigeye Delta failure for PR: {self.pr.title}\n\n{report}"
            # self.issue = self.repo.create_issue(
            #     title=failure_title, body=report, assignee=self.pr.user, labels=["bug"]
            # )
            self.pr.create_issue_comment(body=body)
            return 1
        elif dti.schema_match is False:
            question_title = f"## Schema mismatch detected in delta. Is this expected?"
            header = "#### Please confirm that the schemas are not supposed to match before approving Pull Request."
            tables = (
                f"Source Table: {source_table_name}\nTarget Table: {target_table_name}"
            )
            body = f"{question_title}\n{header}\n{tables}"

            self.pr.create_issue_comment(body=body)
            return 0
        else:
            return 0

    def publish_group_bys(
        self, base_url: str, source_table_name: str, target_table_name: str, di: DeltaInfo
    ):
        dti = di.comparison_target_infos[0]
        group_bys = di.delta.comparison_table_configurations[0].group_bys
        url = f"{base_url}/{di.delta.id}"
        report = _format_group_report(url, source_table_name, target_table_name, dti, group_bys)
        self.pr.create_issue_comment(body=report)

    def publish_bigconfig_plan(self, plan: str):
        self.pr.create_issue_comment(body=plan)
