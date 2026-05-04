pipeline {

    agent any

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

        ECS_SUBNETS = "subnet-018492d0f5ea2c9c9"
        ECS_SECURITY_GROUP = "sg-06c270f9f6e045654"

        S3_BUCKET = "qa-automation-reports-bucket-sefi"
        REPORT_FILE = "report-${BUILD_NUMBER}.html"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                bat """
                docker build -t ${ECR_REPOSITORY}:latest .
                docker tag ${ECR_REPOSITORY}:latest ${FULL_IMAGE}
                docker tag ${ECR_REPOSITORY}:latest ${LATEST_IMAGE}
                """
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([[
                    \$class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    bat """
                    aws ecr get-login-password --region ${AWS_REGION} ^
                    | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    """
                }
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([[
                    \$class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    bat """
                    docker push ${FULL_IMAGE}
                    docker push ${LATEST_IMAGE}
                    """
                }
            }
        }

        stage('Run ECS Task') {
            steps {
                withCredentials([[
                    \$class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {

                    bat """
                    aws ecs run-task ^
                      --cluster ${ECS_CLUSTER} ^
                      --launch-type FARGATE ^
                      --task-definition ${ECS_TASK_DEFINITION} ^
                      --count 1 ^
                      --network-configuration "awsvpcConfiguration={subnets=[${ECS_SUBNETS}],securityGroups=[${ECS_SECURITY_GROUP}],assignPublicIp=ENABLED}" ^
                      --overrides "{\\"containerOverrides\\":[{\\"name\\":\\"qa-framework\\",\\"environment\\":[{\\"name\\":\\"REPORT_FILE\\",\\"value\\":\\"${REPORT_FILE}\\"}]}]}" ^
                      --region ${AWS_REGION} > task.json
                    """
                }
            }
        }

        stage('Wait for Task to Finish') {
            steps {
                withCredentials([[
                    \$class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {

                    script {
                        def taskArn = bat(
                            script: 'powershell -Command "(Get-Content task.json | ConvertFrom-Json).tasks[0].taskArn"',
                            returnStdout: true
                        ).trim()

                        echo "Task ARN: ${taskArn}"

                        bat """
                        aws ecs wait tasks-stopped ^
                          --cluster ${ECS_CLUSTER} ^
                          --tasks ${taskArn} ^
                          --region ${AWS_REGION}
                        """

                        bat """
                        aws ecs describe-tasks ^
                          --cluster ${ECS_CLUSTER} ^
                          --tasks ${taskArn} ^
                          --region ${AWS_REGION} > result.json
                        """
                    }
                }
            }
        }

        stage('Print Report Link') {
            steps {
                echo "Report:"
                echo "https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${REPORT_FILE}"
            }
        }
    }

    post {
        success {
            echo "🔥 SUCCESS - Everything is working end-to-end"
        }
        failure {
            echo "❌ FAILURE"
        }
    }
}