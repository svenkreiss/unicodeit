const path = require('path');

module.exports = {
  entry: './ts_src/replace.ts',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: [ '.tsx', '.ts', '.js' ],
  },
  output: {
    filename: 'unicodeit.js',
    path: path.resolve(__dirname, 'dist'),
  },
};
