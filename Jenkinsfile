pipeline {
    agent none

    environment {
        DOCKER_IMAGE = 'galhalevi/calculator'
        PIP_DISABLE_PIP_VERSION_CHECK=1
    }

    options {
        disableConcurrentBuilds()
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
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
                                export PIP_CACHE_DIR="$PWD/.pip-cache"
                                mkdir -p "$PIP_CACHE_DIR"
                                rm -rf .venv-${PYTHON_VERSION}
                                python -m venv .venv-${PYTHON_VERSION}
                                . .venv-${PYTHON_VERSION}/bin/activate
                                python -m pip install -U pip
                                python -m pip install -r requirements-dev.txt
                                if [ "${PYTHON_VERSION}" = "3.12" ]; then
                                    echo "Running ruff + mypy + coverage (only on Python ${PYTHON_VERSION})"
                                    python -m ruff check . --output-format junit --output-file reports/ruff-${PYTHON_VERSION}.xml
                                    python -m mypy calculator

                                    # Override coverage gating during pytest so reports are published;
                                    # enforce fail_under via `coverage report` (from .coveragerc) after.
                                    python -m pytest \\
                                        --junitxml=reports/pytest-${PYTHON_VERSION}.xml \\
                                        --junit-prefix=py${PYTHON_VERSION} \\
                                        -o junit_suite_name=pytest-py${PYTHON_VERSION} \\
                                        --cov \\
                                        --cov-report=xml:reports/coverage.xml \\
                                        --cov-fail-under=0 \\
                                        -v tests/
                                    python -m coverage report --show-missing
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
                        archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true, fingerprint: true

                        script {
                            if (env.PYTHON_VERSION == '3.12') {
                                junit "reports/ruff-${PYTHON_VERSION}.xml"
                                
                                recordCoverage(
                                    tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']],
                                    sourceCodeRetention: 'LAST_BUILD',
                                    enabledForFailure: true
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

            environment {
                CACHE_REF = "${DOCKER_IMAGE}:buildcache"
            }

            steps {
                checkout scm

                script {
                    def shaTag = "sha-${env.GIT_COMMIT.take(7)}"
                    def branchBuild = "${env.BRANCH_NAME}-b${env.BUILD_NUMBER}"
                    def latestTag = 'latest'

                    def imageRef = "${env.DOCKER_IMAGE}:${shaTag}"

                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
                        sh """
                            set -eu

                            echo "\$DH_TOKEN" | docker login -u "\$DH_USER" --password-stdin
                            
                            # Ensure we have a buildx builder on THIS node/daemon
                            docker buildx create --name jx --driver docker-container --use 2>/dev/null || docker buildx use jx
                            docker buildx inspect --bootstrap

                            # Build + push image, while importing/exporting cache via registry
                            docker buildx build \\
                                --pull \\
                                --cache-from type=registry,ref=${env.CACHE_REF} \\
                                --cache-to   type=registry,ref=${env.CACHE_REF},mode=max \\
                                -t ${env.DOCKER_IMAGE}:${shaTag} \\
                                -t ${env.DOCKER_IMAGE}:${branchBuild} \\
                                -t ${env.DOCKER_IMAGE}:${latestTag} \\
                                --push \\
                                .
                            
                            out=\$(docker run --rm ${imageRef} add 2 3)
                            echo "\$out"
                            echo "\$out" | grep -F "5.0"
                        """
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
