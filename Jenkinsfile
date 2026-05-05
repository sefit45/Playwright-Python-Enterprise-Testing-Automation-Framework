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

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def tag = "build-${env.BUILD_NUMBER}"
                    env.IMAGE = "${ECR_REPO}:${tag}"

                    bat "docker build -t qa-framework:latest ."
                    bat "docker tag qa-framework:latest ${env.IMAGE}"
                    bat "docker tag qa-framework:latest ${ECR_REPO}:latest"
                }
            }
        }

        stage('ECR Login & Push') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    bat """
                    aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin ${ECR_REPO}
                    docker push ${env.IMAGE}
                    docker push ${ECR_REPO}:latest
                    """
                }
            }
        }

        stage('Run ECS Tasks in Parallel') {
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
    }
}

def runEcsTask(marker, name) {

    withCredentials([[
        $class: 'AmazonWebServicesCredentialsBinding',
        credentialsId: 'aws-creds'
    ]]) {

        def reportName = "report-${env.BUILD_NUMBER}-${name}.html"

        bat """
        aws ecs run-task ^
          --cluster ${CLUSTER} ^
          --launch-type FARGATE ^
          --task-definition ${TASK_DEF} ^
          --count 1 ^
          --network-configuration "awsvpcConfiguration={subnets=[${SUBNET}],securityGroups=[${SG}],assignPublicIp=ENABLED}" ^
          --overrides "{\\"containerOverrides\\":[{\\"name\\":\\"qa-framework\\",\\"environment\\":[{\\"name\\":\\"PYTEST_MARKER\\",\\"value\\":\\"${marker}\\"},{\\"name\\":\\"REPORT_FILE\\",\\"value\\":\\"${reportName}\\"}]}]}" ^
          --region ${AWS_REGION} > task-${name}.json
        """

        def taskArn = readFile("task-${name}.json")
            .split('"taskArn": "')[1]
            .split('"')[0]

        echo "Task ARN (${name}): ${taskArn}"

        bat """
        aws ecs wait tasks-stopped ^
          --cluster ${CLUSTER} ^
          --tasks ${taskArn} ^
          --region ${AWS_REGION}
        """

        bat """
        aws ecs describe-tasks ^
          --cluster ${CLUSTER} ^
          --tasks ${taskArn} ^
          --region ${AWS_REGION} > result-${name}.json
        """

        def result = readFile("result-${name}.json")

        if (!result.contains('"exitCode": 0')) {
            error "Task ${name} FAILED"
        } else {
            echo "Task ${name} PASSED"
        }
    }
}