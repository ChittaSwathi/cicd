pipeline {
    agent any
    
    stages {
        stage('Prepare') {
            steps {
                // Give execution permission to the shell script
                sh 'chmod +x hello_world.sh'
            }
        }
        
        stage('Build') {
            steps {
                // Run the script
                sh './hello_world.sh'
            }
        }
        
        stage('Deploy') {
            steps {
                // Mock deployment step
                echo 'Deploying application (mock step)...'
            }
        }
    }
}
