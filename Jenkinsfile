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

                    // 🔥 IMPORTANT – match Jenkins EXACT parameter names
                    def rawEnv = params.ENV ?: "dev"
                    def rawSuite = params.'Test-Suite' ?: "Minimal Connectivity Tests - MCT"

                    def envInput = rawEnv.toString().trim().toLowerCase()
                    def suiteInput = rawSuite.toString().trim().toLowerCase()

                    echo "Raw ENV input: '${envInput}'"
                    echo "Raw TEST_SUITE input: '${suiteInput}'"

                    // ✅ ENV FIX
                    if (envInput.contains("st")) {
                        env.SELECTED_ENV = "st"
                    } else if (envInput.contains("uat")) {
                        env.SELECTED_ENV = "uat"
                    } else if (envInput.contains("prod")) {
                        env.SELECTED_ENV = "prod"
                    } else {
                        env.SELECTED_ENV = "dev"
                    }

                    // ✅ SUITE FIX
                    if (suiteInput.contains("regression")) {
                        env.SELECTED_MARKER = "regression"
                    } else if (suiteInput.contains("api")) {
                        env.SELECTED_MARKER = "api"
                    } else if (suiteInput.contains("db")) {
                        env.SELECTED_MARKER = "db"
                    } else if (suiteInput.contains("ui")) {
                        env.SELECTED_MARKER = "ui"
                    } else if (suiteInput.contains("sanity")) {
                        env.SELECTED_MARKER = "sanity"
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