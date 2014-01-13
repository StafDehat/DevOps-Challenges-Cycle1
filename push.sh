#!/bin/bash

cd /home/ahoward/DevOps-Challenges-Cycle1
find . | xargs git add
git commit
git push
