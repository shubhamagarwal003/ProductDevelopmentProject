set +e

CreateDocker () {
	docker build -t britecore_webapp .
	docker tag britecore_webapp shubham003/britecore_webapp
	docker push shubham003/britecore_webapp
}

DeployDocker() {
	aws ecs create-cluster --cluster-name britecore-cluster
	aws ecs register-task-definition --cli-input-json file://./fargate-task.json
	aws ecs run-task --cli-input-json file://./fargate-run-task.json
	# aws ecs create-service --cluster britecore-cluster --service-name britecore-service \
	# --task-definition britecore-fargate --desired-count 2 --launch-type "FARGATE" \
	# --network-configuration "awsvpcConfiguration={subnets=[subnet-b0118abf],securityGroups=[sg-a9943de2],assignPublicIp=ENABLED}"
}

MODE=$1
if [ $MODE == "Create" ]
        then
                echo "Creating Image"
                CreateDocker
elif [ $MODE == "Deploy" ]
        then
                echo "Deploying Image"
                DeployDocker

fi

# sg-a9943de2
# subnet-177c1e5d