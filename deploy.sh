#!/bin/bash

fission spec init
fission env create --spec --name update-experience-time-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name update-experience-time-fn --env update-experience-time-env --src "./func/*" --entrypoint main.update_experience_time --executortype newdeploy --maxscale 1
fission route create --spec --name update-experience-time-rt --method PUT --url /update-experience-time --function update-experience-time-fn