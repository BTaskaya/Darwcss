pipeline {
    agent { docker { image 'python:3.7.1' } }
    environment {
        GATEWAY = credentials('gateway_key')
    }
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
                    flake8 --max-complexity 7 --output-file --ignore E501 flake8_results.txt darwcss/
                    [ -f flake8_results.txt ] && flake8_junit flake8_results.txt test_flake8.xml;rm flake8_results.txt
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
            steps {
                sh """
                curl -XPOST -H 'Authorization: gateway: ${GATEWAY}' -H "Content-type: application/json" -d '{"name": "darwcss","branch": "${BRANCH_NAME}"}' 'https://gateway.kernel.live/poster/rtd'
                """
            }
        }
    }
    post {
        always {
            junit 'test_*.xml'
        }
        success {
            sh """
            curl -XPOST -H 'Authorization: gateway: ${GATEWAY}' -H "Content-type: application/json" -d '{"name": "darwcss-jenkins","b_status": "success","b_name": "${BUILD_DISPLAY_NAME}"}' 'https://gateway.kernel.live/poster/discord'
            curl -XPOST -H 'Authorization: gateway: ${GATEWAY}' -H "Content-type: application/json" -d '{"name": "darwcss-jenkins","b_status": "success","b_name": "${BUILD_DISPLAY_NAME}"}' 'https://gateway.kernel.live/poster/telegram'            
            """
        }
        unstable {
            sh """
            curl -XPOST -H 'Authorization: gateway: ${GATEWAY}' -H "Content-type: application/json" -d '{"name": "darwcss-jenkins","b_status": "unstable","b_name": "${BUILD_DISPLAY_NAME}"}' 'https://gateway.kernel.live/poster/discord'
            curl -XPOST -H 'Authorization: gateway: ${GATEWAY}' -H "Content-type: application/json" -d '{"name": "darwcss-jenkins","b_status": "unstable","b_name": "${BUILD_DISPLAY_NAME}"}' 'https://gateway.kernel.live/poster/telegram'            
            """
        }
        failure {
            sh """
            curl -XPOST -H 'Authorization: gateway: ${GATEWAY}' -H "Content-type: application/json" -d '{"name": "darwcss-jenkins","b_status": "fail","b_name": "${BUILD_DISPLAY_NAME}"}' 'https://gateway.kernel.live/poster/discord'
            curl -XPOST -H 'Authorization: gateway: ${GATEWAY}' -H "Content-type: application/json" -d '{"name": "darwcss-jenkins","b_status": "fail","b_name": "${BUILD_DISPLAY_NAME}"}' 'https://gateway.kernel.live/poster/telegram'            
            """        
        }
    }
}
