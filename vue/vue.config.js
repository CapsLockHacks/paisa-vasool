module.exports = {
  'transpileDependencies': [
    'vuetify'
  ],
  devServer: {
    port: 7000,
    proxy: {
      "^/api": {
        // target: "http://172.16.26.116:6969"
        target: "https://paisavasool.mrkaran.dev"
      }
    }
  },
}
