import subprocess
import glob
import os
import shutil

author = "中华人民共和国全国人民代表大会 <>"
repo = "chinese-constitution"

# Initialize git repository
if not os.path.exists(repo):
    os.makedirs(repo)
subprocess.call(["git", "init", "-q"], cwd=repo)
subprocess.call(["git", "checkout",
                 "-b", "master", "-q"],
                cwd=repo)

# Add README
f = "misc/README.md"
shutil.copy(f, os.path.join(repo, "README.md"))
subprocess.call(["git", "add", "README.md"], cwd=repo)
subprocess.call(["git", "commit",
                 "-m 添加 README",
                 "-q", "--no-status"], cwd=repo)

for f in sorted(glob.glob("texts/*.md")):

    # Metadata
    data = os.path.splitext(os.path.basename(f))[0]
    data = data.split("-")

    # Date extraction
    # Git limitation, see
    # https://stackoverflow.com/questions/21787872/is-it-possible-to-set-a-git-commit-to-have-a-timestamp-prior-to-1970
    if int(data[0]) < 1970:
        date = "1970-01-01 00:00:00+0000"
    else:
        date = "-".join(data[:3]) + " 00:00:00+0000"

    # Message
    message = data[0] + "年" + data[1] + "月" + data[2] + "日" + data[3]

    subprocess.call(["git", "checkout", "master", "-q"], cwd=repo)

    # Amendments of 1975 and 1978 are considered as two separate branches
    if "1975" in date:
        subprocess.call(["git", "checkout",
                         "-b", "1975宪法", "-q"],
                        cwd=repo)
    elif "1978" in date:
        subprocess.call(["git", "checkout",
                         "-b", "1978宪法", "-q"],
                        cwd=repo)

    # Copy to the repository
    shutil.copy(f, os.path.join(repo, "Constitution.md"))

    # Commit
    subprocess.call(["git", "add", "Constitution.md"], cwd=repo)
    subprocess.call(["git", "commit", "--author=%s" % author,
                     "--date=%s" % date, "-m %s" % message,
                     "-q", "--no-status"], cwd=repo)

    # Tagging
    if "1970" in date:
        subprocess.call(["git", "tag", "1954宪法"], cwd=repo)
    elif "1975" in date:
        subprocess.call(["git", "tag", "1975宪法"], cwd=repo)
    elif "1978" in date:
        subprocess.call(["git", "tag", "1978宪法"], cwd=repo)
    elif "1982" in date:
        subprocess.call(["git", "tag", "1982宪法"], cwd=repo)
    elif "2018" in date:
        subprocess.call(["git", "tag", "现行宪法"], cwd=repo)
