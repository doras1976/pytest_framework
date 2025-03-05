pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/doras1976/pytest_framework'
            }
        }

        stage('Set Up Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest --html=reports/test_report.html --self-contained-html
                '''
            }
        }

        stage('Publish Test Report') {
            steps {
                publishHTML (target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'test_report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
}
