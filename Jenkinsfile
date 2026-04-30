// Jenkins Pipeline for Playwright Python Enterprise Automation Framework
// This pipeline supports dynamic environment selection and dynamic test suite selection

pipeline {

    // Run pipeline on any available Jenkins agent
    agent any

    environment {

        // Explicit Python virtual environment paths for local Windows Jenkins execution
        PYTHON = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\python.exe"
        PIP = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pip.exe"
        PYTEST = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pytest.exe"
        PLAYWRIGHT = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\playwright.exe"
    }

    stages {

        stage('Checkout Code') {
            steps {

                // Pull latest code from GitHub repository
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {

                // Upgrade pip package manager
                bat "\"%PYTHON%\" -m pip install --upgrade pip"

                // Install project dependencies
                bat "\"%PIP%\" install -r requirements.txt"

                // Install Playwright browsers
                bat "\"%PLAYWRIGHT%\" install"
            }
        }

        stage('Resolve Test Parameters') {
            steps {
                script {

                    // Convert selected environment into pytest --env value
                    if (params.ENV == 'Dev') {
                        env.SELECTED_ENV = 'dev'
                    } else if (params.ENV == 'ST') {
                        env.SELECTED_ENV = 'qa'
                    } else if (params.ENV == 'UAT') {
                        env.SELECTED_ENV = 'qa'
                    } else if (params.ENV == 'PROD-Like') {
                        env.SELECTED_ENV = 'prod'
                    } else if (params.ENV == 'PROD') {
                        env.SELECTED_ENV = 'prod'
                    } else {
                        env.SELECTED_ENV = 'dev'
                    }

                    // Convert selected test suite into pytest marker
                    if (params.TEST_SUITE == 'Minimal Connectivity Tests - MCT') {
                        env.SELECTED_MARKER = 'smoke'
                    } else if (params.TEST_SUITE == 'Sanity Tests') {
                        env.SELECTED_MARKER = 'sanity'
                    } else if (params.TEST_SUITE == 'Progression Tests') {
                        env.SELECTED_MARKER = 'regression'
                    } else if (params.TEST_SUITE == 'Regression Tests') {
                        env.SELECTED_MARKER = 'regression'
                    } else if (params.TEST_SUITE == 'APIs Tests') {
                        env.SELECTED_MARKER = 'api'
                    } else if (params.TEST_SUITE == 'DB Tests') {
                        env.SELECTED_MARKER = 'db'
                    } else if (params.TEST_SUITE == 'UI Tests') {
                        env.SELECTED_MARKER = 'ui'
                    } else {
                        env.SELECTED_MARKER = 'smoke'
                    }

                    // Print selected execution configuration
                    echo "Selected environment: ${env.SELECTED_ENV}"
                    echo "Selected test marker: ${env.SELECTED_MARKER}"
                }
            }
        }

        stage('Run Tests') {
            steps {

                // Run pytest using selected environment and selected marker
                bat "\"%PYTEST%\" -m %SELECTED_MARKER% --env=%SELECTED_ENV% --alluredir=allure-results"
            }
        }

        stage('Generate Allure Report') {
            steps {

                // Publish Allure report inside Jenkins
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('Archive HTML Report') {
            steps {

                // Archive pytest HTML report
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }

        stage('Archive Allure Results') {
            steps {

                // Archive raw Allure result files
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }
    }

    post {

        always {

            // Always print final status
            echo 'Pipeline execution completed.'
        }

        success {

            // Success message
            echo 'Automation tests completed successfully.'
        }

        failure {

            // Failure message
            echo 'Automation tests failed. Please check logs and reports.'
        }
    }
}