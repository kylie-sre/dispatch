#!/usr/bin/env python
import os.path

from setuptools import find_packages, setup


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


def get_requirements(env):
    with open("requirements-{}.txt".format(env)) as fp:
        return [x.strip() for x in fp.read().split("\n") if not x.startswith("#")]


install_requires = get_requirements("base")
dev_requires = get_requirements("dev")
VERSION = "0.1.0.dev0"
# Get the long description from the README file
with open(os.path.join(ROOT_PATH, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dispatch",
    version=VERSION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Netflix, Inc.",
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require={"dev": dev_requires},
    zip_safe=False,
    include_package_data=True,
    entry_points={
        "console_scripts": ["dispatch = dispatch.cli:entrypoint"],
        "dispatch.plugins": [
            "dispatch_document_resolver = dispatch.plugins.dispatch_core.plugin:DispatchDocumentResolverPlugin",
            "dispatch_participant_resolver = dispatch.plugins.dispatch_core.plugin:DispatchParticipantResolverPlugin",
            "dispatch_pkce_auth = dispatch.plugins.dispatch_core.plugin:PKCEAuthProviderPlugin",
            "dispatch_ticket = dispatch.plugins.dispatch_core.plugin:DispatchTicketPlugin",
            "dispatch_basic_auth = dispatch.plugins.dispatch_core.plugin:BasicAuthProviderPlugin",
            "dispatch_contact = dispatch.plugins.dispatch_core.plugin:DispatchContactPlugin",
            "google_calendar_conference = dispatch.plugins.dispatch_google.calendar.plugin:GoogleCalendarConferencePlugin",
            "google_docs_document = dispatch.plugins.dispatch_google.docs.plugin:GoogleDocsDocumentPlugin",
            "google_drive_storage = dispatch.plugins.dispatch_google.drive.plugin:GoogleDriveStoragePlugin",
            "google_drive_task = dispatch.plugins.dispatch_google.drive.plugin:GoogleDriveTaskPlugin",
            "google_gmail_conversation = dispatch.plugins.dispatch_google.gmail.plugin:GoogleGmailConversationPlugin",
            "google_groups_participants = dispatch.plugins.dispatch_google.groups.plugin:GoogleGroupParticipantGroupPlugin",
            "jira_ticket = dispatch.plugins.dispatch_jira.plugin:JiraTicketPlugin",
            "pagerduty_oncall = dispatch.plugins.dispatch_pagerduty.plugin:PagerDutyOncallPlugin",
            "slack_contact = dispatch.plugins.dispatch_slack.plugin:SlackContactPlugin",
            "slack_conversation = dispatch.plugins.dispatch_slack.plugin:SlackConversationPlugin",
            "zoom_conference = dispatch.plugins.dispatch_zoom.plugin:ZoomConferencePlugin",
            "opsgenie_oncall = dispatch.plugins.dispatch_opsgenie.plugin:OpsGenieOncallPlugin",
        ],
    },
)
