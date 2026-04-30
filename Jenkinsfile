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

                    echo "ALL PARAMS: ${params}"

                    // 🔥 Normalize
                    def envInput = params.ENV.toString().trim().toLowerCase()
                    def suiteInput = params.TEST_SUITE.toString().trim().toLowerCase()

                    echo "ENV INPUT = ${envInput}"
                    echo "SUITE INPUT = ${suiteInput}"

                    // 🔥 MAP BASED (NO IF AT ALL)
                    def envMap = [
                        "st" : "st",
                        "uat": "uat",
                        "prod": "prod"
                    ]

                    def suiteMap = [
                        "regression tests" : "regression",
                        "progression tests": "regression",
                        "apis tests"      : "api",
                        "db tests"        : "db",
                        "ui tests"        : "ui",
                        "sanity tests"    : "sanity"
                    ]

                    def resolvedEnv = envMap.get(envInput, "dev")
                    def resolvedMarker = suiteMap.get(suiteInput, "smoke")

                    env.SELECTED_ENV = resolvedEnv
                    env.SELECTED_MARKER = resolvedMarker

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
                        unstable("Tests failed but reports were generated.")
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
    }
}