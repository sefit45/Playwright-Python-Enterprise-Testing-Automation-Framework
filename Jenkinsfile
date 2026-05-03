pipeline {

    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'st', 'uat', 'prod'], description: 'Select environment')
    }

    environment {
        DOCKER_IMAGE = "sefit1976/qa-framework"
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        FULL_IMAGE = "${DOCKER_IMAGE}:${IMAGE_TAG}"
    }

    stages {

        stage('01 - Checkout') {
            steps {
                checkout scm
            }
        }

        stage('02 - Build Docker Image') {
            steps {
                echo "Building Docker image ${FULL_IMAGE}"
                bat "docker build -t ${FULL_IMAGE} ."
            }
        }

        stage('03 - Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat """
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    """
                }
            }
        }

        stage('04 - Push Docker Image') {
            steps {
                echo "Pushing Docker image ${FULL_IMAGE}"
                bat "docker push ${FULL_IMAGE}"
            }
        }

        stage('05 - Prepare Workspace') {
            steps {
                bat """
                if exist allure-results-api rmdir /s /q allure-results-api
                if exist allure-results-ui rmdir /s /q allure-results-ui
                if exist allure-results-db rmdir /s /q allure-results-db
                if exist allure-results-auth rmdir /s /q allure-results-auth
                if exist allure-results-flaky rmdir /s /q allure-results-flaky

                if exist flaky-reports-api rmdir /s /q flaky-reports-api
                if exist flaky-reports-ui rmdir /s /q flaky-reports-ui
                if exist flaky-reports-db rmdir /s /q flaky-reports-db
                if exist flaky-reports-auth rmdir /s /q flaky-reports-auth

                mkdir allure-results-api
                mkdir allure-results-ui
                mkdir allure-results-db
                mkdir allure-results-auth
                mkdir allure-results-flaky

                mkdir flaky-reports-api
                mkdir flaky-reports-ui
                mkdir flaky-reports-db
                mkdir flaky-reports-auth
                """
            }
        }

        stage('06 - Parallel Test Execution') {
            parallel {

                stage('API Tests') {
                    steps {
                        bat """
                        docker run --rm ^
                        -v "%CD%\\allure-results-api:/app/allure-results" ^
                        -v "%CD%\\flaky-reports-api:/app/flaky-reports" ^
                        -e FLAKY_REPORT_FILE=/app/flaky-reports/flaky_report.json ^
                        ${FULL_IMAGE} ^
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
                        ${FULL_IMAGE} ^
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
                        ${FULL_IMAGE} ^
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
                        ${FULL_IMAGE} ^
                        python -m pytest -m "auth and not demo" --env=${params.ENV} --reruns 2 --reruns-delay 1 --alluredir=/app/allure-results
                        """
                    }
                }
            }
        }

        stage('07 - Generate Flaky Dashboard') {
            steps {
                echo "Generating Flaky Analytics Dashboard"
                bat """
                docker run --rm ^
                -v "%CD%\\flaky-reports-api:/app/flaky-reports-api" ^
                -v "%CD%\\flaky-reports-ui:/app/flaky-reports-ui" ^
                -v "%CD%\\flaky-reports-db:/app/flaky-reports-db" ^
                -v "%CD%\\flaky-reports-auth:/app/flaky-reports-auth" ^
                -v "%CD%\\allure-results-flaky:/app/allure-results-flaky" ^
                ${FULL_IMAGE} ^
                python utils/flaky_dashboard.py
                """
            }
        }

        stage('08 - Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [
                        [path: 'allure-results-api'],
                        [path: 'allure-results-ui'],
                        [path: 'allure-results-db'],
                        [path: 'allure-results-auth'],
                        [path: 'allure-results-flaky']
                    ]
                ])
            }
        }

        stage('09 - Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'allure-results-*/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'flaky-reports-*/**', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo "SUCCESS - Image ${FULL_IMAGE} built, pushed and tested"
        }
        failure {
            echo "FAILURE - Pipeline failed"
        }
        always {
            echo "Pipeline finished"
        }
    }
}