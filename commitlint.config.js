// for more information on config options:
// https://commitlint.js.org/#/reference-configuration

module.exports = {
    // Resolve and load @commitlint/config-conventional from node_modules
    extends: ['@commitlint/config-conventional'],
    // Resolve and load @commitlint/format from node_modules
    formatter: '@commitlint/format',
    // Custom URL to show upon failure
    helpUrl: 'https://www.conventionalcommits.org/en/v1.0.0/',
    // Override the @commitlint/config-conventional rules 
    // to escalate warnings into errors
    rules: {
        'body-leading-blank': [2, 'always'],
        'footer-leading-blank': [2, 'always']
    }
};
