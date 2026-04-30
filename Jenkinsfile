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
                checkout scm
            }
        }

        stage('02 - Install Dependencies') {
            steps {
                echo 'Installing dependencies...'

                bat "\"%PYTHON%\" -m pip install --upgrade pip"
                bat "\"%PIP%\" install -r requirements.txt"
                bat "\"%PLAYWRIGHT%\" install"
            }
        }

        stage('03 - Resolve Execution Parameters') {
            steps {
                script {

                    // Read Jenkins parameters safely
                    def rawEnv = params.ENV ?: params.environment ?: "dev"
                    def rawSuite = params.TEST_SUITE ?: params.'Test-Suite' ?: params.Test_Suite ?: "Minimal Connectivity Tests - MCT"

                    // Normalize values
                    def envInput = rawEnv.toString().trim().toLowerCase()
                    def suiteInput = rawSuite.toString().trim().toLowerCase()

                    echo "Raw ENV input: '${envInput}'"
                    echo "Raw TEST_SUITE input: '${suiteInput}'"

                    // Resolve environment
                    if (envInput == "dev") {
                        env.SELECTED_ENV = "dev"
                    } else if (envInput == "st") {
                        env.SELECTED_ENV = "qa"
                    } else if (envInput == "uat") {
                        env.SELECTED_ENV = "qa"
                    } else if (envInput == "prod-like") {
                        env.SELECTED_ENV = "prod"
                    } else if (envInput == "prod") {
                        env.SELECTED_ENV = "prod"
                    } else {
                        env.SELECTED_ENV = "dev"
                    }

                    // Resolve test suite marker
                    if (suiteInput.contains("mct") || suiteInput.contains("minimal connectivity")) {
                        env.SELECTED_MARKER = "smoke"
                    } else if (suiteInput.contains("sanity")) {
                        env.SELECTED_MARKER = "sanity"
                    } else if (suiteInput.contains("progression")) {
                        env.SELECTED_MARKER = "regression"
                    } else if (suiteInput.contains("regression")) {
                        env.SELECTED_MARKER = "regression"
                    } else if (suiteInput.contains("api")) {
                        env.SELECTED_MARKER = "api"
                    } else if (suiteInput.contains("db")) {
                        env.SELECTED_MARKER = "db"
                    } else if (suiteInput.contains("ui")) {
                        env.SELECTED_MARKER = "ui"
                    } else {
                        env.SELECTED_MARKER = "smoke"
                    }

                    echo "Resolved ENV: ${env.SELECTED_ENV}"
                    echo "Resolved MARKER: ${env.SELECTED_MARKER}"
                }
            }
        }

        stage('04 - Execute Tests') {
            steps {
                script {

                    def exitCode = bat(
                        script: "\"%PYTEST%\" -n auto -m \"%SELECTED_MARKER% and not demo\" --env=%SELECTED_ENV% --alluredir=allure-results",
                        returnStatus: true
                    )

                    env.TEST_STATUS = exitCode.toString()
                    echo "Pytest exit code: ${env.TEST_STATUS}"
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

        stage('06 - Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }

        stage('07 - Evaluate Test Results') {
            steps {
                script {
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
            echo 'Pipeline finished.'
        }

        success {
            echo 'Automation pipeline completed successfully.'
        }

        unstable {
            echo 'Automation pipeline completed with test failures. Please review Allure and HTML reports.'
        }

        failure {
            echo 'Automation pipeline failed due to infrastructure or Jenkins execution issue.'
        }
    }
}