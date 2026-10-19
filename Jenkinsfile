
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'muhammadaryas/simple-app-jenkins'
        REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat 'echo Mulai build aplikasi'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
            }
        }

        stage('Deploy App + Database') {
            steps {
                bat 'docker compose down'
                bat 'docker compose up -d --build'
                bat 'ping -n 20 127.0.0.1 > nul'
            }
        }

        stage('Verify') {
            steps {
                bat 'curl http://localhost:5000/'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: REGISTRY_CREDENTIALS,
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )
                ]) {
                    bat 'echo %PASS%| docker login -u %USER% --password-stdin'
                    bat 'docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest'
                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker push %IMAGE_NAME%:latest'
                }
            }
        }
    }
}
