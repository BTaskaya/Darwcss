pipeline {
    agent { docker { image 'python:3.7.1' } }
    environment {
        WEBHOOK_DISCORD = credentials('discord-webhook-1')
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
        success {
            sh """
                curl -H "Content-Type: application/json" \
                -X POST \
                -d '{"content":"abc","embed":{"title":"Jenkins build ","description":"Your ${env.BUILD_NUMBER}th ${currentBuild.fullDisplayName} [build](${env.BUILD_URL}) on ${BRANCH_NAME} resulted with Success","url":"${env.BUILD_URL}","color":65347,"thumbnail":{"url":"https://jenkins.io/images/logos/san-diego/san-diego.png"},"image":{"url":"https://cdn1.iconfinder.com/data/icons/basic-ui-icon-rounded-colored/512/icon-41-512.png"},"author":{"name":"Jenkins build node ${NODE_NAME}","url":"https://ci.kernel.live","icon_url":"https://wiki.jenkins.io/download/attachments/2916393/logo.png?version=1&modificationDate=1302753947000&api=v2"}}}' $WEBHOOK_DISCORD
               """
        }
        unstable {
            sh """
                curl -H "Content-Type: application/json" \
                -X POST \
                -d '{"content":"abc","embed":{"title":"Jenkins build ","description":"Your ${env.BUILD_NUMBER}th ${currentBuild.fullDisplayName} [build](${env.BUILD_URL}) on ${BRANCH_NAME} resulted with Success","url":"${env.BUILD_URL}","color":16752128,"thumbnail":{"url":"https://jenkins.io/images/logos/san-diego/san-diego.png"},"image":{"url":"https://cdn1.iconfinder.com/data/icons/map-objects/154/map-object-warning-attention-point-512.png"},"author":{"name":"Jenkins build node ${NODE_NAME}","url":"https://ci.kernel.live","icon_url":"https://wiki.jenkins.io/download/attachments/2916393/logo.png?version=1&modificationDate=1302753947000&api=v2"}}}' $WEBHOOK_DISCORD
               """
        }
        failure {
            sh """
                curl -H "Content-Type: application/json" \
                -X POST \
                -d '{"content":"abc","embed":{"title":"Jenkins build ","description":"Your ${env.BUILD_NUMBER}th ${currentBuild.fullDisplayName} [build](${env.BUILD_URL}) on ${BRANCH_NAME} resulted with Success","url":"${env.BUILD_URL}","color":16711680,"thumbnail":{"url":"https://jenkins.io/images/logos/san-diego/san-diego.png"},"image":{"url":"https://cdn4.iconfinder.com/data/icons/unigrid-flat-basic/90/019_023_link_chain_broken_disconnect_2-512.png"},"author":{"name":"Jenkins build node ${NODE_NAME}","url":"https://ci.kernel.live","icon_url":"https://wiki.jenkins.io/download/attachments/2916393/logo.png?version=1&modificationDate=1302753947000&api=v2"}}}' $WEBHOOK_DISCORD
               """
        }
    }
}
