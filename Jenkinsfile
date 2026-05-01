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
        TEST_EXIT_CODE = "0"
    }

    stages {

        stage('01 - Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('02 - Clean Previous Results') {
            steps {
                echo 'Cleaning previous reports and execution artifacts...'
                bat """
                if exist allure-results rmdir /s /q allure-results
                if exist report.html del /q report.html
                if exist logs rmdir /s /q logs
                if exist screenshots rmdir /s /q screenshots

                mkdir allure-results
                mkdir logs
                mkdir screenshots
                """
            }
        }

        stage('03 - Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat "\"${env.PYTHON}\" -m pip install --upgrade pip"
                bat "\"${env.PIP}\" install -r requirements.txt"
                bat "\"${env.PLAYWRIGHT}\" install"
            }
        }

        stage('04 - Execute Tests') {
            steps {
                script {
                    echo "Running tests with ENV=${params.ENV} and TEST_SUITE=${params.TEST_SUITE}"

                    def exitCode = bat(
                        script: "\"${env.PYTEST}\" -n auto -m \"${params.TEST_SUITE} and not demo\" --env=${params.ENV} --alluredir=allure-results",
                        returnStatus: true
                    )

                    env.TEST_EXIT_CODE = "${exitCode}"

                    echo "Pytest exit code: ${env.TEST_EXIT_CODE}"
                }
            }
        }

        stage('05 - Add Allure Environment Info') {
            steps {
                echo 'Adding environment details to Allure report...'
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

        stage('06 - Publish Allure Report') {
            steps {
                echo 'Publishing Allure report...'
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('07 - Archive Reports And Logs') {
            steps {
                echo 'Archiving reports, logs and screenshots...'
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'logs/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'screenshots/**', allowEmptyArchive: true
            }
        }

        stage('08 - Final Build Status') {
            steps {
                script {
                    if (env.TEST_EXIT_CODE != "0") {
                        error("Tests failed. Build marked as FAILURE after reports were generated and archived.")
                    } else {
                        echo "All tests passed successfully."
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
            echo 'SUCCESS - Clean execution'
        }

        failure {
            echo 'FAILURE - Tests or pipeline failed'
        }
    }
}