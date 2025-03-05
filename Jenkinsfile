pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/doras1976/pytest_framework.git'
            }
        }

        stage('Set Up Environment') {
            steps {
                withCredentials([string(credentialsId: 'aws-codeartifact-token', variable: 'AWS_TOKEN')]) {
                    sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        pip config set global.index-url https://aws:$AWS_TOKEN@dev-code-artifacts-098885917934.d.codeartifact.us-east-1.amazonaws.com/pypi/devCodeRepo/simple/
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run API Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    export PYTHONPATH=$PYTHONPATH:$(pwd)  # Ensure Python finds schemas
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
