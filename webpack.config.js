const path = require('path');

module.exports = {
  mode: 'development',
  entry: './ts_src/replace.ts',
  devtool: 'inline-source-map',
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
    path: path.resolve(__dirname, 'ts_dist'),
  },
};
