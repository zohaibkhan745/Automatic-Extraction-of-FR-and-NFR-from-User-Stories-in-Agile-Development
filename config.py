"""
Configuration file for the FR/NFR Extraction System
"""

# Functional Requirement Keywords
FUNCTIONAL_KEYWORDS = [
    'create', 'add', 'delete', 'remove', 'update', 'edit', 'view', 'display',
    'show', 'list', 'search', 'filter', 'sort', 'calculate', 'generate',
    'send', 'receive', 'upload', 'download', 'save', 'load', 'export',
    'import', 'register', 'login', 'logout', 'authenticate', 'authorize',
    'submit', 'cancel', 'confirm', 'select', 'choose', 'enter', 'input',
    'output', 'print', 'scan', 'notify', 'alert', 'track', 'monitor',
    'process', 'execute', 'run', 'start', 'stop', 'pause', 'resume',
    'enable', 'disable', 'activate', 'deactivate', 'configure', 'set'
]

# Non-Functional Requirement Keywords
NON_FUNCTIONAL_KEYWORDS = [
    'secure', 'security', 'fast', 'performance', 'scalable', 'scalability',
    'reliable', 'reliability', 'available', 'availability', 'usable',
    'usability', 'maintainable', 'maintainability', 'portable', 'portability',
    'efficient', 'efficiency', 'responsive', 'response time', 'load time',
    'speed', 'quick', 'quickly', 'stable', 'stability', 'robust',
    'robustness', 'compatible', 'compatibility', 'accessible', 'accessibility',
    'user-friendly', 'intuitive', 'easy to use', 'simple', 'within',
    'milliseconds', 'seconds', 'minutes', 'concurrent', 'users',
    'throughput', 'latency', 'uptime', 'downtime', 'backup', 'recovery'
]

# NFR Categories (for advanced classification)
NFR_CATEGORIES = {
    'performance': ['fast', 'quick', 'speed', 'load', 'response time', 'milliseconds', 'seconds', 'performance'],
    'security': ['secure', 'security', 'encrypt', 'authentication', 'authorization', 'protected'],
    'usability': ['user-friendly', 'easy', 'simple', 'intuitive', 'usable', 'usability'],
    'reliability': ['reliable', 'available', 'uptime', 'stable', 'robust'],
    'scalability': ['scalable', 'concurrent', 'users', 'throughput'],
    'maintainability': ['maintainable', 'modular', 'documented'],
    'portability': ['portable', 'compatible', 'cross-platform']
}

# User Story Patterns
USER_STORY_PATTERNS = [
    r'as a (.*?), i want (.*?) so that (.*)',
    r'as a (.*?), i want (.*)',
    r'as an? (.*?), i (want|need|would like) (.*)',
    r'the (system|application|user|admin) (should|must|shall|will|can) (.*)',
    r'(system|application) (should|must|shall|will) (.*)',
]

# Requirement indicators
REQUIREMENT_INDICATORS = [
    'should', 'must', 'shall', 'will', 'can', 'need to', 'able to',
    'want to', 'would like to', 'require', 'required'
]

# Stopwords to be removed (will be supplemented by NLTK)
CUSTOM_STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves']
