#!/usr/bin/env python3
"""
Configuration and constants for tech fingerprinting
"""

# Common paths to check
COMMON_PATHS = {
    '/wp-admin/': 'WordPress',
    '/administrator/': 'Joomla',
    '/admin/': 'Generic Admin Panel',
    '/phpmyadmin/': 'phpMyAdmin',
    '/.git/': 'Git Repository',
    '/.env': 'Environment File',
    '/api/': 'API Endpoint',
    '/graphql': 'GraphQL',
    '/swagger/': 'Swagger/OpenAPI',
    '/.svn/': 'SVN Repository',
    '/config/': 'Config Directory',
    '/backup/': 'Backup Directory'
}

# CDN detection headers
CDN_HEADERS = {
    'CF-RAY': 'Cloudflare',
    'X-Amz-Cf-Id': 'Amazon CloudFront',
    'X-Cache': 'Varnish/CDN',
    'X-Fastly-Request-ID': 'Fastly',
    'X-Azure-Ref': 'Azure CDN'
}

# Cookie technology indicators
COOKIE_INDICATORS = {
    'PHPSESSID': 'PHP',
    'JSESSIONID': 'Java/JSP',
    'ASP.NET_SessionId': 'ASP.NET',
    'laravel_session': 'Laravel',
    'django': 'Django',
    'express': 'Express.js',
    'connect.sid': 'Express.js',
    'rack.session': 'Ruby/Rack'
}

# JavaScript framework signatures
JS_FRAMEWORKS = {
    'react': ['react.js', 'react.min.js', 'React', '_reactRoot'],
    'angular': ['angular.js', 'angular.min.js', 'ng-', 'ng-app'],
    'vue': ['vue.js', 'vue.min.js', 'Vue', 'v-cloak'],
    'jquery': ['jquery', 'jQuery', '$.fn.jquery'],
    'nextjs': ['_next', '__NEXT_DATA__'],
    'nuxt': ['__NUXT__'],
    'svelte': ['__svelte']
}

# Security headers to check
SECURITY_HEADERS = [
    'Strict-Transport-Security',
    'Content-Security-Policy',
    'X-Frame-Options',
    'X-Content-Type-Options',
    'X-XSS-Protection',
    'Referrer-Policy',
    'Permissions-Policy'
]

# HTTP timeout settings
REQUEST_TIMEOUT = 10
PATH_CHECK_TIMEOUT = 5

# SSL/TLS settings
SSL_TIMEOUT = 5