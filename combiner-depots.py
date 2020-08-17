import glob
import git
import time
import os
import tqdm
import sys

FILES = sys.argv[1]

# list all commits
commits = []

print('Chargement des commits...')
files = list(glob.glob(FILES + '/*/**/'))
for repo_dir in tqdm.tqdm(files, total=len(files)):
	try:
		repo = git.Repo(repo_dir)
		found_a_good_branch = False
		for branch in ('texte-futur', 'texte', 'texte-abrogé'):
			try:
				for commit in repo.iter_commits(branch):
					found_a_good_branch = True
					commits.append({
						'repo': repo_dir,
						'commit': str(commit),
						'date': commit.committed_date,
						'branch': branch
					})
				break
			except KeyboardInterrupt:
				raise
			except:
				pass
		if not found_a_good_branch:
			raise Exception('no good branch')
	except KeyboardInterrupt:
		raise
	except Exception as e:
		print(e)
		print('invalid repo', repo_dir)

# sort them by date
commits.sort(key=lambda commit: commit['date'])

# create the new repository
os.system('rm -rf combined/')
repo = git.Repo.init('combined')

# execute them one by one by order
print('Re-execution des commits...')
for commit in tqdm.tqdm(commits, total=len(commits)):
	commit_obj = git.Repo(commit['repo']).commit(commit['commit'])

	try:
		filename = [b.name for b in commit_obj.tree.blobs][0]
	except:
		print('no file found in', commit['repo'], 'at', commit['commit'], 'trying parent')
		commit_obj = git.Repo(commit['repo']).commit(commit['commit']+'^')
		filename = [b.name for b in commit_obj.tree.blobs][0]

	filecontents = (commit_obj.tree / filename).data_stream.read().decode('utf-8')
	open('combined/' + filename, 'w').write(filecontents)

	repo.git.add('--all')
	t = time.strftime("%d %b %Y", time.gmtime(commit['date']))
	repo.index.commit(f"{filename}: {t}")