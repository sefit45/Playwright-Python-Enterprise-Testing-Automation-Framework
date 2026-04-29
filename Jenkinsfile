pipeline {

    agent any

    environment {
        PYTHON = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\python.exe"
        PIP    = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pip.exe"
        PYTEST = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pytest.exe"
        PLAYWRIGHT = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\playwright.exe"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "\"%PYTHON%\" -m pip install --upgrade pip"
                bat "\"%PIP%\" install -r requirements.txt"
                bat "\"%PLAYWRIGHT%\" install"
            }
        }

        stage('Run Tests') {
            steps {
                bat "\"%PYTEST%\" -m smoke --env=dev --alluredir=allure-results"
            }
        }

        // 🔥 זה השלב החדש
        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }

        stage('Archive HTML Report') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Tests passed.'
        }
        failure {
            echo 'Tests failed.'
        }
    }
}