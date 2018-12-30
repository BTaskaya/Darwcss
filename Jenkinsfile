pipeline {
    agent { docker { image 'python:3.7.1' } }
    stages {
        stage('prepare') {
            steps {
                sh 'python -m venv .venv'
                sh """. .venv/bin/activate
                    pip install pytest twine mypy flake8 mccabe flake8-junit-report
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
        stage('flake8') {
            steps {
                sh """. .venv/bin/activate
                    flake8 --max-complexity 7 --output-file --ignore E501 flake8_results.txt darwcss/ || true
                    [ -f flake8_results.txt ] && flake8_junit flake8_results.txt test_flake8.xml;rm flake8_results.txt || true
                   """
            }
        }
        stage('mypy') {
            steps {
                sh """. .venv/bin/activate
                    mypy --junit-xml=test_mypy.xml darwcss/
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
                LOCAL_PYPI = credentials('local-pypi')
                LOCAL_PYPI_HOST = 'https://pypi.kernel.live'
                GLOBAL_PYPI = credentials('global-pypi')
            }
            steps {
                sh """. .venv/bin/activate
                    twine upload -u $LOCAL_PYPI_USR -p $LOCAL_PYPI_PSW --repository-url $LOCAL_PYPI_HOST dist/*
                    twine upload -u $GLOBAL_PYPI_USR -p $GLOBAL_PYPI_PSW dist/* || true
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
            junit 'test_*.xml'
        }
    }
}
