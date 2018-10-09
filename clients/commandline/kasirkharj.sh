#!/bin/bash
# set your variables
TOKEN=1234567
BASE_URL= http://localhost:8009
curl --data "token=$TOKEN&meghdar=$1&matn=$2" $BASE_URL/submit/kharj/
