#!/bin/bash

fission spec init
fission env create --spec --name update-member-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name update-member-fn --env update-member-env --src "./func/*" --entrypoint main.update_exchange_member --executortype newdeploy --maxscale 1
fission route create --spec --name update-member-rt --method PUT --url /onboarding/broker_member --function update-member-fn