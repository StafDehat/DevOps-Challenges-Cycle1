#!/bin/bash

git pull
git status | grep deleted | perl -pe 's/^#\s*deleted:\s*(.*)$/\1/' | \
while read LINE; do
  git rm $LINE
done
cd /home/ahoward/DevOps-Challenges-Cycle1
find . | xargs git add
git commit
git push
