#!/bin/sh

# Changing the author (or committer) would require re-writing all of the history. 
# If you're okay with that and think it's worth it then you should check out 
# git filter-branch. The man page includes several examples to get you started. 
# Also note that you can use environment variables to change the name of the author, 
# committer, dates, etc. -- see the "Environment Variables" section of the git man page.

# Specifically, you can fix all the wrong author names and emails for all branches 
# and tags with this command (source: GitHub help):

git filter-branch --env-filter '
OLD_EMAIL="cgg@festo.net"
CORRECT_NAME="Christian Gröling"
CORRECT_EMAIL="ch.groeling@gmail.com"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags