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

                    echo "Pytest exit code: ${exitCode}"

                    if (exitCode != 0) {
                        error("Tests failed")
                    }
                }
            }
        }

        stage('04 - Add Allure Environment Info') {
            steps {
                script {
                    bat """
                    if not exist allure-results mkdir allure-results

                    echo Environment=${params.ENV}> allure-results\\environment.properties
                    echo Test_Suite=${params.TEST_SUITE}>> allure-results\\environment.properties
                    echo Executor=Jenkins>> allure-results\\environment.properties
                    echo Build_Number=%BUILD_NUMBER%>> allure-results\\environment.properties
                    echo Job_Name=%JOB_NAME%>> allure-results\\environment.properties
                    echo Build_URL=%BUILD_URL%>> allure-results\\environment.properties
                    echo Git_Branch=%GIT_BRANCH%>> allure-results\\environment.properties
                    echo Git_Commit=%GIT_COMMIT%>> allure-results\\environment.properties
                    """
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
    }

    post {
        always {
            echo 'Pipeline finished.'
        }

        success {
            echo 'SUCCESS - Clean execution'
        }

        failure {
            echo 'FAILURE - Tests or pipeline failed'
        }
    }
}