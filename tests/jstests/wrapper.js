module.exports = require('babel-jest').default.createTransformer({
  presets: [
    "@babel/preset-env",
    "@babel/preset-react"
  ],
  plugins: [
    [
      "@babel/plugin-transform-runtime",
      { "regenerator": true }
    ]
  ]
});
