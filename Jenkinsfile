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
                TWINE_REPOSITORY = 'https://pypi.kernel.live'
                PYPI = credentials('local-pypi')
            }
            steps {
                sh """. .venv/bin/activate
                    twine upload -u $PYPI_USR -p $PYPI_PSW dist/*
                   """
            }
        }
    }
    post {
        always {
            junit 'test_results.xml'
        }
    }
}
