pipeline {
    agent {
        docker {
            image 'python:3.12'
            label 'docker'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        DOCKER_IMAGE = 'galhalevi/calculator'
    }   

    stages {
        stage('Checkout code') {
            steps {
                git branch: 'level2', url: 'https://github.com/gal-halevi/learning-jenkins.git'
            }
        }
        stage('Install dependencies') {
            steps {
                sh "python3 -m pip install -r requirements.txt"
            }
        }
        stage('Run Tests') {
            steps {
                sh """
                mkdir -p reports
                python3 -m pytest --junitxml=reports/results.xml -v tests/
                """
            }
            post {
                always {
                    junit "reports/results.xml"
                }
            }
        }

        stage('Build & Push Docker Image') {
            agent { label 'docker' }
            steps {
                script {
                    if (!env.GIT_COMMIT) {
                        error("Missing GIT_COMMIT — cannot tag Docker image.")
                    }
                    if (!env.BUILD_NUMBER) {
                        error("Missing BUILD_NUMBER — cannot tag Docker image.")
                    } 
                    def shortCommit = env.GIT_COMMIT.take(7)
                    def buildTag = env.BUILD_NUMBER
                    def latestTag = 'latest'

                    echo "Using commit tag=${shortCommit}, build tag=${buildTag}"

                    def img = docker.build("${DOCKER_IMAGE}:${shortCommit}")

                    docker.withRegistry('', 'dockerhub-creds') {
                        img.push(shortCommit)
                        img.push(buildTag)
                        img.push(latestTag)
                    }    
                }
            }
        }

        stage('Archive app') {
            steps {
                archiveArtifacts artifacts: '*.py', fingerprint: true, followSymlinks: false
            }
        }
    }
    post {
        success {
            echo "Build succeeded 🎉"
        }
        failure {
            echo "Build failed ❌"
        }
    }
}
