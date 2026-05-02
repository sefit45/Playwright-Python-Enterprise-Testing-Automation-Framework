pipeline {

    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'st', 'uat', 'prod'], description: 'Select environment')
    }

    environment {
        IMAGE_NAME = "qa-framework"
    }

    stages {

        stage('01 - Checkout') {
            steps {
                checkout scm
            }
        }

        stage('02 - Clean') {
            steps {
                bat """
                if exist allure-results rmdir /s /q allure-results
                if exist report.html del /q report.html
                if exist logs rmdir /s /q logs
                if exist screenshots rmdir /s /q screenshots

                mkdir allure-results
                """
            }
        }

        stage('03 - Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('04 - Parallel Execution') {
            parallel {

                stage('API Tests') {
                    steps {
                        echo "Running API tests..."
                        bat """
                        docker run --rm ^
                        -e ENV=${params.ENV} ^
                        ${IMAGE_NAME} ^
                        python -m pytest -m "api and not demo" --env=${params.ENV} --alluredir=allure-results
                        """
                    }
                }

                stage('UI + FullStack Tests') {
                    steps {
                        echo "Running UI & FullStack tests..."
                        bat """
                        docker run --rm ^
                        -e ENV=${params.ENV} ^
                        ${IMAGE_NAME} ^
                        python -m pytest -m "(ui or fullstack) and not demo" --env=${params.ENV} --alluredir=allure-results
                        """
                    }
                }

                stage('DB Tests') {
                    steps {
                        echo "Running DB tests..."
                        bat """
                        docker run --rm ^
                        -e ENV=${params.ENV} ^
                        ${IMAGE_NAME} ^
                        python -m pytest -m "db and not demo" --env=${params.ENV} --alluredir=allure-results
                        """
                    }
                }

                stage('Auth Tests') {
                    steps {
                        echo "Running Auth tests..."
                        bat """
                        docker run --rm ^
                        -e ENV=${params.ENV} ^
                        ${IMAGE_NAME} ^
                        python -m pytest -m "auth and not demo" --env=${params.ENV} --alluredir=allure-results
                        """
                    }
                }
            }
        }

        stage('05 - Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('06 - Archive') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo 'SUCCESS - Parallel Docker execution completed'
        }
        failure {
            echo 'FAILURE - One or more suites failed'
        }
    }
}