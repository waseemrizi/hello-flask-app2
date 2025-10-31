pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'waseemrizi/hello-flask-app2'
        IMAGE_TAG = "${env.BUILD_NUMBER}"         // Each build gets its own tag
        KUBECONFIG = '/root/.kube/config'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/waseemrizi/hello-flask-app2.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$IMAGE_TAG .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $DOCKER_IMAGE:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy to K3s') {
            steps {
                sh '''
                echo "Deploying version $IMAGE_TAG to K3s..."
                kubectl set image deployment/hello-flask2 hello-flask2=$DOCKER_IMAGE:$IMAGE_TAG --record || kubectl apply -f k8s-deployment.yaml
                kubectl rollout status deployment/hello-flask2
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                echo "Verifying app response..."
                sleep 5
                curl -f http://172.16.12.38:30002 || (echo "❌ App verification failed" && exit 1)
                echo "✅ Deployment verified successfully!"
                '''
            }
        }
    }
}
