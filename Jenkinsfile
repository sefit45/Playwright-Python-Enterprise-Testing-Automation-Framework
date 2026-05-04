pipeline {

    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'st', 'uat', 'prod'], description: 'Select environment')
    }

    environment {
        AWS_REGION = "eu-central-1"
        AWS_ACCOUNT_ID = "401713183707"

        ECR_REPOSITORY = "qa-framework"
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        IMAGE_TAG = "build-${BUILD_NUMBER}"

        FULL_IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
        LATEST_IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"

        ECS_CLUSTER = "qa-automation-cluster-fixed-after-role-definition"
        ECS_TASK_DEFINITION = "qa-framework-task"
        ECS_CONTAINER_NAME = "qa-framework"

        ECS_SUBNETS = "subnet-018492d0f5ea2c9c9"
        ECS_SECURITY_GROUP = "sg-06c270f9f6e045654"
    }

    stages {

        stage('01 - Checkout') {
            steps {
                checkout scm
            }
        }

        stage('02 - Build Docker Image') {
            steps {
                echo "Building Docker image: ${FULL_IMAGE}"

                bat """
                docker build -t ${ECR_REPOSITORY}:latest .
                docker tag ${ECR_REPOSITORY}:latest ${FULL_IMAGE}
                docker tag ${ECR_REPOSITORY}:latest ${LATEST_IMAGE}
                """
            }
        }

        stage('03 - AWS ECR Login') {
            steps {
                echo "Logging Docker into AWS ECR"

                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    bat """
                    aws ecr get-login-password --region ${AWS_REGION} ^
                    | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    """
                }
            }
        }

        stage('04 - Push Docker Image to ECR') {
            steps {
                echo "Pushing Docker image to ECR"

                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    bat """
                    docker push ${FULL_IMAGE}
                    docker push ${LATEST_IMAGE}
                    """
                }
            }
        }

        stage('05 - Run ECS Fargate Task') {
            steps {
                echo "Running ECS Fargate task from image: ${LATEST_IMAGE}"

                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    bat """
                    aws ecs run-task ^
                      --cluster ${ECS_CLUSTER} ^
                      --launch-type FARGATE ^
                      --task-definition ${ECS_TASK_DEFINITION} ^
                      --count 1 ^
                      --network-configuration "awsvpcConfiguration={subnets=[${ECS_SUBNETS}],securityGroups=[${ECS_SECURITY_GROUP}],assignPublicIp=ENABLED}" ^
                      --region ${AWS_REGION} > ecs-run-task-output.json
                    """
                }
            }
        }

        stage('06 - Archive ECS Run Output') {
            steps {
                archiveArtifacts artifacts: 'ecs-run-task-output.json', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo "Pipeline finished"
        }

        success {
            echo "SUCCESS - Jenkins built image, pushed to ECR and triggered ECS Fargate task"
        }

        failure {
            echo "FAILURE - Jenkins pipeline failed"
        }
    }
}