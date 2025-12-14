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
                            checkout scm
                        }
                    }

                    stage('Run Tests') {
                        steps {
                            sh """
                                set -eu
                                mkdir -p reports
                                python -m pip install -r requirements-dev.txt
                                if [ "${PYTHON_VERSION}" = "3.12" ]; then
                                    echo "Running ruff + mypy + coverage (only on Python ${PYTHON_VERSION})"
                                    python -m ruff check . --output-format junit --output-file reports/ruff-${PYTHON_VERSION}.xml
                                    python -m mypy calculator
                                    python -m pytest \\
                                        --junitxml=reports/pytest-${PYTHON_VERSION}.xml \\
                                        --junit-prefix=py${PYTHON_VERSION} \\
                                        -o junit_suite_name=pytest-py${PYTHON_VERSION} \\
                                        --cov \\
                                        --cov-report=xml:reports/coverage.xml \\
                                        --cov-fail-under=85 \\
                                        -v tests/
                                else
                                    echo "Running pytest only (Python ${PYTHON_VERSION})"
                                    python -m pytest \\
                                    --junitxml=reports/pytest-${PYTHON_VERSION}.xml \\
                                    --junit-prefix=py${PYTHON_VERSION} \\
                                    -o junit_suite_name=pytest-py${PYTHON_VERSION} \\
                                    -v tests/
                                fi
                            """
                        }
                    }
                }
                post {
                    always {
                        junit "reports/pytest-${PYTHON_VERSION}.xml"
                        script {
                            if (env.PYTHON_VERSION == '3.12') {
                                junit "reports/ruff-${PYTHON_VERSION}.xml"
                                
                                recordCoverage(
                                    tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']],
                                    sourceCodeRetention: 'LAST_BUILD',
                                    failNoReports: true
                                )
                            }
                        }
                    }
                }
            }
        }

        stage('Build & Push Docker Image') {
            when {
                branch 'main'
            }
            agent { label 'docker' }
            steps {
                checkout scm

                script {
                    def shaTag = "sha-${env.GIT_COMMIT.take(7)}"
                    def branchBuild = "${env.BRANCH_NAME}-b${env.BUILD_NUMBER}"
                    def latestTag = 'latest'

                    def imageRef = "${env.DOCKER_IMAGE}:${shaTag}"
                    def img = docker.build(imageRef)

                    sh """
                        set -eu
                        out=\$(docker run --rm ${imageRef})
                        echo "\$out"
                        echo "\$out" | grep -F "2 + 3 = 5"
                    """

                    docker.withRegistry('', 'dockerhub-creds') {
                        img.push(shaTag)
                        img.push(branchBuild)
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
