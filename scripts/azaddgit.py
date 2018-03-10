# Update the Azure PowerShell content with Git URLs
# for cases where the Git URLs were skipped.
# -----
# Written By: Den Delimarsky (dend)
# Written On: March 9, 2018
# -----

import os, sys, codecs
import collections
import frontmatter  # pip install python-frontmatter (https://github.com/eyeseast/python-frontmatter)

PUB_READY_FOLDER = '/mnt/c/Users/dendeli/Downloads/azurermps-5.5.0/azurermps-5.5.0'
LOOKUP_FOLDER = '/mnt/c/projects/_output'

# Source for this function: https://stackoverflow.com/a/8898439
def cleanup_bom (path):
    print ('Checking and removing BOM in ' + path)

    BUFSIZE = 4096
    BOMLEN = len(codecs.BOM_UTF8)

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r+b") as fp:
                chunk = fp.read(BUFSIZE)
                if chunk.startswith(codecs.BOM_UTF8):
                    i = 0
                    chunk = chunk[BOMLEN:]
                    while chunk:
                        fp.seek(i)
                        fp.write(chunk)
                        i += len(chunk)
                        fp.seek(BOMLEN, os.SEEK_CUR)
                        chunk = fp.read(BUFSIZE)
                    fp.seek(-BOMLEN, os.SEEK_CUR)
                    fp.truncate()

# Yes, I am also looking at the code below going (trust me, I wrote it):
#
# ╱╱▏╱▏╱▏╱╱╱╱╱╱▏╱╱╱╱╱▏
# ▉╱▉╱▉╱▏▉▉▉▉▉╱┈▉▉▉▉╱
# ▉╱▉╱▉╱▏┈┈▉╱▏┈┈▉╱╱╱╱▏
# ▉╱▉╱▉╱▏┈┈▉╱▏┈┈▉▉▉▉╱
# ▉▉▉▉▉╱┈┈┈▉╱┈┈┈▉╱
#
# But, python-frontmatter apparently does not understand
# {{TEXT_HERE}}, which makes sense.
# https://symfony.com/doc/current/components/yaml/yaml_format.html
# So, I thought I would replace with @@ but that is 
# not OK either, so I just replaced the fragments with GUID chunks to save time
# and focus on the important parts of the work.
# Oh, and [Object object] also breaks the front matter parser.

def cleanup_unenc (path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r+") as fp:
                contents = fp.read()
                contents = contents.replace('{{', '448ae5be-6b').replace('}}','add50398-d0').replace('[object Object]:','edd50378-d9')
                fp.seek(0)
                fp.write(contents)
                fp.truncate()

def reverse_cleanup_unenc (path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r+") as fp:
                contents = fp.read()
                contents = contents.replace('448ae5be-6b', '{{').replace('add50398-d0','}}').replace('edd50378-d9','[object Object]:')
                fp.seek(0)
                fp.write(contents)
                fp.truncate()

# FYI: Check for BOM and remove it.
# This throws off the front matter reader.

# Because old copy is dirty
reverse_cleanup_unenc(LOOKUP_FOLDER)

cleanup_bom(PUB_READY_FOLDER)
cleanup_bom(LOOKUP_FOLDER)
cleanup_unenc(PUB_READY_FOLDER)
cleanup_unenc(LOOKUP_FOLDER)

# Files that have the necessary content.
gifted_files = []

print ('Traversing gifted files...')
for root, dirs, files in os.walk(LOOKUP_FOLDER):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            print ('File found: ' + file_path)
            gifted_files.append(file_path)

# Check if we have dupes in the list.
dupes = [item for item, count in collections.Counter(gifted_files).items() if count > 1]
dupe_count = len(dupes)
print ('Duplicate files found: ' + str(dupe_count))

if dupe_count > 0:
    print ('Dupe files in the folder with gifted Markdown content. Check your content.')
else:
    for g_file in gifted_files:
        for root, dirs, files in os.walk(PUB_READY_FOLDER):
            for file in files:
                s_file_path = os.path.join(root, file)
                base_path = os.path.basename(g_file)
                if str(file).lower() == base_path.lower():
                    print ('Found match for ' + g_file)
                    with open(g_file) as f:
                        post = frontmatter.load(f)
                        
                        content_url = ''
                        original_content_url = ''

                        if post.get('content_git_url'):
                            content_url = post.get('content_git_url')
                            print ('Metadata for the content_git_url:')
                            print (content_url)
                        if post.get('original_content_git_url'):
                            original_content_git_url = post.get('original_content_git_url')
                            print ('Metadata for the original_content_git_url:')
                            print (original_content_git_url)

                        print ('Reading target: ' + s_file_path)

                        with open(s_file_path, 'r+') as s_f:

                            s_post = frontmatter.load(s_f)

                            if (content_url):                          
                                s_post.metadata['content_git_url'] = content_url
                            
                            if (original_content_url):                          
                                s_post.metadata['original_content_git_url'] = content_url
                                
                            s_f.write(frontmatter.dumps(s_post))

reverse_cleanup_unenc(PUB_READY_FOLDER)

# And this is how I feel now that the script is working: 
#                                                                       ,---,  
#                                                                    ,`--.' |  
#            .---.                      ,---,                        |   :  :  
#           /. ./|                    ,--.' |                        '   '  ;  
#       .--'.  ' ;   ,---.     ,---.  |  |  :       ,---.     ,---.  |   |  |  
#      /__./ \ : |  '   ,'\   '   ,'\ :  :  :      '   ,'\   '   ,'\ '   :  ;  
#  .--'.  '   \' . /   /   | /   /   |:  |  |,--. /   /   | /   /   ||   |  '  
# /___/ \ |    ' '.   ; ,. :.   ; ,. :|  :  '   |.   ; ,. :.   ; ,. :'   :  |  
# ;   \  \;      :'   | |: :'   | |: :|  |   /' :'   | |: :'   | |: :;   |  ;  
#  \   ;  `      |'   | .; :'   | .; :'  :  | | |'   | .; :'   | .; :`---'. |  
#   .   \    .\  ;|   :    ||   :    ||  |  ' | :|   :    ||   :    | `--..`;  
#    \   \   ' \ | \   \  /  \   \  / |  :  :_:,' \   \  /  \   \  / .--,_     
#     :   '  |--"   `----'    `----'  |  | ,'      `----'    `----'  |    |`.  
#      \   \ ;                        `--''                          `-- -`, ; 
#       '---"                                                          '---`"  

print ('Done!')