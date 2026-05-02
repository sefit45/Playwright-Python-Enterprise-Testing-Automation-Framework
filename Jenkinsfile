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
        USE_DOCKER = "true"
    }

    stages {

        stage('01 - Checkout') {
            steps {
                checkout scm
            }
        }

        stage('02 - Clean') {
            steps {
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

        stage('03 - Try Docker Execution') {
            steps {
                script {
                    try {
                        echo "Building Docker image..."

                        bat "docker build -t qa-framework ."

                        echo "Running tests inside Docker..."

                        def exitCode = bat(
                            script: "docker run --rm qa-framework",
                            returnStatus: true
                        )

                        env.TEST_EXIT_CODE = "${exitCode}"

                        echo "Docker execution finished with exit code: ${env.TEST_EXIT_CODE}"

                    } catch (Exception e) {
                        echo "Docker failed, switching to fallback venv execution"
                        env.USE_DOCKER = "false"
                    }
                }
            }
        }

        stage('04 - Fallback Venv Execution') {
            when {
                expression { env.USE_DOCKER == "false" }
            }
            steps {
                script {
                    echo "Running fallback using local venv..."

                    bat "\"${env.PYTHON}\" -m pip install --upgrade pip"
                    bat "\"${env.PIP}\" install -r requirements.txt"
                    bat "\"${env.PLAYWRIGHT}\" install"

                    def exitCode = bat(
                        script: "\"${env.PYTEST}\" -n auto -m \"${params.TEST_SUITE} and not demo\" --env=${params.ENV} --alluredir=allure-results",
                        returnStatus: true
                    )

                    env.TEST_EXIT_CODE = "${exitCode}"

                    echo "Fallback execution exit code: ${env.TEST_EXIT_CODE}"
                }
            }
        }

        stage('05 - Add Allure Info') {
            steps {
                bat """
                echo Environment=${params.ENV}> allure-results\\environment.properties
                echo Test_Suite=${params.TEST_SUITE}>> allure-results\\environment.properties
                echo Executor=Jenkins>> allure-results\\environment.properties
                echo Build_Number=%BUILD_NUMBER%>> allure-results\\environment.properties
                echo Job_Name=%JOB_NAME%>> allure-results\\environment.properties
                echo Build_URL=%BUILD_URL%>> allure-results\\environment.properties
                """
            }
        }

        stage('06 - Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('07 - Archive') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'logs/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'screenshots/**', allowEmptyArchive: true
            }
        }

        stage('08 - Final Status') {
            steps {
                script {
                    if (env.TEST_EXIT_CODE != "0") {
                        error("Tests failed")
                    } else {
                        echo "All tests passed successfully"
                    }
                }
            }
        }
    }
}