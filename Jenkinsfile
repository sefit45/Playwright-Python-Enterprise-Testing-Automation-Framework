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
        LATEST_REPORT_FILE = "latest.html"
        ALLURE_FOLDER = "allure-latest"
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
                      --overrides "{\\"containerOverrides\\":[{\\"name\\":\\"qa-framework\\",\\"environment\\":[{\\"name\\":\\"REPORT_FILE\\",\\"value\\":\\"${REPORT_FILE}\\"}]}]}" ^
                      --region ${AWS_REGION} > task.json
                    """
                }
            }
        }

        stage('06 - Wait for ECS Task to Finish') {
            steps {
                echo "Waiting for ECS task to finish"

                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    script {
                        def taskArn = bat(
                            script: '@powershell -NoProfile -Command "(Get-Content task.json | ConvertFrom-Json).tasks[0].taskArn"',
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

        stage('07 - Check Test Result') {
            steps {
                echo "Checking test result from ECS"

                script {
                    def exitCode = bat(
                        script: '@powershell -NoProfile -Command "(Get-Content result.json | ConvertFrom-Json).tasks[0].containers[0].exitCode"',
                        returnStdout: true
                    ).trim()

                    echo "Container exit code: ${exitCode}"

                    if (exitCode != "0") {
                        error("Tests FAILED")
                    } else {
                        echo "Tests PASSED"
                    }
                }
            }
        }

        stage('08 - Archive ECS Output') {
            steps {
                archiveArtifacts artifacts: 'task.json,result.json', allowEmptyArchive: true
            }
        }

        stage('09 - Print Report Link') {
            steps {
                echo "Report URL:"
                echo "https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${REPORT_FILE}"

                echo "Latest Report URL:"
                echo "https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${LATEST_REPORT_FILE}"

                echo "Allure Report URL:"
                echo "https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${ALLURE_FOLDER}/index.html"
            }
        }
    }

    post {
        always {
            echo "Pipeline finished"
            echo "Report URL: https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${REPORT_FILE}"
            echo "Latest Report URL: https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${LATEST_REPORT_FILE}"
            echo "Allure URL: https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${ALLURE_FOLDER}/index.html"
        }

        success {
            echo "SUCCESS - Jenkins built image, pushed to ECR, ran ECS Fargate task, waited for completion and tests passed"

            withCredentials([string(credentialsId: 'slack-webhook-url', variable: 'SLACK_WEBHOOK_URL')]) {
                script {
                    writeFile file: 'send-slack.ps1', text: """
\$payload = @{
    text = "✅ QA PASSED - Build ${BUILD_NUMBER} - Report: https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${REPORT_FILE} - Allure: https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${ALLURE_FOLDER}/index.html"
} | ConvertTo-Json -Compress

Invoke-RestMethod -Uri \$env:SLACK_WEBHOOK_URL -Method Post -ContentType "application/json" -Body \$payload
"""
                    bat 'powershell -NoProfile -ExecutionPolicy Bypass -File send-slack.ps1'
                }
            }
        }

        failure {
            echo "FAILURE - Jenkins pipeline failed or tests failed"

            withCredentials([string(credentialsId: 'slack-webhook-url', variable: 'SLACK_WEBHOOK_URL')]) {
                script {
                    writeFile file: 'send-slack.ps1', text: """
\$payload = @{
    text = "❌ QA FAILED - Build ${BUILD_NUMBER} - Report: https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${REPORT_FILE} - Allure: https://${S3_BUCKET}.s3.${AWS_REGION}.amazonaws.com/${ALLURE_FOLDER}/index.html"
} | ConvertTo-Json -Compress

Invoke-RestMethod -Uri \$env:SLACK_WEBHOOK_URL -Method Post -ContentType "application/json" -Body \$payload
"""
                    bat 'powershell -NoProfile -ExecutionPolicy Bypass -File send-slack.ps1'
                }
            }
        }
    }
}