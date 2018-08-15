import babel from 'rollup-plugin-babel';
import resolve from 'rollup-plugin-node-resolve';
import json from 'rollup-plugin-json';
import replace from 'rollup-plugin-replace'

export default {
    input: 'js_files/index.js',
    indent: '\t',
    plugins: [
        json(),
        resolve({
            jsnext: true,
            browser: true,
            module: true,
        }),
        babel({
            exclude: 'node_modules/**',
        }),
        replace({
          'process.env.NODE_ENV': JSON.stringify('development'),
          'process.env.VUE_ENV': JSON.stringify('browser')
        }),
    ],
    output: [
        {
            format: 'umd',
            name: 'BRITECORE',
            file: 'risk_type/static/js/custom.js'
        }
    ],
};