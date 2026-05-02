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
                if exist allure-results-api rmdir /s /q allure-results-api
                if exist allure-results-ui rmdir /s /q allure-results-ui
                if exist allure-results-db rmdir /s /q allure-results-db
                if exist allure-results-auth rmdir /s /q allure-results-auth

                if exist flaky-reports-api rmdir /s /q flaky-reports-api
                if exist flaky-reports-ui rmdir /s /q flaky-reports-ui
                if exist flaky-reports-db rmdir /s /q flaky-reports-db
                if exist flaky-reports-auth rmdir /s /q flaky-reports-auth

                mkdir allure-results-api
                mkdir allure-results-ui
                mkdir allure-results-db
                mkdir allure-results-auth

                mkdir flaky-reports-api
                mkdir flaky-reports-ui
                mkdir flaky-reports-db
                mkdir flaky-reports-auth
                """
            }
        }

        stage('03 - Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('04 - Parallel Docker Execution') {
            parallel {

                stage('API Tests') {
                    steps {
                        bat """
                        docker run --rm ^
                        -v "%CD%\\allure-results-api:/app/allure-results" ^
                        -v "%CD%\\flaky-reports-api:/app/flaky-reports" ^
                        -e FLAKY_REPORT_FILE=/app/flaky-reports/flaky_report.json ^
                        ${IMAGE_NAME} ^
                        python -m pytest -m "api and not demo" --env=${params.ENV} --reruns 2 --reruns-delay 1 --alluredir=/app/allure-results
                        """
                    }
                }

                stage('UI + FullStack Tests') {
                    steps {
                        bat """
                        docker run --rm ^
                        -v "%CD%\\allure-results-ui:/app/allure-results" ^
                        -v "%CD%\\flaky-reports-ui:/app/flaky-reports" ^
                        -e FLAKY_REPORT_FILE=/app/flaky-reports/flaky_report.json ^
                        ${IMAGE_NAME} ^
                        python -m pytest -m "(ui or fullstack) and not demo" --env=${params.ENV} --reruns 2 --reruns-delay 1 --alluredir=/app/allure-results
                        """
                    }
                }

                stage('DB Tests') {
                    steps {
                        bat """
                        docker run --rm ^
                        -v "%CD%\\allure-results-db:/app/allure-results" ^
                        -v "%CD%\\flaky-reports-db:/app/flaky-reports" ^
                        -e FLAKY_REPORT_FILE=/app/flaky-reports/flaky_report.json ^
                        ${IMAGE_NAME} ^
                        python -m pytest -m "db and not demo" --env=${params.ENV} --reruns 2 --reruns-delay 1 --alluredir=/app/allure-results
                        """
                    }
                }

                stage('Auth Tests') {
                    steps {
                        bat """
                        docker run --rm ^
                        -v "%CD%\\allure-results-auth:/app/allure-results" ^
                        -v "%CD%\\flaky-reports-auth:/app/flaky-reports" ^
                        -e FLAKY_REPORT_FILE=/app/flaky-reports/flaky_report.json ^
                        ${IMAGE_NAME} ^
                        python -m pytest -m "auth and not demo" --env=${params.ENV} --reruns 2 --reruns-delay 1 --alluredir=/app/allure-results
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
                    results: [
                        [path: 'allure-results-api'],
                        [path: 'allure-results-ui'],
                        [path: 'allure-results-db'],
                        [path: 'allure-results-auth']
                    ]
                ])
            }
        }

        stage('06 - Archive') {
            steps {
                archiveArtifacts artifacts: 'allure-results-api/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results-ui/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results-db/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results-auth/**', allowEmptyArchive: true

                archiveArtifacts artifacts: 'flaky-reports-api/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'flaky-reports-ui/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'flaky-reports-db/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'flaky-reports-auth/**', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo 'SUCCESS - Parallel Docker execution completed with flaky analytics'
        }
        failure {
            echo 'FAILURE - One or more suites failed'
        }
    }
}