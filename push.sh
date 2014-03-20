#!/bin/bash

cd /home/ahoward/DevOps-Challenges-Cycle1
git pull
git status | grep deleted | perl -pe 's/^#\s*deleted:\s*(.*)$/\1/' | \
while read LINE; do
  git rm $LINE
done
find . | xargs git add
git commit
git push
