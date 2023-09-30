#! /bin/bash

#GitHub Runner
sudo apt install -y jq
export RUNNER_CFG_PAT=${gh_pat}
sudo curl -s https://raw.githubusercontent.com/actions/runner/main/scripts/create-latest-svc.sh | bash -s ${gh_username}/${gh_repo}
