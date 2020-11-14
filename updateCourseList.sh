# if the last commit contains course list updates,
# we can squash new updates to it
git add .
git commit -m "u"
git rebase -i HEAD~2
git push --force origin master