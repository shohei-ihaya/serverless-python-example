#!/usr/local/bin bats

# Sleep some seconds needed for stable test pass(if not, sometimes localstack's docker not started yet when run `sam loacl invoke`)
setup() {
    echo "setup"
    docker-compose up -d localstack
    sleep 5
    docker_network_id=$(docker network ls -q -f NAME=$(basename $(pwd))_default)
}

teardown() {
    echo "teardown"
    docker-compose down
}

# By default, sam create api-gw. And the event it pass lambda has "not base64 encoded" body
# However, the command `sam local generate-event` return the event, and its body id "base64 encoded"
# As a workaround, read body json and create event json like {"body" : {"key":"val"}} which format is that lambda actually get at production dev

# This test use 'bats'.
# You should write such way `[(space)'actual' = 'expcted'(space)]`. Otherwise, you'll fail test with status 127
# Status 127 generally means 'command not found'.

@test "Lambda function should return correct response" {
    body=$(echo $(cat src/tests/payload_body.json) | sed -e 's/"/\\\\\\"/g')
    sed -e "s/content/$body/" src/tests/payload_template.json > event.json
    actual=`pipenv run sam local invoke "SendEmail" --docker-network "${docker_network_id}" -t sam_template.yml --event event.json --env-vars environments/sam_local_env.json | jq -r .`
    rm event.json
    [ `echo "${actual}" | jq .body` = '"success"' ]
    [ `echo "${actual}" | jq .statusCode` -eq 200 ]
}
