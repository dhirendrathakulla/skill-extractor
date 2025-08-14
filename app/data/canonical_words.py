canonical_map = {
    # Programming Languages (extended)
    'python': 'python',
    'py': 'python',
    'python3': 'python',
    'javascript': 'javascript',
    'js': 'javascript',
    'typescript': 'typescript',
    'ts': 'typescript',
    'java': 'java',
    'jdk': 'java',
    'c': 'c',
    'c++': 'cpp',
    'cpp': 'cpp',
    'c#': 'c#',
    'csharp': 'c#',
    'ruby': 'ruby',
    'rb': 'ruby',
    'php': 'php',
    'swift': 'swift',
    'scala': 'scala',
    'perl': 'perl',
    'r': 'r',
    'matlab': 'matlab',
    'go': 'go',
    'golang': 'go',
    'rust': 'rust',
    'kotlin': 'kotlin',
    'dart': 'dart',
    'elixir': 'elixir',
    'haskell': 'haskell',
    'lua': 'lua',
    'groovy': 'groovy',
    'objectivec': 'objective-c',
    'objective-c': 'objective-c',
    'shell': 'bash',
    'bash': 'bash',
    'powershell': 'powershell',
    'zsh': 'zsh',
    'fish shell': 'fish',
    'typescript jsx': 'tsx',
    'tsx': 'tsx',
    'jsx': 'jsx',

    # Databases - SQL (extended)
    'sql': 'sql',
    'mysql': 'mysql',
    'postgresql': 'postgresql',
    'postgres': 'postgresql',
    'pg': 'postgresql',              # common alias
    'pgvector': 'pgvector',          # PostgreSQL extension for vector search
    'sqlite': 'sqlite',
    'mariadb': 'mariadb',
    'oracle': 'oracle',
    'db2': 'db2',
    'sqlserver': 'sqlserver',
    'mssql': 'sqlserver',
    'redshift': 'redshift',
    'bigquery': 'bigquery',
    'snowflake': 'snowflake',

    # Databases - NoSQL (extended)
    'nosql': 'nosql',
    'mongodb': 'mongodb',
    'mongo': 'mongodb',
    'mongo db': 'mongodb',
    'mongo-db': 'mongodb',
    'mongodb atlas': 'mongodb',
    'cassandra': 'cassandra',
    'redis': 'redis',
    'dynamodb': 'dynamodb',
    'couchdb': 'couchdb',
    'neo4j': 'neo4j',
    'elasticsearch': 'elasticsearch',
    'arangodb': 'arangodb',
    'firebase': 'firebase',
    'cosmosdb': 'cosmosdb',
    'hazelcast': 'hazelcast',

    # Web Frameworks - Backend (extended)
    'django': 'django',
    'flask': 'flask',
    'spring': 'spring',
    'springboot': 'spring',
    'laravel': 'laravel',
    'express': 'express',
    'expressjs': 'express',
    'express.js': 'express',
    'ruby on rails': 'rails',
    'rails': 'rails',
    'fastapi': 'fastapi',
    'aspnet': 'asp.net',
    'asp.net': 'asp.net',
    'symfony': 'symfony',
    'cakephp': 'cakephp',
    'playframework': 'play framework',
    'play framework': 'play framework',
    'gin': 'gin',
    'echo': 'echo',
    'micronaut': 'micronaut',
    'koa': 'koa',
    'vertx': 'vertx',

    # Frontend frameworks and libraries (extended)
    'react': 'react',
    'reactjs': 'react',
    'react.js': 'react',
    'angular': 'angular',
    'angularjs': 'angular',
    'vue': 'vue',
    'vuejs': 'vue',
    'vue.js': 'vue',
    'svelte': 'svelte',
    'ember': 'ember',
    'backbone': 'backbone',
    'jquery': 'jquery',
    'polymer': 'polymer',
    'preact': 'preact',
    'alpinejs': 'alpinejs',

    # Frontend languages / specs (extended)
    'html': 'html',
    'html5': 'html',
    'css': 'css',
    'css3': 'css',
    'sass': 'sass',
    'scss': 'sass',
    'less': 'less',
    'stylus': 'stylus',
    'postcss': 'postcss',

    # Mobile frameworks (extended)
    'react native': 'react native',
    'reactnative': 'react native',
    'flutter': 'flutter',
    'ionic': 'ionic',
    'xamarin': 'xamarin',
    'cordova': 'cordova',
    'nativeScript': 'nativescript',
    'nativescript': 'nativescript',

    # DevOps & Cloud (extended)
    'docker': 'docker',
    'kubernetes': 'kubernetes',
    'k8s': 'kubernetes',
    
      # Amazon DynamoDB
    'amazon dynamodb': 'dynamodb',
    'dynamodb': 'dynamodb',

    # Amazon Elastic Compute Cloud EC2
    'amazon elastic compute cloud ec2': 'ec2',
    'elastic compute cloud': 'ec2',
    'amazon ec2': 'ec2',
    'ec2': 'ec2',

    # Amazon Redshift
    'amazon redshift': 'redshift',
    'redshift': 'redshift',

    # Amazon Web Services AWS software
    'amazon web services aws software': 'aws',
    'amazon web services': 'aws',
    'aws software': 'aws',
    'amazonwebservices': 'aws',
    'aws': 'aws',
    'amazon web service': 'aws',
     'amazon s3': 's3',
    's3': 's3',
    'amazon cloudfront': 'cloudfront',
    'cloudfront': 'cloudfront',
    'amazon lambda': 'aws lambda',
    'lambda': 'aws lambda',
    'amazon rds': 'rds',
    'rds': 'rds',
    'amazon vpc': 'vpc',
    'vpc': 'vpc',
    'eks': 'eks',
    'elastic kubernetes service': 'eks',
# Azure
    'azure cloud': 'azure',
    'microsoft azure': 'azure',
    'azure': 'azure',
    'azure vm': 'azure vm',
    'azure functions': 'azure functions',
    'azure storage': 'azure storage',

    # Google Cloud
    'google cloud': 'gcp',
    'google cloud platform': 'gcp',
    'gcp': 'gcp',
    'google compute engine': 'gce',
    'gce': 'gce',
    'google kubernetes engine': 'gke',
    'gke': 'gke',
    'azure': 'azure',
    'googlecloudplatform': 'gcp',
    
    'openstack': 'openstack',
    'digitalocean': 'digitalocean',
    'linode': 'linode',
    'oracle cloud': 'oracle cloud',
    'ibm cloud': 'ibm cloud',
    'vmware cloud': 'vmware cloud',
    'terraform': 'terraform',
    'ansible': 'ansible',
    'chef': 'chef',
    'puppet': 'puppet',
    'jenkins': 'jenkins',
    'gitlabci': 'gitlab ci',
    'gitlab ci': 'gitlab ci',
    'circleci': 'circleci',
    'travisci': 'travis ci',
    'travis ci': 'travis ci',
    'teamcity': 'teamcity',
    'bamboo': 'bamboo',
    'argo': 'argo',
    'argo cd': 'argo cd',

    # CI/CD tools (extended)
    'github actions': 'github actions',
    'bitbucket pipelines': 'bitbucket pipelines',
    'azure devops': 'azure devops',

    # Container orchestration (extended)
    'openshift': 'openshift',
    'rancher': 'rancher',
    'mesos': 'mesos',
    'nomad': 'nomad',

    # Operating Systems (extended)
    'linux': 'linux',
    'ubuntu': 'ubuntu',
    'debian': 'debian',
    'fedora': 'fedora',
    'centos': 'centos',
    'windows': 'windows',
    'win': 'windows',
    'macos': 'macos',
    'osx': 'macos',
    'unix': 'unix',
    'redhat': 'redhat',
    'archlinux': 'archlinux',

    # Machine Learning / Data Science (extended)
    'tensorflow': 'tensorflow',
    'pytorch': 'pytorch',
    'scikit-learn': 'scikit-learn',
    'scikitlearn': 'scikit-learn',
    'keras': 'keras',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'xgboost': 'xgboost',
    'lightgbm': 'lightgbm',
    'opencv': 'opencv',
    'fastai': 'fastai',
    'catboost': 'catboost',
    'huggingface': 'huggingface',
    'spaCy': 'spacy',
    'spacy': 'spacy',
    'nltk': 'nltk',

    # Big Data (extended)
    'hadoop': 'hadoop',
    'spark': 'spark',
    'apache spark': 'spark',
    'apache hadoop': 'hadoop',
    'hive': 'hive',
    'pig': 'pig',
    'presto': 'presto',
    'flink': 'flink',
    'kinesis': 'kinesis',

    # Message Brokers (extended)
    'kafka': 'kafka',
    'rabbitmq': 'rabbitmq',
    'activemq': 'activemq',
    'mqtt': 'mqtt',
    'zeromq': 'zeromq',
    'nsq': 'nsq',

    # Testing frameworks (extended)
    'junit': 'junit',
    'pytest': 'pytest',
    'mocha': 'mocha',
    'jest': 'jest',
    'selenium': 'selenium',
    'cypress': 'cypress',
    'karma': 'karma',
    'jasmine': 'jasmine',
    'enzyme': 'enzyme',

    # Version control (extended)
    'git': 'git',
    'svn': 'svn',
    'subversion': 'svn',
    'mercurial': 'mercurial',
    'hg': 'mercurial',

    # Editors / IDEs (optional, extended)
    'vscode': 'vscode',
    'visual studio code': 'vscode',
    'intellij': 'intellij',
    'eclipse': 'eclipse',
    'pycharm': 'pycharm',
    'android studio': 'android studio',
    'netbeans': 'netbeans',
    'sublime': 'sublime text',
    'sublime text': 'sublime text',
    'atom': 'atom',

    # Miscellaneous tools (extended)
    'postman': 'postman',
    'jira': 'jira',
    'confluence': 'confluence',
    'slack': 'slack',
    'new relic': 'new relic',
    'datadog': 'datadog',
    'splunk': 'splunk',
    'prometheus': 'prometheus',
    'grafana': 'grafana',
    'cloudwatch': 'cloudwatch',
    'cloud': 'cloud infrastructure',
    'elasticstack': 'elastic stack',
    'elastic stack': 'elastic stack',

    # More databases (extended)
    'timescaledb': 'timescaledb',
    'influxdb': 'influxdb',
    'cockroachdb': 'cockroachdb',
    'druid': 'druid',

    # Languages / Platforms (extended)
    'powershellcore': 'powershell',
    'powershell': 'powershell',
    'flutter': 'flutter',
    'reactnative': 'react native',
    'react native': 'react native',
    'xamarin': 'xamarin',
    'cordova': 'cordova',
    'electron': 'electron',

    # API / Protocols
    'grpc': 'grpc',
    'g rpc': 'grpc',
    'g-rpc': 'grpc',

    'graphql': 'graphql',
    'graph ql': 'graphql',
    'graph-ql': 'graphql',

    'rest': 'rest',
    'restapi': 'rest',
    'rest api': 'rest',
    'rest-api': 'rest',
    'restfull': 'rest',       # common misspelling
    'restful': 'rest',

    'soap': 'soap',
    's oap': 'soap',

    'websocket': 'websocket',
    'web socket': 'websocket',
    'web-socket': 'websocket',
    'websockets': 'websocket',
    'web sockets': 'websocket',
    'web-sockets': 'websocket',

    # Additional
    'apachebeam': 'apache beam',
    'apache beam': 'apache beam',

    # Container tools
    'helm': 'helm',
    'vault': 'vault',

    # Monitoring & Logging
    'prometheus': 'prometheus',
    'grafana': 'grafana',

    # Cloudformation and Infrastructure as Code
    'cloudformation': 'cloudformation',
    'pulumi': 'pulumi',
      # General cloud terms
    'cloud': 'cloud infrastructure',
    'cloud computing': 'cloud infrastructure',
    'cloud platform': 'cloud infrastructure',
    'cloud services': 'cloud infrastructure',
    'cloud solutions': 'cloud infrastructure',
    'multi cloud': 'multi-cloud',
    'hybrid cloud': 'hybrid cloud',

    # Misc common skills
    'oauth': 'oauth',
    'openid': 'openid',
    'jwt': 'jwt',

      # JS Runtimes
    'node': 'nodejs',
    'node.js': 'nodejs',
    'nodejs': 'nodejs',
    'deno': 'deno',
    'deno.js': 'deno',

    # JS Package Managers / Bundlers
    'npm': 'npm',
    'yarn': 'yarn',
    'pnpm': 'pnpm',
    'webpack': 'webpack',
    'rollup': 'rollup',
    'parcel': 'parcel',

    # JS Testing Libraries
    'jest': 'jest',
    'mocha': 'mocha',
    'chai': 'chai',
    'enzyme': 'enzyme',
    'cypress': 'cypress',

    # JS Frameworks / Libraries (frontend mostly covered, adding server-side & others)
    'nextjs': 'next.js',
    'next.js': 'next.js',
    'nuxt': 'nuxt.js',
    'nuxt.js': 'nuxt.js',
    'gatsby': 'gatsby',
    'electron': 'electron',
    'threejs': 'three.js',
    'three.js': 'three.js',

    # JS ML / NLP Libraries
    'tensorflow.js': 'tensorflow.js',
    'tfjs': 'tensorflow.js',
    'brain.js': 'brain.js',
    'onnxruntime': 'onnxruntime',
    'onnxruntime.js': 'onnxruntime',
    'huggingface.js': 'huggingface.js',
    'transformers.js': 'transformers.js',
    'nlp.js': 'nlp.js',
    'compromise': 'compromise',

    # Vector databases relevant to JS ecosystem
    'pinecone': 'pinecone',
    'weaviate': 'weaviate',
    'vespa': 'vespa',
    'milvus': 'milvus',
    'faiss': 'faiss',

    # JS-related utilities/tools
    'eslint': 'eslint',
    'prettier': 'prettier',
    'babel': 'babel',

    # Hugging Face ecosystem (JS bindings & tools)
    'huggingface': 'huggingface',
    'huggingface transformers': 'huggingface',
    'huggingface.js': 'huggingface.js',
    'transformers.js': 'transformers.js',

       # Python ORMs
    'sqlalchemy': 'sqlalchemy',
    'django orm': 'django orm',
    'peewee': 'peewee',
    'pony orm': 'pony orm',
    'tortoise orm': 'tortoise orm',
    'pony': 'pony orm',
    'tortoise': 'tortoise orm',

    # Java ORMs
    'hibernate': 'hibernate',
    'mybatis': 'mybatis',
    'eclipse link': 'eclipse link',
    'eclipselink': 'eclipse link',
    'toplink': 'toplink',
    'jpa': 'jpa',
    'jakarta persistence api': 'jpa',

    # JavaScript / Node.js ORMs
    'sequelize': 'sequelize',
    'typeorm': 'typeorm',
    'objection': 'objection',
    'prisma': 'prisma',
    'mikro-orm': 'mikro-orm',
    'mikro orm': 'mikro-orm',

    # PHP ORMs
    'doctrine': 'doctrine',
    'eloquent': 'eloquent',
    'propel': 'propel',

    # Ruby ORMs
    'activerecord': 'activerecord',
    'active record': 'activerecord',
    'sequel': 'sequel',

    # C# ORMs
    'entity framework': 'entity framework',
    'ef core': 'entity framework',
    'nhibernate': 'nhibernate',
    'dapper': 'dapper',

    # Go ORMs
    'gorm': 'gorm',
    'ent': 'ent',
    'xorm': 'xorm',
    'beego orm': 'beego orm',
    'pop': 'pop',

    # Kotlin ORMs
    'exposed': 'exposed',

    # Swift ORMs
    'vapor fluent': 'vapor fluent',
    'fluent': 'vapor fluent',

    # Scala ORMs
    'slick': 'slick',

    # Elixir ORMs
    'ecto': 'ecto',

     # Full stack variations
    "fullstack": "full stack",
    "full-stack": "full stack",
    "full stack": "full stack",
    "fullstackdeveloper": "full stack",
    "fullstack developer": "full stack",
    "full stack developer": "full stack",
    "full-stack developer": "full stack",
   ' full-stack development': "full stack",
}
