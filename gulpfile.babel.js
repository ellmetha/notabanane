import "core-js/stable";
import "regenerator-runtime/runtime";

import gulp from 'gulp';
import env from 'gulp-env';
import mjml from 'gulp-mjml';
import log from 'fancy-log';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import minimist from "minimist";
import path from 'path';
import PluginError from 'plugin-error';
import webpack from 'webpack';
import WebpackDevServer from 'webpack-dev-server';


/* Global variables */
const rootDir = `${__dirname}/`;
const staticDir = `${rootDir}main/static/`;
const templatesDir = `${rootDir}main/templates/`;
const PROD_ENV = minimist(process.argv.slice(2)).production;
const WEBPACK_DEV_SERVER_PORT = (
  process.env.WEBPACK_DEV_SERVER_PORT ? process.env.WEBPACK_DEV_SERVER_PORT : 8080);
env.set({ NODE_ENV: PROD_ENV ? 'production' : 'debug' });

/* Directories */
const buildDir = PROD_ENV ? `${staticDir}build` : `${staticDir}build_dev`;
const sassDir = `${staticDir}sass`;
const jsDir = `${staticDir}js`;


/*
 * Global webpack config
 * ~~~~~~~~~~~~~~~~~~~~~
 */

const webpackConfig = {
  mode: PROD_ENV ? 'production' : 'development',
  entry: {
    App: [`${jsDir}/App.jsx`, `${sassDir}/App.scss`],
    WagtailAdminOverrides: [`${sassDir}/WagtailAdminOverrides.scss`],
  },
  output: {
    filename: 'js/[name].js',
    path: buildDir,
    publicPath: PROD_ENV ? '/s5/' : '/static/',
  },
  resolve: {
    modules: ['node_modules'],
    extensions: ['.webpack.js', '.web.js', '.js', '.jsx', '.json', 'scss'],
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        resolve: {
          extensions: ['.js', '.jsx'],
        },
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
            ],
            plugins: [
              [
                '@babel/plugin-transform-runtime',
                { regenerator: true }
              ]
            ],
          },
        },
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },
      { test: /\.txt$/, use: 'raw-loader' },
      {
        test: /\.(png|jpg|jpeg|gif|svg|woff|woff2)([\?]?.*)$/,
        type: 'asset/resource'
      },
      { test: /\.(eot|ttf|wav|mp3|otf)([\?]?.*)$/, type: 'asset/resource' },
    ],
  },
  optimization: {
    minimize: PROD_ENV,
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: 'css/[name].css' }),
    ...(PROD_ENV ? [
      new webpack.LoaderOptionsPlugin({
        minimize: true,
      }),
    ] : []),
  ],
};


/*
 * Webpack task
 * ~~~~~~~~~~~~
 */

/* Task to build our JS and CSS applications. */
gulp.task('build-webpack-assets', gulp.series(() => (
  new Promise((resolve, reject) => {
    // eslint-disable-next-line consistent-return
    webpack(webpackConfig, (err, stats) => {
      if (err) {
        return reject(err);
      }
      if (stats.hasErrors()) {
        return reject(new Error(stats.compilation.errors.join('\n')));
      }
      console.log(stats.toString({
        chunks: false,
        colors: true,
      }));
      resolve();
    });
  })
)));


/*
 * Other tasks
 * ~~~~~~~~~~~
 */

/* Task to build our MJML templates. */
gulp.task('build-mjml-templates', gulp.series(() => (
  gulp.src(`${staticDir}/mjml/**/*.mjml`)
    .pipe(mjml())
    .pipe(gulp.dest(`${templatesDir}/emails/`))
)));

/* Task to move images to the build folder. */
gulp.task('build-images', gulp.series(() => (
  gulp.src(`${staticDir}/img/**/*`)
    .pipe(gulp.dest(`${buildDir}/img/`))
)));


/*
 * Global tasks
 * ~~~~~~~~~~~~
 */

gulp.task('build', gulp.series(['build-webpack-assets', 'build-mjml-templates', 'build-images']));


/*
 * Development tasks
 * ~~~~~~~~~~~~~~~~~
 */

gulp.task('webpack-dev-server', gulp.series(() => {
  const devWebpackConfig = Object.create(webpackConfig);
  devWebpackConfig.mode = 'development';
  devWebpackConfig.devtool = 'eval';
  devWebpackConfig.devServer = { hot: true };
  devWebpackConfig.entry = {
    App: [
      `${jsDir}/App.jsx`, `${sassDir}/App.scss`,
      `webpack-dev-server/client?http://localhost:${WEBPACK_DEV_SERVER_PORT}`,
      'webpack/hot/only-dev-server',
    ],
  };
  devWebpackConfig.module = {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        resolve: {
          extensions: ['.js', '.jsx'],
        },
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
            ],
            plugins: [
              [
                '@babel/plugin-transform-runtime',
                { regenerator: true }
              ]
            ],
          },
        },
      },
      { test: /\.scss$/, use: ['style-loader', 'css-loader', 'sass-loader'] },
      { test: /\.txt$/, use: 'raw-loader' },
      { test: /\.(png|jpg|jpeg|gif|svg|woff|woff2)([\?]?.*)$/, type: 'asset/inline' },
      { test: /\.(eot|ttf|wav|mp3|otf)([\?]?.*)$/, type: 'asset/resource' },
    ],
  };
  devWebpackConfig.output = {
    path: path.resolve(__dirname, staticDir),
    publicPath: `http://localhost:${WEBPACK_DEV_SERVER_PORT}/static/`,
    filename: 'js/[name].js',
  };
  devWebpackConfig.plugins = [
    new webpack.LoaderOptionsPlugin({ debug: true }),
    new webpack.HotModuleReplacementPlugin(),
  ];

  // Start a webpack-dev-server
  new WebpackDevServer(webpack(devWebpackConfig), {
    static: {
      directory: path.resolve(__dirname, staticDir, '..'),
      publicPath: '/static/',
    },
    headers: { 'Access-Control-Allow-Origin': '*' },
    hot: true,
  }).listen(WEBPACK_DEV_SERVER_PORT, 'localhost', (err) => {
    if (err) throw new PluginError('webpack-dev-server', err);
    log(
      '[webpack-dev-server]',
      `http://localhost:${WEBPACK_DEV_SERVER_PORT}/webpack-dev-server/`,
    );
  });
}));
