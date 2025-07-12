#!/bin/bash

RES=$(curl -s -4 --request POST http://localhost:5000/api/timeline_post \
-d 'name=Test&email=example@test.com&content=This is a test timeline post')

curl -4 http://localhost:5000/api/timeline_post

ID=$(echo "$RES" | jq '.id')

curl -4 --request DELETE http://localhost:5000/api/timeline_post/$ID
