from git import Repo
import os

upstream_url = "https://github.com/november-pain/git-fork-sync-test.git"
main_branch = "master"

repo = Repo(os.getcwd())

repo.config_writer().set_value("user", "name", "devops").release()
repo.config_writer().set_value("user", "email", "devops@inc4.net").release()

upstream = repo.create_remote("upstream", upstream_url)

upstream.fetch()

remote_origin_refs = repo.remote("origin").refs
remote_upstream_refs = repo.remote("upstream").refs

origin_branches = [branch.name.split('/')[1] for branch in remote_origin_refs]
upstream_branches = [branch.name.split('/')[1] for branch in remote_upstream_refs]

common_branches = [branch for branch in upstream_branches if branch in origin_branches]
new_branches = [branch for branch in upstream_branches if branch not in origin_branches]

print("Upstream branches: " + upstream_branches)
print("Origin branches: " + origin_branches)
print("New branches: " + new_branches)
print("Common branches: " + common_branches)

def merge_existing_branch(git, branch, main_branch):
    git.checkout(branch)
    git.merge("--no-edit", "upstream/" + branch)
    git.push()
    git.checkout(main_branch)

def merge_non_existing_branch(git, branch, main_branch):
    git.checkout(main_branch)
    git.checkout('-b', branch)
    git.merge("--no-edit", "upstream/" + branch)
    git.push("--set-upstream", "origin", branch)
    git.checkout(main_branch)

git = repo.git

for branch in common_branches:
    merge_existing_branch(git, branch, main_branch)

for branch in new_branches:
    merge_non_existing_branch(git, branch, main_branch)
