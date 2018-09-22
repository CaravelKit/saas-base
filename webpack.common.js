const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
    entry: {
        auth: './app/components/auth/js/appAuth.js',
        dashboard: './app/components/dashboard/js/appDashboard.js',
        authStyles: './app/components/auth/js/authStyles.js',
        dashboardStyles: './app/components/dashboard/js/dashboardStyles.js'
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'static/js')
    },
    plugins: [
        new CleanWebpackPlugin(['static/js']), // <== This is Dist folder by fact
        new VueLoaderPlugin()
    ],
    resolve: {
        alias: {
          'vue$': 'vue/dist/vue.esm.js', // 'vue/dist/vue.common.js' for webpack 1
          '@app': path.resolve(__dirname, 'app')
        }
    },
    module: {
        rules: [
        {
            test: /.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
            use: [{
                loader: 'file-loader',
                options: {
                name: '[name].[ext]',
                outputPath: '../fonts/',    // where the fonts will go
                publicPath: '/static/fonts'       // override the default path
                }
            }]
        },
        {
            test: /\.css$/,
            use: [
                'style-loader',
                'css-loader',
                'sass-loader'
            ]
        },
        {
            test: /\.scss$/,
            use: [
                "style-loader", // creates style nodes from JS strings
                "css-loader", // translates CSS into CommonJS
                "sass-loader" // compiles Sass to CSS, using Node Sass by default
            ]
        },
        {
            test: /\.vue$/,
            use: 'vue-loader'
        }
    ]}
};