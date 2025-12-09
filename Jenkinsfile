pipeline {
    agent {
        docker {
            image 'python:3.12'
            label 'docker'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

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
