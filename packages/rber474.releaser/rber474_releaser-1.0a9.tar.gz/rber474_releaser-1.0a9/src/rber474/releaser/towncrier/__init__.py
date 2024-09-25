from rber474.releaser.utils import get_default_location
from rber474.releaser.utils import get_towncrier_directory
from rber474.releaser.utils import get_towncrier_types
from rber474.releaser.utils import Style
from zest.releaser.utils import read_text_file
from zest.releaser.utils import write_text_file

import json
import re
import zest.releaser.choose
import zest.releaser.git
import zest.releaser.utils


try:
    from zest.releaser.utils import system as execute_command
except ImportError:
    from zest.releaser.utils import execute_command


def create_newsfile(context):
    """Check last tag diff commits and create the newsfiles based in jira issues."""
    print(f"{Style.RED}rber474.releaser.towncrier{Style.RESET}")
    news_directory = get_towncrier_directory()
    vcs = zest.releaser.choose.version_control()
    issues = extract_issues(vcs)

    if not issues:
        print(f"{Style.RED}No issues found.{Style.RESET}")
        print(
            f"{Style.RED}Commit message must be formatted <TASK-ID> <issue type> <message>.{Style.RESET}"
        )
        return

    if zest.releaser.utils.ask(
        "Do you want to create the news fragments for these issues?", True
    ):

        for issue in issues:
            prefix = issue.get("prefix", "")
            fixed_prefix, n = re.subn("[-/ ]", "", prefix)
            if fixed_prefix:
                fixed_prefix = f"{fixed_prefix} "
            issue_type = issue.get("type")
            issue_number = issue.get("issue")
            issue_message = issue.get("message")
            issue_author = issue.get("author")

            print(
                f"{Style.GREEN}Creating or Editing newsfile for {issue_number} {issue_type} {fixed_prefix} {issue_message} {issue_author}{Style.RESET}"
            )

            # Get the newsfile path
            newsfile_path = (
                f"{news_directory}/{issue_number.upper()}.{issue_type.lower()}"
            )

            try:
                # Get the newsfile content
                newsfile_content, newsfile_encoding = read_text_file(newsfile_path)
                # Add the issue message to the newsfile content
                contents = "\n".join(newsfile_content)
                newsfile_content = (
                    f"{contents}{fixed_prefix}{issue_message} {issue_author}\n"
                )
            except FileNotFoundError:
                # Add the issue message to the newsfile content
                newsfile_content = f"{fixed_prefix}{issue_message} {issue_author}\n"
            except BaseException:
                raise

            # Write the newsfile content
            write_text_file(newsfile_path, newsfile_content)

        if issues:
            msg = "Update towncrier fragments"
            # Ensure the newsfile is added to the git index
            # to avoid pre-commit hooks to fail
            execute_command(["git", "add", "."])
            commit_cmd = vcs.cmd_commit(msg)
            commit = execute_command(commit_cmd)
            print(commit)
    print("End custom releaser.")


def extract_issues(vcs):
    """Extract the issues from the commit messages."""

    pretty_data = get_history(vcs)

    # Reverse the list to get the commits in the correct order
    pretty_data = reversed(pretty_data)

    types = get_towncrier_types()

    # Pattern matchs the commit message with the following format:
    # <optional prefix> <issue> <type> <message> [<author>]
    # Examples:
    # WEBAGL-21101 bugfix AttributeError RequestContainer object has no attribute getClientForURL [rbermudez]
    # WEBAgL-21101 feature AttributeError: 'RequestContainer' object has no attribute 'getClientForURL [rbermudez]
    # test WEBAgL-21101 bugfix AttributeError: 'RequestContainer' object has no attribute 'getClientForURL [rbermudez]
    pattern = r"{}".format(
        rf'(?i)(?P<prefix>.*?|)(?P<issue>\w*\S-\d+) (?P<type>({"|".join(types)})) (?P<message>.*) (?P<author>\[.*?\])'
    )

    # Extract the commit messages that include the issue number, issue type and
    # message.
    matching = [
        re.search(pattern, commit).groupdict()
        for commit in pretty_data
        if re.search(pattern, commit)
    ]

    if matching:
        print(
            f"{Style.GREEN}These are all the commits since the last tag:{Style.RESET}"
        )
        print("")
        print(json.dumps(matching, indent=4))
        print(f"{Style.RED}Found issues: {Style.RESET}{len(matching)}{Style.RESET}")
    return matching


def get_history(vcs):
    """Get the history from the last tag to the current commit."""

    pretty_data = []
    default_location = get_default_location()
    history_file = vcs.history_file(location=default_location)
    if history_file:

        try:
            found = zest.releaser.utils.get_last_tag(vcs, allow_missing=True)
            if found:
                log_command = vcs.cmd_log_since_tag(found)
            else:
                log_command = None
        except SystemExit:
            log_command = get_all_commits_command(vcs)

    if log_command:
        data = execute_command(log_command)
        pretty_data = prettyfy_logs(data, vcs)

    return pretty_data


def get_all_commits_command(vcs):
    """Get command to get all commits. Git is the only one implemented."""
    if isinstance(vcs, zest.releaser.git.Git):
        return ["git", "log"]


def prettyfy_logs(data, vcs):
    """Return a prettyfied log data."""
    new_data = []
    if isinstance(vcs, zest.releaser.git.Git):
        # Q: How to prettyfy git logs?
        # A: Take just the lines that start with whitespaces
        author = ""
        for line in data.split("\n"):
            if line and line.startswith("Author: "):
                author = line.replace("Author: ", "")
            if line and line.startswith(" "):
                if not line.strip().lower().startswith("back to development"):
                    if author:
                        new_data.append(f"- {line.strip()} [{author}]")
                    else:
                        new_data.append(f"- {line.strip()}")
                    new_data.append("")
    else:
        # Not implemented yet
        new_data = data.split("\n")

    return new_data
