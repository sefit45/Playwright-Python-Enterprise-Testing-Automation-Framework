stage('03 - Resolve Execution Parameters') {
    steps {
        script {

            // Normalize input (trim spaces + enforce exact match)
            def envInput = params.ENV?.trim()
            def suiteInput = params.TEST_SUITE?.trim()

            echo "Raw ENV input: '${envInput}'"
            echo "Raw TEST_SUITE input: '${suiteInput}'"

            // Environment mapping
            def envMap = [
                'Dev'      : 'dev',
                'ST'       : 'qa',
                'UAT'      : 'qa',
                'PROD-Like': 'prod',
                'PROD'     : 'prod'
            ]

            // Test suite mapping
            def suiteMap = [
                'Minimal Connectivity Tests - MCT': 'smoke',
                'Sanity Tests'                   : 'sanity',
                'Progression Tests'             : 'regression',
                'Regression Tests'              : 'regression',
                'APIs Tests'                    : 'api',
                'DB Tests'                      : 'db',
                'UI Tests'                      : 'ui'
            ]

            // Apply mapping safely
            env.SELECTED_ENV = envMap[envInput] ?: 'dev'
            env.SELECTED_MARKER = suiteMap[suiteInput] ?: 'smoke'

            // Debug logs
            echo "Selected Jenkins ENV parameter: ${envInput}"
            echo "Selected Jenkins TEST_SUITE parameter: ${suiteInput}"
            echo "Resolved framework environment: ${env.SELECTED_ENV}"
            echo "Resolved pytest marker: ${env.SELECTED_MARKER}"
        }
    }
}