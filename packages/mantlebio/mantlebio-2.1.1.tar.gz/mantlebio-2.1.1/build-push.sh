#!/bin/bash
set -e;

TAG=mantle-sdk
REGION=us-west-2

echo "Building mantle-sdk image...";

DOCKER_BUILDKIT=1 docker build --platform linux/amd64 --tag $TAG .

echo "Tagging $TAG image...";
docker tag mantle-sdk:latest public.ecr.aws/c7j2m0e6/mantle-sdk:latest

echo "Pushing $TAG image...";
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/c7j2m0e6

docker push public.ecr.aws/c7j2m0e6/mantle-sdk:latest