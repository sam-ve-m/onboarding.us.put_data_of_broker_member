fission spec init
fission env create --spec --name onb-us-broker-mmbr-env --image nexus.sigame.com.br/fission-onboarding-us-broker-member-ben:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-us-broker-mmbr-fn --env onb-us-broker-mmbr-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-us-broker-mmbr-rt --method PUT --url /onboarding/broker_member --function onb-us-broker-mmbr-fn