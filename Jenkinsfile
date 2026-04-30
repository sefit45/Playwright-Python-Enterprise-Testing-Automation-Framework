// Jenkins Pipeline for Playwright Python Enterprise Automation Framework
// This pipeline supports dynamic environment selection, dynamic test suite selection,
// Allure reporting, artifact archiving, and delayed test result evaluation

pipeline {

    // Run pipeline on any available Jenkins agent
    agent any

    environment {

        // Explicit Python virtual environment paths for local Windows Jenkins execution
        PYTHON = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\python.exe"
        PIP = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pip.exe"
        PYTEST = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pytest.exe"
        PLAYWRIGHT = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\playwright.exe"

        // Default test status value
        TEST_STATUS = "0"
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

                // Install project dependencies from requirements.txt
                bat "\"%PIP%\" install -r requirements.txt"

                // Install Playwright browsers
                bat "\"%PLAYWRIGHT%\" install"
            }
        }

        stage('Resolve Test Parameters') {
            steps {
                script {

                    // Convert selected Jenkins environment into pytest --env value
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

                    // Convert selected Jenkins test suite into pytest marker
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
                script {

                    // Run pytest and capture exit code without stopping the pipeline immediately
                    def exitCode = bat(
                        script: "\"%PYTEST%\" -m %SELECTED_MARKER% --env=%SELECTED_ENV% --alluredir=allure-results",
                        returnStatus: true
                    )

                    // Print pytest exit code
                    echo "Pytest exit code: ${exitCode}"

                    // Save pytest exit code for final evaluation
                    env.TEST_STATUS = exitCode.toString()
                }
            }
        }

        stage('Generate Allure Report') {
            steps {

                // Publish Allure report inside Jenkins even if tests failed
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('Archive HTML Report') {
            steps {

                // Archive pytest HTML report as Jenkins artifact
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }

        stage('Archive Allure Results') {
            steps {

                // Archive raw Allure result files as Jenkins artifacts
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }

        stage('Evaluate Test Results') {
            steps {
                script {

                    // Fail the build only after reports and artifacts were created
                    if (env.TEST_STATUS != "0") {
                        error("Tests failed. Reports were generated successfully. Marking build as FAILED.")
                    }
                }
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
            echo 'Automation tests failed. Please check Jenkins reports and artifacts.'
        }
    }
}