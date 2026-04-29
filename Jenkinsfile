// Jenkins Pipeline for Playwright Python Automation Framework
// This pipeline installs dependencies, runs tests, and generates reports

pipeline {

    // Run pipeline on any available Jenkins agent
    agent any

    stages {

        // Stage 1: Checkout source code from GitHub
        stage('Checkout Code') {
            steps {

                // Pull latest code from connected Git repository
                checkout scm
            }
        }

        // Stage 2: Create Python virtual environment
        stage('Create Virtual Environment') {
            steps {

                // Create virtual environment for clean dependency isolation
                bat 'py -m venv venv'
            }
        }

        // Stage 3: Install dependencies
        stage('Install Dependencies') {
            steps {

                // Upgrade pip package manager
                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'

                // Install all project dependencies from requirements.txt
                bat 'venv\\Scripts\\pip.exe install -r requirements.txt'

                // Install Playwright browsers
                bat 'venv\\Scripts\\playwright.exe install'
            }
        }

        // Stage 4: Run smoke tests
        stage('Run Smoke Tests') {
            steps {

                // Run smoke tests with pytest
                bat 'venv\\Scripts\\pytest.exe -m smoke --env=dev --alluredir=allure-results'
            }
        }

        // Stage 5: Archive HTML report
        stage('Archive HTML Report') {
            steps {

                // Save HTML report as Jenkins build artifact
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }

        // Stage 6: Archive Allure results
        stage('Archive Allure Results') {
            steps {

                // Save Allure raw result files as Jenkins artifacts
                archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            }
        }
    }

    post {

        // Always run after pipeline completes
        always {

            // Print final pipeline status message
            echo 'Pipeline execution completed.'
        }

        // Run only if pipeline succeeds
        success {

            // Print success message
            echo 'Automation tests completed successfully.'
        }

        // Run only if pipeline fails
        failure {

            // Print failure message
            echo 'Automation tests failed. Please check logs and reports.'
        }
    }
}