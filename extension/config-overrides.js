const path = require('path');

module.exports = function override(config, env) {
  config.entry = {
    main: path.join(__dirname, 'src/popup/index.tsx'),
    background: path.join(__dirname, 'src/background/index.ts'),
    content: path.join(__dirname, 'src/content/index.ts'),
  };
  config.output.filename = 'static/js/[name].js';
  return config;
};