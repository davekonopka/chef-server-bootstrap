#!/bin/bash

CHEF_REPO=/tmp/provisioning
CHEF_CLIENT_VERSION="11.18.12"

# Chef 11 compatible chef-server cookbook url
CHEF_COOKBOOK_URL="https://supermarket.chef.io/cookbooks/chef-server/versions/2.1.6/download"

# Install Chef Client
curl -L https://www.chef.io/chef/install.sh | sudo bash -s -- -v $CHEF_CLIENT_VERSION

# Create required bootstrap dirs/files
sudo mkdir -p $CHEF_REPO/cache $CHEF_REPO/cookbooks

cat >$CHEF_REPO/first_run.json <<EOL
{
  "chef-server": {
    "version": "11.1.6-1"
  },
  "run_list": [ "recipe[chef-server::default]" ]
}
EOL

# Pull down Chef 11 compatible cookbook
wget -qO- $CHEF_COOKBOOK_URL | sudo tar xvzC $CHEF_REPO/cookbooks

cd $CHEF_REPO
sudo chef-client -z -j $CHEF_REPO/first_run.json
