module.exports = {
  /**
   * Application configuration section
   * http://pm2.keymetrics.io/docs/usage/application-declaration/
   */
  apps : [

    // First application
    {
      name      : 'gnews',
      exec_mode : 'fork',
      script    : "index.js",
      env: {
        PORT: 8087
      },
    }
  ]
};
