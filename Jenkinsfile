// Jenkins Pipeline for Playwright Python Automation Framework
// Full version with explicit Python path for Windows Jenkins

pipeline {

    agent any

    environment {

        // Path to your local Python interpreter (from VS Code output)
        PYTHON = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\python.exe"
        PIP    = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pip.exe"
        PYTEST = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\pytest.exe"
        PLAYWRIGHT = "C:\\Users\\sefit\\playwright-python-framework\\venv\\Scripts\\playwright.exe"
    }

    stages {

        stage('Checkout Code') {
            steps {
                // Pull latest code from GitHub
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {

                // Upgrade pip
                bat "\"%PYTHON%\" -m pip install --upgrade pip"

                // Install requirements
                bat "\"%PIP%\" install -r requirements.txt"

                // Install Playwright browsers
                bat "\"%PLAYWRIGHT%\" install"
            }
        }

        stage('Run Smoke Tests') {
            steps {

                // Run tests with pytest
                bat "\"%PYTEST%\" -m smoke --env=dev --alluredir=allure-results"
            }
        }

        stage('Archive HTML Report') {
            steps {
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }

        stage('Archive Allure Results') {
            steps {
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }
    }

    post {

        always {
            echo 'Pipeline execution completed.'
        }

        success {
            echo 'Automation tests completed successfully.'
        }

        failure {
            echo 'Automation tests failed. Please check logs and reports.'
        }
    }
}