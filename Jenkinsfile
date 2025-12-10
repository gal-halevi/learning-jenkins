pipeline {
    agent none

    environment {
        DOCKER_IMAGE = 'galhalevi/calculator'
    }

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {
        stage('Python Compatibility Test') {
            matrix {
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '3.10', '3.11', '3.12'
                    }
                }
    
                agent {
                    docker {
                        image "python:${PYTHON_VERSION}-slim"
                        label 'docker'
                    }
                }
                stages {
                    stage('Checkout code') {
                        steps {
                            git branch: 'level3', url: 'https://github.com/gal-halevi/learning-jenkins.git'
                        }
                    }

                    stage('Run Tests') {
                        steps {
                            sh "mkdir -p reports"
                            sh "python -m pip install -r requirements-dev.txt"
                            sh "python -m ruff check . --output-format junit --output-file reports/ruff.xml"
                            sh "python -m pytest --junitxml=reports/pytest.xml -v tests/"
                        }
                    }
                }
                post {
                    always {
                        junit "reports/ruff.xml"
                        junit "reports/pytest.xml"
                    }
                }
            }
        }

        stage('Build & Push Docker Image') {
            when {
                branch 'level3'
            }
            agent { label 'docker' }
            steps {
                git branch: 'level3', url: 'https://github.com/gal-halevi/learning-jenkins.git'
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

                    def img = docker.build("${env.DOCKER_IMAGE}:${shortCommit}")

                    docker.withRegistry('', 'dockerhub-creds') {
                        img.push(shortCommit)
                        img.push(buildTag)
                        img.push(latestTag)
                    }    
                }
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
