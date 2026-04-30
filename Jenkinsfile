pipeline {

    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'st', 'uat', 'prod'], description: 'Environment')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'sanity', 'regression', 'api', 'db', 'ui'], description: 'Test suite')
    }

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

                bat "\"${env.PYTHON}\" -m pip install --upgrade pip"
                bat "\"${env.PIP}\" install -r requirements.txt"
                bat "\"${env.PLAYWRIGHT}\" install"
            }
        }

        stage('03 - Resolve Execution Parameters') {
            steps {
                script {

                    def envInput = params.ENV.toString().trim().toLowerCase()
                    def suiteInput = params.TEST_SUITE.toString().trim().toLowerCase()

                    env.SELECTED_ENV = envInput
                    env.SELECTED_MARKER = suiteInput

                    echo "Resolved ENV: ${env.SELECTED_ENV}"
                    echo "Resolved MARKER: ${env.SELECTED_MARKER}"
                }
            }
        }

        stage('04 - Execute Tests') {
            steps {
                script {

                    echo "Running with ENV=${env.SELECTED_ENV} MARKER=${env.SELECTED_MARKER}"

                    def exitCode = bat(
                        script: "\"${env.PYTEST}\" -n auto -m \"${env.SELECTED_MARKER} and not demo\" --env=${env.SELECTED_ENV} --alluredir=allure-results",
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
                        error("Tests failed - failing pipeline")
                    } else {
                        echo "All tests passed successfully"
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

        failure {
            echo 'Pipeline failed due to test or infrastructure issues.'
        }
    }
}