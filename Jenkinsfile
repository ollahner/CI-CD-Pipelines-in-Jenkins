pipeline {
    agent any

    environment {
        APP_NAME = 'hello-spencer'
        APP_PORT = '5556'
        IMAGE_NAME = "hello-spencer:${env.BUILD_NUMBER}"
    }

    stages {
        stage('Source') {
            steps {
                checkout scm
                sh 'git --no-pager log -1 --oneline'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t "$IMAGE_NAME" .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm "$IMAGE_NAME" python -m pytest tests/test_hello.py -v'
            }
        }

        stage('Deployment') {
            steps {
                sh '''
                    docker rm -f "$APP_NAME" || true
                    docker run -d \
                        --name "$APP_NAME" \
                        --restart unless-stopped \
                        -p "$APP_PORT:$APP_PORT" \
                        -e APP_PORT="$APP_PORT" \
                        "$IMAGE_NAME"
                '''
            }
        }

        stage('Integration Test') {
            steps {
                sh '''
                    for i in $(seq 1 15); do
                        if docker run --rm --network "container:$APP_NAME" "$IMAGE_NAME" \
                            python tests/test_api.py; then
                            exit 0
                        fi
                        sleep 2
                    done
                    docker logs "$APP_NAME"
                    exit 1
                '''
            }
        }
    }

    post {
        failure {
            sh 'docker logs "$APP_NAME" || true'
        }
        success {
            echo "Deployment is running on port ${APP_PORT} in Docker container ${APP_NAME}."
        }
    }
}
