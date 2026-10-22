pipeline {
    agent any

    environment {
        AWS_REGION     = 'ap-south-1'
        AWS_ACCOUNT_ID = '082706807472'
        ECR_REPO       = 'upiwhere'
        REGISTRY       = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG      = "v${BUILD_NUMBER}"
        IMAGE          = "${REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
        KUBECONFIG     = '/var/lib/jenkins/.kube/config'
    }

    triggers { pollSCM('H/2 * * * *') }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build & Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt pytest httpx
                    python -m compileall -q backend
                    pytest -q tests
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE} -t ${REGISTRY}/${ECR_REPO}:latest .'
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    aws ecr describe-repositories --repository-names ${ECR_REPO} --region ${AWS_REGION} >/dev/null 2>&1 || \
                      aws ecr create-repository --repository-name ${ECR_REPO} --region ${AWS_REGION}
                    aws ecr get-login-password --region ${AWS_REGION} | \
                      docker login --username AWS --password-stdin ${REGISTRY}
                    docker push ${IMAGE}
                    docker push ${REGISTRY}/${ECR_REPO}:latest
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl create secret docker-registry ecr-secret \
                      --docker-server=${REGISTRY} --docker-username=AWS \
                      --docker-password="$(aws ecr get-login-password --region ${AWS_REGION})" \
                      --dry-run=client -o yaml | kubectl apply -f -
                    sed "s|IMAGE_PLACEHOLDER|${IMAGE}|" k8s/deployment.yaml | kubectl apply -f -
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/upiwhere-app --timeout=180s
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                kubectl get pods -o wide
                kubectl get deployment upiwhere-app
                kubectl get svc upiwhere-svc
                kubectl port-forward svc/upiwhere-svc 18081:80 > /tmp/pf.log 2>&1 &
                PF=$!
                trap 'kill $PF' EXIT
                sleep 6
                curl -sf http://localhost:18081/ | head -n 5
                '''
            }
        }
        
        stage('Scale Deployment') {
            steps {
                sh '''
                echo "Scaling upiwhere-app deployment to 4 replicas..."
                kubectl scale deployment upiwhere-app --replicas=4
                
                echo "Waiting for the new pods to roll out..."
                kubectl rollout status deployment/upiwhere-app --timeout=180s
                
                echo "Verifying scaled pod count:"
                kubectl get pods -o wide
                kubectl get deployment upiwhere-app
                '''
            }
        }
    }

    post {
        success { echo "Deployed ${IMAGE}" }
        failure { echo 'Pipeline failed: check the stage logs' }
    }
}
