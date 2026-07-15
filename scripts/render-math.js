// scripts/render-math.js — 用 MathJax 预渲染 HTML 中的公式为 SVG
const { mathjax } = require('mathjax-full/js/mathjax.js');
const { TeX } = require('mathjax-full/js/input/tex.js');
const { SVG } = require('mathjax-full/js/output/svg.js');
const { liteAdaptor } = require('mathjax-full/js/adaptors/liteAdaptor.js');
const { RegisterHTMLHandler } = require('mathjax-full/js/handlers/html.js');
const { AllPackages } = require('mathjax-full/js/input/tex/AllPackages.js');
const fs = require('fs');
const path = require('path');

const htmlFile = process.argv[2] || path.join(__dirname, '..', 'index.html');
let html = fs.readFileSync(htmlFile, 'utf8');

// 初始化 MathJax
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({ packages: AllPackages });
const svg = new SVG({ fontCache: 'none' });
const mj = mathjax.document(html, { InputJax: tex, OutputJax: svg });

// 渲染所有公式
mj.render();

// 收集渲染结果
const body = mj.document.body;
let result = adaptor.outerHTML(body);

// 去掉 body 标签
result = result.replace(/^<body>/, '').replace(/<\/body>$/, '');

// 保持 head 不动，只替换 body
const headEnd = html.indexOf('</head>');
const bodyStart = html.indexOf('<body>');
const bodyEnd = html.lastIndexOf('</body>');

const before = html.substring(0, bodyStart + '<body>'.length);
const after = html.substring(bodyEnd);

const output = before + result + after;
fs.writeFileSync(htmlFile, output, 'utf8');
console.log('[math] 公式预渲染完成');
