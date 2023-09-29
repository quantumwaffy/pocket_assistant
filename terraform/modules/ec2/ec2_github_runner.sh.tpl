#! /bin/bash

#GitHub Runner
sudo yum install libicu -y
export RUNNER_CFG_PAT=${gh_pat}
sudo curl -s https://raw.githubusercontent.com/actions/runner/main/scripts/create-latest-svc.sh | bash -s ${gh_username}/${gh_repo}
