"use strict";
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) if (e.indexOf(p[i]) < 0)
            t[p[i]] = s[p[i]];
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
const component_compiler_utils_1 = require("@vue/component-compiler-utils");
const postcss_modules_sync_1 = require("postcss-modules-sync");
const postcss_clean_1 = require("./postcss-clean");
const hash = require("hash-sum");
const fs = require("fs");
const path = require("path");
const templateCompiler = require('vue-template-compiler');
class SFCCompiler {
    constructor(script, style, template, resolve = require.resolve) {
        this.template = template;
        this.style = style;
        this.script = script;
        this.resolve = resolve;
    }
    compileToDescriptor(filename, source) {
        const descriptor = component_compiler_utils_1.parse({
            source,
            filename,
            needMap: true,
            compiler: templateCompiler
        });
        const scopeId = 'data-v-' +
            (this.template.isProduction
                ? hash(path.basename(filename) + source)
                : hash(filename + source));
        const template = descriptor.template && this.compileTemplate(filename, descriptor.template);
        const styles = descriptor.styles.map(style => this.compileStyle(filename, scopeId, style));
        const { script: rawScript, customBlocks } = descriptor;
        const script = rawScript && {
            code: rawScript.src
                ? this.read(rawScript.src, filename)
                : rawScript.content,
            map: rawScript.map
        };
        return {
            scopeId,
            template,
            styles,
            script,
            customBlocks
        };
    }
    compileTemplate(filename, template) {
        const _a = this.template, { preprocessOptions } = _a, options = __rest(_a, ["preprocessOptions"]);
        const functional = 'functional' in template.attrs;
        return Object.assign({ functional }, component_compiler_utils_1.compileTemplate(Object.assign({}, options, { source: template.src
                ? this.read(template.src, filename)
                : template.content, filename, preprocessLang: template.lang, preprocessOptions: (template.lang &&
                preprocessOptions &&
                preprocessOptions[template.lang]) ||
                {}, isFunctional: functional })));
    }
    compileStyle(filename, scopeId, style) {
        let tokens = undefined;
        const needsCSSModules = style.module === true || typeof style.module === 'string';
        const postcssPlugins = [
            needsCSSModules
                ? postcss_modules_sync_1.default(Object.assign({ generateScopedName: '[path][local]-[hash:base64:4]' }, this.style.postcssModulesOptions, { getJSON: (t) => {
                        tokens = t;
                    } }))
                : undefined,
            this.template.isProduction
                ? postcss_clean_1.default(this.style.postcssCleanOptions)
                : undefined
        ]
            .concat(this.style.postcssPlugins)
            .filter(Boolean);
        const preprocessOptions = (style.lang &&
            this.style.preprocessOptions &&
            this.style.preprocessOptions[style.lang]) ||
            {};
        const source = style.src ? this.read(style.src, filename) : style.content;
        const result = component_compiler_utils_1.compileStyle({
            source: preprocessOptions.data ? `${preprocessOptions.data}\n${source}` : source,
            filename,
            id: scopeId,
            map: style.map,
            scoped: style.scoped || false,
            postcssPlugins,
            postcssOptions: this.style.postcssOptions,
            preprocessLang: style.lang,
            preprocessOptions,
            trim: this.style.trim
        });
        return Object.assign({ media: style.attrs.media, scoped: style.scoped, moduleName: style.module === true ? '$style' : style.module, module: tokens }, result, { code: result.code });
    }
    read(filename, context) {
        try {
            return fs
                .readFileSync(filename.startsWith('.')
                ? path.resolve(path.dirname(context), filename)
                : this.resolve(filename, { paths: [path.dirname(context)] }))
                .toString();
        }
        catch (e) {
            if (/cannot find module/i.test(e.message)) {
                throw Error(`Cannot find '${filename}' in '${context}'`);
            }
            throw e;
        }
    }
}
exports.SFCCompiler = SFCCompiler;
