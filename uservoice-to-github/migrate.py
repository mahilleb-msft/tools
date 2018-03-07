# UserVoice to GitHub Migration Tool

import uservoice
from github import Github
from purifier import ProfanitiesFilter

# UserVoice account ID. This is part of the URL, e.g. for msdocs.uservoice.com, this would be msdocs.
USERVOICE_ACCOUNT_ID = ''
USERVOICE_API_KEY = ''
USERVOICE_API_SECRET = ''
USERVOICE_SSO_KEY = ''
USERVOICE_CALLBACK_URL = 'http://docs.microsoft.com/'

GITHUB_TARGET_REPO = 'MicrosoftDocs/feedback'
GITHUB_PERSONAL_ACCESS_TOKEN = ''

f = ProfanitiesFilter([''], replacements="*") 
f.inside_words = True

# GitHub Client
g = Github(GITHUB_PERSONAL_ACCESS_TOKEN)

# UserVoice Client
client = uservoice.Client(USERVOICE_ACCOUNT_ID, USERVOICE_API_KEY, USERVOICE_API_SECRET, callback=USERVOICE_CALLBACK_URL)

suggestions = client.get_collection("/api/v1/suggestions?sort=newest")

# Loads the first page (at most 100 records) of suggestions and reads the count.
print ("Total suggestions: " + str(len(suggestions)))

ideas_to_migrate = []

print ('Collecting suggestions...')

# Loop through suggestions and figure out which ones need to be migrated.
for suggestion in suggestions:
    if suggestion['status']:
        status_type = suggestion['status']['name']
        if status_type.lower() != 'completed' and status_type.lower() != 'declined':
            ideas_to_migrate.append(suggestion)
    else:
        ideas_to_migrate.append(suggestion)


migration_count = str(len(ideas_to_migrate))
print ("Number of suggestions to migrate: " + migration_count)

target_repo = g.get_repo(GITHUB_TARGET_REPO)

# FYI: Mapping on labels
# started = in-progress
# under review = triaged
# planned = triaged

counter = 0
print ('Kicking off migration to GitHub...')
for idea in ideas_to_migrate:
    counter += 1
    print ('Migrating idea ' + str(counter) + ' of ' + migration_count + "...")

    idea_text = '_No details provided._'

    if idea['text']:
        idea_text = f.clean(idea['text'])

    # String that defines the attribution block of the issue.
    attribution_string = '\n\n----------\n⚠ Idea migrated from UserVoice\n\n' + '**Created By:** ' + idea['creator']['name'] + '\n**Created On:** ' + idea['created_at'] + '\n**Votes at Migration:** ' + str(idea['vote_count']) + '\n**Supporters at Migration:** ' + str(idea['supporters_count'])

    # Define labels
    labels = []
    if idea['status']:
        status_type = idea['status']['name']
        if status_type.lower() == 'under review' or status_type.lower() == 'planned':
            labels.append('triaged')
        elif status_type.lower() == 'started':
            labels.append('in-progress')


    target_repo.create_issue(f.clean(idea['title']), idea_text + attribution_string, labels=labels)

print ('Migration complete!')
