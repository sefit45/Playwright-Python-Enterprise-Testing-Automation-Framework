pipeline {

    agent any

    environment {
        PYTHON = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\python.exe"
        PIP = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pip.exe"
        PYTEST = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pytest.exe"
        PLAYWRIGHT = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\playwright.exe"

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

                // Install project dependencies and Playwright browsers
                echo 'Installing dependencies...'

                // Upgrade pip package manager
                bat "\"%PYTHON%\" -m pip install --upgrade pip"

                // Install dependencies from requirements.txt
                bat "\"%PIP%\" install -r requirements.txt"

                // Install Playwright supported browsers
                bat "\"%PLAYWRIGHT%\" install"
            }
        }

        stage('03 - Resolve Execution Parameters') {
            steps {
                script {

                    // Normalize Jenkins input values
                    // trim() removes hidden spaces
                    // toLowerCase() prevents case-sensitive mapping problems
                    def envInput = params.ENV?.trim().toLowerCase()
                    def suiteInput = params.TEST_SUITE?.trim().toLowerCase()

                    // Print raw normalized values for debugging
                    echo "Raw ENV input: '${envInput}'"
                    echo "Raw TEST_SUITE input: '${suiteInput}'"

                    // Map Jenkins environment choices to framework environment values
                    def envMap = [
                        'dev'      : 'dev',
                        'st'       : 'qa',
                        'uat'      : 'qa',
                        'prod-like': 'prod',
                        'prod'     : 'prod'
                    ]

                    // Map Jenkins test suite choices to pytest markers
                    def suiteMap = [
                        'minimal connectivity tests - mct': 'smoke',
                        'sanity tests'                   : 'sanity',
                        'progression tests'              : 'regression',
                        'regression tests'               : 'regression',
                        'apis tests'                     : 'api',
                        'db tests'                       : 'db',
                        'ui tests'                       : 'ui'
                    ]

                    // Resolve selected environment with safe fallback
                    env.SELECTED_ENV = envMap[envInput] ?: 'dev'

                    // Resolve selected pytest marker with safe fallback
                    env.SELECTED_MARKER = suiteMap[suiteInput] ?: 'smoke'

                    // Print final resolved execution configuration
                    echo "Resolved ENV: ${env.SELECTED_ENV}"
                    echo "Resolved MARKER: ${env.SELECTED_MARKER}"
                }
            }
        }

        stage('04 - Execute Tests') {
            steps {
                script {

                    // Run pytest in parallel mode
                    // -n auto enables pytest-xdist automatic worker selection
                    // "and not demo" excludes intentionally failing demo tests from CI
                    def exitCode = bat(
                        script: "\"%PYTEST%\" -n auto -m \"%SELECTED_MARKER% and not demo\" --env=%SELECTED_ENV% --alluredir=allure-results",
                        returnStatus: true
                    )

                    // Save pytest exit code for later evaluation
                    env.TEST_STATUS = exitCode.toString()

                    // Print pytest exit code
                    echo "Pytest exit code: ${env.TEST_STATUS}"
                }
            }
        }

        stage('05 - Allure Report') {
            steps {

                // Generate and publish Allure report inside Jenkins
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('06 - Archive Reports') {
            steps {

                // Archive pytest HTML report
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

                // Archive raw Allure result files
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }

        stage('07 - Evaluate Test Results') {
            steps {
                script {

                    // Mark build as unstable only after reports were generated
                    if (env.TEST_STATUS != "0") {
                        unstable("Tests failed but reports were generated successfully.")
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
            echo 'Pipeline finished.'
        }

        success {

            // Success message
            echo 'Automation pipeline completed successfully.'
        }

        unstable {

            // Unstable message when tests failed but reports were generated
            echo 'Automation pipeline completed with test failures. Please review Allure and HTML reports.'
        }

        failure {

            // Failure message for infrastructure or pipeline issues
            echo 'Automation pipeline failed due to infrastructure or Jenkins execution issue.'
        }
    }
}