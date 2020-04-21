module.exports = {
  publicPath: '/static/',
  outputDir: '../app/public',
  assetsDir: '../static',

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: true
    }
  }
}
