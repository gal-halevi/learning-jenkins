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
        stage('Test in Python container') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    label 'docker'
                }
            }
            steps {
                git branch: 'level2', url: 'https://github.com/gal-halevi/learning-jenkins.git'

                sh "python3 -m pip install -r requirements-dev.txt"
                sh "mkdir -p reports"
                sh "python3 -m ruff check . --output-format junit --output-file reports/ruff.xml"
                sh "python3 -m pytest --junitxml=reports/pytest.xml -v tests/"
                stash name: 'src', includes: '''
                *.py, 
                Dockerfile
                '''
            }
            post {
                always {
                    junit "reports/ruff.xml"
                    junit "reports/pytest.xml"
                }
            }
        }

        stage('Build & Push Docker Image') {
            agent { label 'docker' }
            steps {
                unstash 'src'
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

        stage('Archive app') {
            agent { label 'docker' }
            steps {
                unstash 'src'
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
