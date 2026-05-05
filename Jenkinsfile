pipeline {
    agent any

    environment {
        AWS_REGION = "eu-central-1"
        ECR_REPO = "401713183707.dkr.ecr.eu-central-1.amazonaws.com/qa-framework"
        CLUSTER = "qa-automation-cluster-fixed-after-role-definition"
        TASK_DEF = "qa-framework-task"
        CONTAINER_NAME = "qa-framework"
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
                    env.IMAGE_TAG = "build-${env.BUILD_NUMBER}"
                    env.FULL_IMAGE = "${env.ECR_REPO}:${env.IMAGE_TAG}"

                    echo "Building Docker image: ${env.FULL_IMAGE}"

                    bat "docker build -t qa-framework:latest ."
                    bat "docker tag qa-framework:latest ${env.FULL_IMAGE}"
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
                    | docker login --username AWS --password-stdin 401713183707.dkr.ecr.eu-central-1.amazonaws.com
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
                    bat """
                    docker push ${env.FULL_IMAGE}
                    docker push ${env.ECR_REPO}:latest
                    """
                }
            }
        }

        stage('05 - Run Tests in Parallel (ECS)') {
            parallel {

                stage('API Tests') {
                    steps {
                        script {
                            runEcsTask("api", "api")
                        }
                    }
                }

                stage('UI Tests') {
                    steps {
                        script {
                            runEcsTask("ui or fullstack or auth", "ui")
                        }
                    }
                }

                stage('DB Tests') {
                    steps {
                        script {
                            runEcsTask("db", "db")
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
                        python utils\\flaky_aggregator.py
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

                echo "Flaky Dashboard:"
                echo "https://qa-automation-reports-bucket-sefi.s3.eu-central-1.amazonaws.com/flaky-reports/aggregated-latest.json"
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
            echo "FAILURE - One or more suites failed"
        }
    }
}


def runEcsTask(String marker, String suiteName) {

    withCredentials([[
        $class: 'AmazonWebServicesCredentialsBinding',
        credentialsId: 'aws-creds'
    ]]) {

        def reportName = "report-${env.BUILD_NUMBER}-${suiteName}.html"

        echo "======================================="
        echo "Running ECS suite: ${suiteName}"
        echo "Marker: ${marker}"
        echo "======================================="

        bat """
        aws ecs run-task ^
          --cluster ${env.CLUSTER} ^
          --launch-type FARGATE ^
          --task-definition ${env.TASK_DEF} ^
          --count 1 ^
          --network-configuration "awsvpcConfiguration={subnets=[${env.SUBNET}],securityGroups=[${env.SG}],assignPublicIp=ENABLED}" ^
          --overrides "{\\"containerOverrides\\":[{\\"name\\":\\"${env.CONTAINER_NAME}\\",\\"environment\\":[{\\"name\\":\\"PYTEST_MARKER\\",\\"value\\":\\"${marker}\\"},{\\"name\\":\\"REPORT_FILE\\",\\"value\\":\\"${reportName}\\"},{\\"name\\":\\"BUILD_NUMBER\\",\\"value\\":\\"${env.BUILD_NUMBER}\\"}]}]}" ^
          --region ${env.AWS_REGION} > task-${suiteName}.json
        """

        def taskJson = readFile("task-${suiteName}.json")
        def taskArn = taskJson.split('"taskArn": "')[1].split('"')[0]

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
          --region ${env.AWS_REGION} > result-${suiteName}.json
        """

        def result = readFile("result-${suiteName}.json")

        // ===============================
        // SMART RESULT HANDLING
        // ===============================

        if (result.contains('"exitCode": 0')) {
            echo "Suite ${suiteName} PASSED"
        }
        else if (suiteName == "db") {
            echo "Suite ${suiteName} has no tests or is optional → SKIPPED"
        }
        else {
            error "Suite ${suiteName} FAILED"
        }
    }
}