pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                // Clone the repository
                git 'https://github.com/qianqia3/SDA-UserManagement.git'
            }
        }

        stage('Install dependencies') {
            steps {
                // Install Python dependencies
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // Run SonarQube scan
                withSonarQubeEnv('MySonarQubeServer') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                // Check SonarQube quality gate
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            // Archive test results and code coverage reports
            junit 'tests/reports/*.xml'
            archiveArtifacts artifacts: '**/target/*.xml', allowEmptyArchive: true
        }
        failure {
            mail to: 'your-email@example.com',
                 subject: "Build Failed: ${env.JOB_NAME}",
                 body: "Build ${env.BUILD_NUMBER} failed. Please check Jenkins for more details."
        }
    }
}
