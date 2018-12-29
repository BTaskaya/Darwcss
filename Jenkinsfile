pipeline {
    agent { docker { image 'python:3.7.1' } }
    stages {
        stage('prepare') {
            steps {
                sh 'python -m venv .venv'
                sh """. .venv/bin/activate 
                    pip install pytest twine
                    pip install -e ."""
            }
        }
        stage('test') {
            steps {
                sh """. .venv/bin/activate
                    pytest --junit-xml=test_results.xml tests/
                   """
            }
        }
        stage('build') {
            steps {
                sh """. .venv/bin/activate
                    python setup.py sdist
                   """
            }
        }
        stage('deploy_pypi') {
            environment {
                PYPI = credentials('local-pypi')
                PYPI_HOST = 'https://pypi.kernel.live'
            }
            steps {
                sh """. .venv/bin/activate
                    twine upload -u $PYPI_USR -p $PYPI_PSW --repository-url $PYPI_HOST dist/*
                   """
            }
        }
        stage('deploy_docs') {
            environment {
                RTD = credentials('rtd-endpoint')
                TOKEN = credentials('rtd-token')
            }
            steps {
                sh 'curl -X POST -d branches=master -d token=$TOKEN https://$RTD'
            }
        }
    }
    post {
        always {
            junit 'test_results.xml'
        }
    }
}
