pipeline {
    agent any

    environment {
        IMAGE_NAME = "reyrox2005/campusvibe"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                docker push $IMAGE_NAME:$IMAGE_TAG

                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest

                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Update Helm Image Tag') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                    git config user.name "Jenkins"
                    git config user.email "jenkins@campusvibe.local"

                    sed -i "s/tag: \".*\"/tag: \\"${BUILD_NUMBER}\\"/" campusvibe/values.yaml

                    git add campusvibe/values.yaml

                    git commit -m "Update CampusVibe image tag to ${BUILD_NUMBER}" || true

                    git push https://${GIT_USER}:${GIT_TOKEN}@github.com/ReyRox2005/CampusVibe.git HEAD:main
                    '''
                }
            }
        }

    }

    post {
        success {
            echo "✅ Docker image built, pushed, and Helm image tag updated successfully!"
            echo "🚀 Argo CD will now detect the Git change and deploy the new image to EKS."
        }

        failure {
            echo "❌ Pipeline failed!"
        }

        always {
            sh 'docker logout || true'
        }
    }
}
