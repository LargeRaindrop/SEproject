module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
    ? './'
    : '/',
    module:{
        rules: [
        {test: /\.vue$/,loader: "vue-loader"},
        {test: /\.css$/,use: ["vue-style-loader", "css-loader"]  }
        ]
    }
}
