pipeline {

    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'st', 'uat', 'prod'], description: 'Select environment')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'sanity', 'regression', 'api', 'db', 'ui'], description: 'Select test suite')
    }

    environment {
        PYTHON = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\python.exe"
        PIP = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pip.exe"
        PYTEST = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pytest.exe"
        PLAYWRIGHT = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\playwright.exe"

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

        stage('03 - Execute Tests') {
            steps {
                script {
                    echo "Running with ENV=${params.ENV} MARKER=${params.TEST_SUITE}"

                    def exitCode = bat(
                        script: "\"${env.PYTEST}\" -n auto -m \"${params.TEST_SUITE} and not demo\" --env=${params.ENV} --alluredir=allure-results",
                        returnStatus: true
                    )

                    env.TEST_STATUS = exitCode.toString()
                    echo "Pytest exit code: ${env.TEST_STATUS}"
                }
            }
        }

        stage('04 - Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('05 - Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }

        stage('06 - Evaluate Test Results') {
            steps {
                script {
                    if (env.TEST_STATUS != "0") {
                        error("Tests failed. Reports were generated successfully.")
                    } else {
                        currentBuild.result = 'SUCCESS'
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

        failure {
            echo 'Automation pipeline failed.'
        }
    }
}