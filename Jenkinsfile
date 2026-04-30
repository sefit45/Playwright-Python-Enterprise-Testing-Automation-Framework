// =========================================================
// Jenkins Pipeline
// Playwright Python Enterprise Testing Automation Framework
// =========================================================
//
// Main capabilities:
// - GitHub checkout
// - Dynamic environment selection
// - Dynamic test suite selection
// - Clean parameter mapping using Maps
// - Dependency installation
// - Playwright browser installation
// - Parallel pytest execution
// - Allure report generation
// - HTML report archiving
// - Raw Allure results archiving
// - Delayed test result evaluation
//
// =========================================================

pipeline {

    // Run pipeline on any available Jenkins agent
    agent any

    // Global environment variables for local Windows Jenkins execution
    environment {

        // Python virtual environment executables
        PYTHON = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\python.exe"
        PIP = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pip.exe"
        PYTEST = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pytest.exe"
        PLAYWRIGHT = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\playwright.exe"

        // Default values used during pipeline execution
        SELECTED_ENV = "dev"
        SELECTED_MARKER = "smoke"
        TEST_STATUS = "0"
    }

    stages {

        stage('01 - Checkout Source Code') {
            steps {

                // Pull latest code from GitHub repository
                checkout scm
            }
        }

        stage('02 - Install Dependencies') {
            steps {

                // Print current stage information
                echo 'Installing Python dependencies and Playwright browsers...'

                // Upgrade pip package manager
                bat "\"%PYTHON%\" -m pip install --upgrade pip"

                // Install project dependencies from requirements.txt
                bat "\"%PIP%\" install -r requirements.txt"

                // Install Playwright supported browsers
                bat "\"%PLAYWRIGHT%\" install"
            }
        }

        stage('03 - Resolve Execution Parameters') {
            steps {
                script {

                    // Map Jenkins environment selection to framework environment value
                    def envMap = [
                        'Dev'      : 'dev',
                        'ST'       : 'qa',
                        'UAT'      : 'qa',
                        'PROD-Like': 'prod',
                        'PROD'     : 'prod'
                    ]

                    // Map Jenkins test suite selection to pytest marker
                    def suiteMap = [
                        'Minimal Connectivity Tests - MCT': 'smoke',
                        'Sanity Tests'                   : 'sanity',
                        'Progression Tests'              : 'regression',
                        'Regression Tests'               : 'regression',
                        'APIs Tests'                     : 'api',
                        'DB Tests'                       : 'db',
                        'UI Tests'                       : 'ui'
                    ]

                    // Resolve selected environment with safe default value
                    env.SELECTED_ENV = envMap[params.ENV] ?: 'dev'

                    // Resolve selected test marker with safe default value
                    env.SELECTED_MARKER = suiteMap[params.TEST_SUITE] ?: 'smoke'

                    // Print selected execution configuration
                    echo "Selected Jenkins ENV parameter: ${params.ENV}"
                    echo "Selected Jenkins TEST_SUITE parameter: ${params.TEST_SUITE}"
                    echo "Resolved framework environment: ${env.SELECTED_ENV}"
                    echo "Resolved pytest marker: ${env.SELECTED_MARKER}"
                }
            }
        }

        stage('04 - Execute Tests') {
            steps {
                script {

                    // Print test execution command details
                    echo "Executing tests with marker: ${env.SELECTED_MARKER}"
                    echo "Executing tests on environment: ${env.SELECTED_ENV}"

                    // Run pytest with parallel execution and capture exit code
                    // returnStatus: true allows report generation stages to continue even if tests fail
                    def exitCode = bat(
                        script: "\"%PYTEST%\" -n auto -m %SELECTED_MARKER% --env=%SELECTED_ENV% --alluredir=allure-results",
                        returnStatus: true
                    )

                    // Save pytest exit code for final evaluation stage
                    env.TEST_STATUS = exitCode.toString()

                    // Print pytest result status
                    echo "Pytest exit code: ${env.TEST_STATUS}"
                }
            }
        }

        stage('05 - Generate Allure Report') {
            steps {

                // Publish Allure report inside Jenkins
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('06 - Archive Reports And Artifacts') {
            steps {

                // Archive pytest HTML report
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

                // Archive raw Allure results
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }

        stage('07 - Evaluate Test Results') {
            steps {
                script {

                    // Mark build as UNSTABLE when tests fail
                    // Reports are already generated before this stage
                    if (env.TEST_STATUS != "0") {
                        unstable("Tests failed. Reports were generated successfully. Marking build as UNSTABLE.")
                    } else {
                        echo "All selected tests passed successfully."
                    }
                }
            }
        }
    }

    post {

        always {

            // Always print final pipeline status
            echo 'Pipeline execution completed.'
        }

        success {

            // Success message when all stages and tests passed
            echo 'Automation pipeline completed successfully.'
        }

        unstable {

            // Unstable message when tests failed but reports were generated
            echo 'Automation pipeline completed with test failures. Please review Allure and HTML reports.'
        }

        failure {

            // Failure message for infrastructure or pipeline failures
            echo 'Automation pipeline failed due to infrastructure or execution issue.'
        }
    }
}