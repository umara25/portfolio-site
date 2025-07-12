#!/bin/bash

curl --request POST http://localhost:5000/api/timeline_post -d 'name=Umar&email=umarahmer1@gmail.com&content=this is a test'

curl --request GET http://localhost:5000/api/timeline_post


