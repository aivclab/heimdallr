# https://github.com/pulls?q=is%3Aopen+is%3Apr+user%3Aaivclab+archived%3Afalse+
# https://github.com/pulls?user=aivclab
from datetime import datetime, timedelta
from enum import Enum
from typing import Generator, Iterable, List, Union

from github import Github  # pip install PyGithub
from github.GithubObject import NotSet
from github.Issue import Issue
from github.Label import Label
from github.Milestone import Milestone
from github.NamedUser import NamedUser
from github.PullRequest import PullRequest
from github.Repository import Repository
from sorcery import assigned_names


# TODO: CONVERT TO PLUGINS for heimdallr!


class RepoTypeEnum(Enum):
    all, public, private, forks, sources, member = assigned_names()
    internal = "internal"  # TODO: maybe not be supported


class RepoSortEnum(Enum):
    created, updated, pushed, full_name = assigned_names()


class DirectionEnum(Enum):
    asc, desc = assigned_names()


class StateEnum(Enum):
    open, closed, all = assigned_names()


class PullRequestSortEnum(Enum):
    (created, updated, popularity) = assigned_names()  # (comment  count),

    long_running = (
        "long-running"  # (age, filtering by pulls  updated in the  last  month).
    )


class IssueSortEnum(Enum):
    created, updated, comments = assigned_names()


def yield_org_repos(
    g: Github,
    org_name: str,
    repo_type: Union[str, RepoTypeEnum] = RepoTypeEnum.all,
    sort: Union[str, RepoSortEnum] = RepoSortEnum.pushed,
    direction: Union[str, DirectionEnum] = DirectionEnum.desc,
) -> Generator[Repository, None, None]:
    """

    Read more: https://docs.github.com/en/rest/reference/repos#list-organization-repositories--parameters

    Args:
      g:
      org_name:
      repo_type:
      sort:
      direction:

    Returns:

    """
    repo_type = RepoTypeEnum(repo_type)
    sort = RepoSortEnum(sort)
    direction = DirectionEnum(direction)
    yield from g.get_organization(org_name).get_repos(
        type=repo_type.value, sort=sort.value, direction=direction.value
    )


def yield_org_issues(g: Github, org_name: str) -> Generator[Issue, None, None]:
    """

    :param g:
    :param org_name:
    """
    yield from yield_issues(yield_org_repos(g, org_name))


def yield_org_prs(g: Github, org_name: str) -> Generator[PullRequest, None, None]:
    """

    :param g:
    :param org_name:
    """
    yield from yield_prs(yield_org_repos(g, org_name))


def yield_issues(
    iterable: Iterable[Repository],
    milestone: Union[Milestone, str] = NotSet,
    state: Union[str, StateEnum] = StateEnum.open,
    assignee: Union[NamedUser, str] = NotSet,
    mentioned: NamedUser = NotSet,
    labels: Union[List[str], List[Label]] = NotSet,
    sort: Union[str, IssueSortEnum] = IssueSortEnum.updated,
    direction: Union[str, DirectionEnum] = DirectionEnum.desc,
    since: datetime = NotSet,  # datetime.now(),
    creator: Union[str, NamedUser] = NotSet,
) -> Generator[Issue, None, None]:
    """

    Read more: https://docs.github.com/en/rest/reference/issues#list-issues-assigned-to-the-authenticated-user--parameters

    Args:
      iterable:
      milestone:
      state:
      assignee:
      mentioned:
      labels:
      sort:
      direction:
      since:
      creator:

    Returns:

    """
    state = StateEnum(state)
    sort = IssueSortEnum(sort)
    direction = DirectionEnum(direction)
    for repo in iterable:
        yield from repo.get_issues(
            milestone=milestone,
            state=state.value,
            assignee=assignee,
            mentioned=mentioned,
            labels=labels,
            sort=sort.value,
            direction=direction.value,
            since=since,
            creator=creator,
        )


def yield_prs(
    iterable: Iterable[Repository],
    state: Union[str, StateEnum] = StateEnum.open,
    sort: Union[str, PullRequestSortEnum] = PullRequestSortEnum.updated,
    direction: Union[str, DirectionEnum] = DirectionEnum.desc,
    base: str = NotSet,
    head: str = NotSet,
) -> Generator[PullRequest, None, None]:
    """

    Read more: https://docs.github.com/en/rest/reference/pulls#list-pull-requests--parameters

    Args:
      iterable:
      state:
      sort:
      direction:
      base:
      head:

    Returns:

    """
    state = StateEnum(state)
    sort = PullRequestSortEnum(sort)
    direction = DirectionEnum(direction)
    for repo in iterable:
        yield from repo.get_pulls(
            state=state.value,
            sort=sort.value,
            direction=direction.value,
            base=base,
            head=head,
        )


#
def get_pull_request(g, org_name, repo_name, pull_request_number):
    """

    :param g:
    :param org_name:
    :param repo_name:
    :param pull_request_number:
    :return:
    """
    return (
        g.get_organization(org_name).get_repo(repo_name).get_pull(pull_request_number)
    )


import calendar


def utc_to_epoch(timestamp):  # Timestamp is a datetime object in UTC time
    """

    :param timestamp:
    :return:
    """
    return calendar.timegm(timestamp.utctimetuple())


if __name__ == "__main__":
    from heimdallr.configuration.heimdallr_settings import HeimdallrSettings

    gthb = Github(HeimdallrSettings().github_token)
    remaining = gthb.rate_limiting[0]
    reset_seconds = gthb.rate_limiting_resettime - utc_to_epoch(datetime.utcnow())
    interval_seconds = ((reset_seconds + 1) / (remaining + 1)) + 1
    print(f"intervals recommended {interval_seconds} seconds")
    if remaining > 0 and False:
        # g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token") # Github Enterprise with custom hostname
        # print(list(yield_org_repos(gthb, 'aivclab')))
        print(list(yield_org_issues(gthb, "aivclab"))[0].repository.name)
    else:
        print("rate limited")

        print(f"reset in {timedelta(seconds=reset_seconds)} ")
    # print(list(yield_org_prs(gthb, 'aivclab')))
