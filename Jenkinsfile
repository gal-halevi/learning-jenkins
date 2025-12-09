pipeline {
    agent { label 'docker' }

    stages {
        stage('Checkout code') {
            steps {
                git branch: 'main', url: 'https://github.com/gal-halevi/learning-jenkins.git'
            }
        }
        stage('Install dependencies') {
            steps {
                sh "python3 -m pip install -r requirements.txt"
            }
        }
        stage('Run Tests') {
            steps {
                sh "python3 -m pytest --junitxml=reports/results.xml tests/"
            }
        }
        
        stage('Publish report') {
            steps {
                junit "reports/results.xml"
            }
        }
    }
}
