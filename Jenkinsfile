pipeline {
    agent any

    environment {
        AWS_REGION = "eu-central-1"
        ECR_REPO = "401713183707.dkr.ecr.eu-central-1.amazonaws.com/qa-framework"
        CLUSTER = "qa-automation-cluster-fixed-after-role-definition"
        TASK_DEF = "qa-framework-task"
        SUBNET = "subnet-018492d0f5ea2c9c9"
        SG = "sg-06c270f9f6e045654"
    }

    stages {

        stage('01 - Checkout') {
            steps {
                checkout scm
            }
        }

        stage('02 - Build Docker Image') {
            steps {
                script {
                    def tag = "build-${env.BUILD_NUMBER}"

                    echo "Building Docker image: ${env.ECR_REPO}:${tag}"

                    bat "docker build -t qa-framework:latest ."
                    bat "docker tag qa-framework:latest ${env.ECR_REPO}:${tag}"
                    bat "docker tag qa-framework:latest ${env.ECR_REPO}:latest"
                }
            }
        }

        stage('03 - AWS ECR Login') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    bat """
                    aws ecr get-login-password --region %AWS_REGION% ^
                    | docker login --username AWS --password-stdin ${env.ECR_REPO}
                    """
                }
            }
        }

        stage('04 - Push Image') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    bat "docker push ${env.ECR_REPO}:build-${env.BUILD_NUMBER}"
                    bat "docker push ${env.ECR_REPO}:latest"
                }
            }
        }

        stage('05 - Run Tests in Parallel (ECS)') {
            parallel {

                stage('API Tests') {
                    steps {
                        script {
                            runECSTest("api", "api")
                        }
                    }
                }

                stage('UI Tests') {
                    steps {
                        script {
                            runECSTest("ui", "ui or fullstack or auth")
                        }
                    }
                }

                stage('DB Tests') {
                    steps {
                        script {
                            runECSTest("db", "db")
                        }
                    }
                }
            }
        }

        stage('06 - Aggregate Flaky Reports') {
            steps {
                script {
                    withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: 'aws-creds'
                    ]]) {
                        bat """
                        set BUILD_NUMBER=${env.BUILD_NUMBER}
                        "C:\\Users\\sefit\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" utils\\flaky_aggregator.py
                        """
                    }
                }
            }
        }

        stage('07 - Reports Links') {
            steps {
                echo "API Report:"
                echo "https://qa-automation-reports-bucket-sefi.s3.eu-central-1.amazonaws.com/report-${env.BUILD_NUMBER}-api.html"

                echo "UI Report:"
                echo "https://qa-automation-reports-bucket-sefi.s3.eu-central-1.amazonaws.com/report-${env.BUILD_NUMBER}-ui.html"

                echo "DB Report:"
                echo "https://qa-automation-reports-bucket-sefi.s3.eu-central-1.amazonaws.com/report-${env.BUILD_NUMBER}-db.html"

                echo "Allure:"
                echo "https://qa-automation-reports-bucket-sefi.s3.eu-central-1.amazonaws.com/allure-latest/index.html"

                echo "Flaky Aggregated:"
                echo "https://qa-automation-reports-bucket-sefi.s3.eu-central-1.amazonaws.com/flaky-reports/aggregated-latest.json"
            }
        }

        stage('08 - Slack Notification') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'slack-webhook-url', variable: 'SLACK_WEBHOOK')
                    ]) {
                        bat """
                        set BUILD_NUMBER=${env.BUILD_NUMBER}
                        set SLACK_WEBHOOK=%SLACK_WEBHOOK%
                        "C:\\Users\\sefit\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" utils\\send_slack_alert.py
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished"
        }

        success {
            echo "SUCCESS - All ECS suites completed"
        }

        failure {
            echo "FAILURE - Something went wrong"
        }
    }
}


def runECSTest(String suite, String marker) {

    echo "======================================="
    echo "Running ECS suite: ${suite}"
    echo "Marker: ${marker}"
    echo "======================================="

    def taskFile = "task-${suite}.json"
    def resultFile = "result-${suite}.json"

    withCredentials([[
        $class: 'AmazonWebServicesCredentialsBinding',
        credentialsId: 'aws-creds'
    ]]) {

        bat """
        aws ecs run-task ^
        --cluster ${env.CLUSTER} ^
        --launch-type FARGATE ^
        --task-definition ${env.TASK_DEF} ^
        --count 1 ^
        --network-configuration "awsvpcConfiguration={subnets=[${env.SUBNET}],securityGroups=[${env.SG}],assignPublicIp=ENABLED}" ^
        --overrides "{\\"containerOverrides\\":[{\\"name\\":\\"qa-framework\\",\\"environment\\":[{\\"name\\":\\"PYTEST_MARKER\\",\\"value\\":\\"${marker}\\"},{\\"name\\":\\"REPORT_FILE\\",\\"value\\":\\"report-${env.BUILD_NUMBER}-${suite}.html\\"},{\\"name\\":\\"BUILD_NUMBER\\",\\"value\\":\\"${env.BUILD_NUMBER}\\"}]}]}" ^
        --region ${env.AWS_REGION} > ${taskFile}
        """

        def taskArn = powershell(
            script: "(Get-Content ${taskFile} | ConvertFrom-Json).tasks[0].taskArn",
            returnStdout: true
        ).trim()

        echo "Task ARN: ${taskArn}"

        bat """
        aws ecs wait tasks-stopped ^
        --cluster ${env.CLUSTER} ^
        --tasks ${taskArn} ^
        --region ${env.AWS_REGION}
        """

        bat """
        aws ecs describe-tasks ^
        --cluster ${env.CLUSTER} ^
        --tasks ${taskArn} ^
        --region ${env.AWS_REGION} > ${resultFile}
        """

        def status = powershell(
            script: "(Get-Content ${resultFile} | ConvertFrom-Json).tasks[0].containers[0].exitCode",
            returnStdout: true
        ).trim()

        if (status == "0") {
            echo "Suite ${suite} PASSED"
        } else if (suite == "db") {
            echo "Suite ${suite} has no tests or is optional → SKIPPED"
        } else {
            error "Suite ${suite} FAILED"
        }
    }
}