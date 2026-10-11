# This module gives the demos for assignment 2.
# The classifier demo shows a flowchart with an input image, a model, and two results.
# The model gives one probability per class. The student moves the slider to change them.
# The demo uses HTML and JavaScript in an iframe.
# Because of this, the demo operates in JupyterLab, VS Code, and Colab.

import html
from IPython.display import HTML, display

# The page below is a template. Python replaces __P__ before you show the page.
_PAGE = """
<!doctype html><html><head><meta charset="utf-8"><style>
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:#3c4043}
 .row{display:flex;align-items:center;gap:12px;font-size:15px;padding:4px 0 8px 4px}
 input[type=range]{width:360px;accent-color:#2f6fed}
</style></head><body>
<div class="row"><label for="s">p(dog) = 1 &minus; p(cat):</label>
  <input id="s" type="range" min="0" max="1" step="0.01" value="__P__">
  <b id="v"></b></div>
<div id="fig"></div>
<div id="rule" class="row"></div>
<script>
const ACCENT="#2f6fed", GREY="#8a8f98";
function node(cx,cy,e,on){
  return `<g opacity="${on?1:0.4}"><rect x="${cx-48}" y="${cy-48}" width="96" height="96"
   rx="22" fill="${on?'#eef3ff':'#f7f7f8'}" stroke="${on?ACCENT:'#e4e5e9'}" stroke-width="2"/>
   <text x="${cx}" y="${cy+4}" font-size="46" text-anchor="middle"
   dominant-baseline="middle">${e}</text></g>`;
}
function label(cx,cy,t,on,w){
  return `<text x="${cx}" y="${cy}" font-size="15" font-weight="${w||600}"
   text-anchor="middle" fill="${on?ACCENT:GREY}">${t}</text>`;
}
function arrow(d,on){
  return `<path d="${d}" fill="none" stroke="${on?ACCENT:'#d8dade'}"
   stroke-width="${on?2.5:1.5}" marker-end="url(#${on?'a1':'a0'})"/>`;
}
function draw(p){
  const dog = p > 1 - p;
  document.getElementById("fig").innerHTML = `
  <svg viewBox="0 0 680 320" width="100%" style="max-width:680px">
  <defs>
   <marker id="a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
    orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="${ACCENT}"/></marker>
   <marker id="a0" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
    orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#d8dade"/></marker>
  </defs>
  ${arrow("M 132 150 L 196 150", true)}
  ${arrow("M 302 150 C 370 150, 400 80, 468 80", !dog)}
  ${arrow("M 302 150 C 370 150, 400 220, 468 220", dog)}
  ${node(80,150,"&#128054;",true)}   ${label(80,222,"input image",false,400)}
  ${node(250,150,"&#129504;",true)}  ${label(250,222,"model",false,400)}
  ${node(520,80,"&#128049;",!dog)}
  ${label(520,152,"cat &#183; "+Math.round((1-p)*100)+"%",!dog)}
  ${node(520,220,"&#128021;",dog)}
  ${label(520,292,"dog &#183; "+Math.round(p*100)+"%",dog)}
  </svg>`;
  document.getElementById("v").textContent = p.toFixed(2);
  document.getElementById("rule").innerHTML = dog
    ? `p(dog) = ${p.toFixed(2)} &gt; p(cat) = ${(1-p).toFixed(2)} &rarr; classify as <b>&nbsp;dog</b>&nbsp;&#128021;`
    : `p(cat) = ${(1-p).toFixed(2)} &ge; p(dog) = ${p.toFixed(2)} &rarr; classify as <b>&nbsp;cat</b>&nbsp;&#128049;`;
}
const s = document.getElementById("s");
s.addEventListener("input", e => draw(parseFloat(e.target.value)));
draw(parseFloat(s.value));
</script></body></html>
"""


def show_classifier(start=0.5, width=720, height=460):
    """Show the classifier flowchart. The result is the class with the highest probability."""
    # start: the first value of the slider, p(dog).
    page = _PAGE.replace("__P__", repr(float(start)))
    # The iframe keeps the JavaScript. JupyterLab removes JavaScript from usual HTML output.
    # The div around the iframe stops an unnecessary warning from IPython.
    display(HTML(
        '<div><iframe srcdoc="' + html.escape(page, quote=True) + '" '
        'width="' + str(width) + '" height="' + str(height) + '" '
        'style="border:none" sandbox="allow-scripts"></iframe></div>'
    ))


# The page below is a template. Python replaces __F__, __H1__, __H2__ and __C__.
_NETWORK_PAGE = """
<!doctype html><html><head><meta charset="utf-8"><style>
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:#3c4043}
 .ctl{display:flex;align-items:center;gap:8px;font-size:14px;margin:0 16px 6px 0}
 .ctl b{min-width:14px;color:#2f6fed}
 .bar{display:flex;flex-wrap:wrap;padding:4px 0 10px 4px}
 input[type=range]{width:120px;accent-color:#2f6fed}
 #chain{font-size:14px;color:#5f6368;padding:6px 0 0 4px}
</style></head><body>
<div class="bar">
 <div class="ctl"><label for="f">features p</label>
  <input id="f" type="range" min="1" max="5" step="1" value="__F__"><b id="fv"></b></div>
 <div class="ctl"><label for="h1">hidden 1</label>
  <input id="h1" type="range" min="1" max="5" step="1" value="__H1__"><b id="h1v"></b></div>
 <div class="ctl"><label for="h2">hidden 2</label>
  <input id="h2" type="range" min="0" max="5" step="1" value="__H2__"><b id="h2v"></b></div>
 <div class="ctl"><label for="c">classes m</label>
  <input id="c" type="range" min="2" max="5" step="1" value="__C__"><b id="cv"></b></div>
</div>
<div id="fig"></div>
<div id="chain"></div>
<script>
const ACCENT="#2f6fed", GREY="#8a8f98", LINE="#ccd4e8";
const g = id => document.getElementById(id);
const CY = 150, GAP = 46, R = 17;

function ys(n){
  const out = [];
  for(let i=0;i<n;i++){ out.push(CY + (i - (n-1)/2) * GAP); }
  return out;
}
function draw(){
  const p=+g("f").value, h1=+g("h1").value, h2=+g("h2").value, m=+g("c").value;
  g("fv").textContent=p; g("h1v").textContent=h1;
  g("h2v").textContent = h2===0 ? "none" : h2;
  g("cv").textContent=m;

  const L = [{n:p, name:"X", note:"n\\u00d7"+p, fill:"#f2f4f8", stroke:"#c9d0dd"},
             {n:h1, name:"A\\u2081", note:"n\\u00d7"+h1, fill:"#eef3ff", stroke:ACCENT}];
  if(h2>0) L.push({n:h2, name:"A\\u2082", note:"n\\u00d7"+h2, fill:"#eef3ff", stroke:ACCENT});
  L.push({n:m, name:"P", note:"n\\u00d7"+m, fill:"#eef3ff", stroke:ACCENT});

  const x0=100, x1=580;
  const xs = L.map((_,i)=> L.length===1 ? x0 : x0 + i*(x1-x0)/(L.length-1));
  const pos = L.map((l,i)=> ys(l.n).map(y=>({x:xs[i], y})));

  let s = `<svg viewBox="0 0 680 320" width="100%" style="max-width:680px">`;
  for(let i=0;i<pos.length-1;i++){
    for(const a of pos[i]) for(const b of pos[i+1]){
      s += `<line x1="${a.x+R}" y1="${a.y}" x2="${b.x-R}" y2="${b.y}"
             stroke="${LINE}" stroke-width="1"/>`;
    }
  }
  for(let i=0;i<L.length;i++){
    for(const c of pos[i]){
      s += `<circle cx="${c.x}" cy="${c.y}" r="${R}" fill="${L[i].fill}"
             stroke="${L[i].stroke}" stroke-width="2"/>`;
    }
    s += `<text x="${xs[i]}" y="285" font-size="15" font-weight="600"
           text-anchor="middle" fill="${ACCENT}">${L[i].name}</text>`;
    s += `<text x="${xs[i]}" y="304" font-size="13"
           text-anchor="middle" fill="${GREY}">${L[i].note}</text>`;
  }
  for(let i=0;i<L.length-1;i++){
    const mx = (xs[i]+xs[i+1])/2;
    s += `<text x="${mx}" y="36" font-size="13" text-anchor="middle" fill="${GREY}">
           W${i+1} ${L[i].n}\\u00d7${L[i+1].n}</text>`;
  }
  g("fig").innerHTML = s + `</svg>`;

  const steps = ["X"];
  for(let i=0;i<L.length-1;i++){
    steps.push(`W${i+1} ${L[i].n}\\u00d7${L[i+1].n}`);
    steps.push(i===L.length-2 ? "softmax" : "relu");
  }
  steps.push("P");
  g("chain").textContent = steps.join("  \\u2192  ");
}
for(const id of ["f","h1","h2","c"]) g(id).addEventListener("input", draw);
draw();
</script></body></html>
"""


def show_network(features=3, hidden1=4, hidden2=0, classes=2, width=720, height=480):
    """Show a network diagram. Set hidden2 to 0 for one hidden layer."""
    # features: the number of input features p.
    # hidden1, hidden2: the number of units in each hidden layer, 0 to 5.
    # classes: the number of output classes m.
    page = _NETWORK_PAGE.replace("__F__", str(int(features)))
    page = page.replace("__H1__", str(int(hidden1)))
    page = page.replace("__H2__", str(int(hidden2)))
    page = page.replace("__C__", str(int(classes)))
    display(HTML(
        '<div><iframe srcdoc="' + html.escape(page, quote=True) + '" '
        'width="' + str(width) + '" height="' + str(height) + '" '
        'style="border:none" sandbox="allow-scripts"></iframe></div>'
    ))


# The page below lets the student change the weights with sliders.
# Each slider column is below the connections that it controls.
# The thickness of each line shows the strength of the signal on that connection.
# Blue is a positive signal. Orange is a negative signal.
_WEIGHTS_PAGE = """
<!doctype html><html><head><meta charset="utf-8"><style>
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:#3c4043}
 .bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:2px 0 8px 4px;font-size:14px}
 .ctl{display:flex;align-items:center;gap:8px}
 .ctl b{min-width:30px;color:#2f6fed}
 .ctl input[type=range]{width:110px;accent-color:#2f6fed}
 button{font:inherit;font-size:14px;padding:4px 10px;border:1px solid #d3d6db;
   border-radius:8px;background:#fff;cursor:pointer}
 button:hover{border-color:#2f6fed;color:#2f6fed}
 .panel{position:relative;max-width:660px;height:132px;margin-top:2px}
 .col{position:absolute;width:186px}
 #c1{left:calc(37% - 93px)}
 #c2{left:calc(66.7% - 93px)}
 .head{font-size:13px;color:#8a8f98;text-align:center;margin-bottom:6px}
 .row{display:flex;align-items:center;gap:6px;font-size:12px;margin-bottom:5px}
 .row label{width:58px;color:#5f6368;text-align:right;white-space:nowrap}
 .row input[type=range]{width:84px;accent-color:#2f6fed}
 .row b{width:32px;color:#2f6fed;text-align:right}
</style></head><body>
<div class="bar">
 <span>input image:</span>
 <button id="bdog">&#128054; dog</button>
 <button id="bcat">&#128049; cat</button>
 <div class="ctl"><label for="x0">pointy ears</label>
  <input id="x0" type="range" min="0" max="1" step="0.05" value="0.2"><b id="x0v"></b></div>
 <div class="ctl"><label for="x1">long snout</label>
  <input id="x1" type="range" min="0" max="1" step="0.05" value="0.9"><b id="x1v"></b></div>
</div>
<div id="fig"></div>
<div class="panel"><div class="col" id="c1"></div><div class="col" id="c2"></div></div>
<div style="padding-left:4px"><button id="reset">reset weights</button></div>
<script>
const ACCENT="#2f6fed", POS="#2f6fed", NEG="#e0701c", GREY="#8a8f98";
const D1=[[1.5,-1.5],[-1.5,1.5]], D2=[[2,-2],[-2,2]];
let W1=D1.map(r=>r.slice()), W2=D2.map(r=>r.slice());
const g=id=>document.getElementById(id);
const FX=[150,150], HX=[340,340], OX=[540,540];
const FY=[118,208], HY=[118,208], OY=[104,222];

function relu(z){ return z>0?z:0; }
function softmax(z){
  const mx=Math.max(...z), e=z.map(v=>Math.exp(v-mx)), s=e.reduce((a,b)=>a+b,0);
  return e.map(v=>v/s);
}
function edge(x1,y1,x2,y2,c){
  const w = 1 + 5*Math.min(1, Math.abs(c)/2);
  const col = c>=0 ? POS : NEG;
  const op = 0.18 + 0.72*Math.min(1, Math.abs(c)/2);
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}"
    stroke-width="${w.toFixed(2)}" opacity="${op.toFixed(2)}"/>`;
}
function unit(cx,cy,val,label,maxv){
  const t = maxv>0 ? Math.min(1, val/maxv) : 0;
  const fill = `rgba(47,111,237,${(0.06+0.5*t).toFixed(3)})`;
  return `<circle cx="${cx}" cy="${cy}" r="24" fill="${fill}" stroke="${ACCENT}"
     stroke-width="2"/>
   <text x="${cx}" y="${cy+4}" font-size="12" text-anchor="middle"
     fill="#26303d">${val.toFixed(2)}</text>
   <text x="${cx}" y="${cy+42}" font-size="12" text-anchor="middle"
     fill="${GREY}">${label}</text>`;
}
function box(cx,cy,emoji,on){
  return `<g opacity="${on?1:0.35}"><rect x="${cx-38}" y="${cy-38}" width="76" height="76"
    rx="18" fill="${on?'#eef3ff':'#f7f7f8'}" stroke="${on?ACCENT:'#e4e5e9'}"
    stroke-width="2"/><text x="${cx}" y="${cy+3}" font-size="38" text-anchor="middle"
    dominant-baseline="middle">${emoji}</text></g>`;
}
function draw(){
  const x=[+g("x0").value, +g("x1").value];
  g("x0v").textContent=x[0].toFixed(2); g("x1v").textContent=x[1].toFixed(2);

  const z1=[0,0];
  for(let j=0;j<2;j++) for(let i=0;i<2;i++) z1[j]+=x[i]*W1[i][j];
  const a=z1.map(relu);
  const z2=[0,0];
  for(let k=0;k<2;k++) for(let j=0;j<2;j++) z2[k]+=a[j]*W2[j][k];
  const p=softmax(z2);
  const dogWins = p[1] > p[0];

  let s=`<svg viewBox="0 0 660 300" width="100%" style="max-width:660px">`;
  s+=`<line x1="88" y1="163" x2="118" y2="140" stroke="#d8dade" stroke-width="1.5"
       stroke-dasharray="4 3"/>`;
  s+=`<line x1="88" y1="163" x2="118" y2="190" stroke="#d8dade" stroke-width="1.5"
       stroke-dasharray="4 3"/>`;
  for(let i=0;i<2;i++) for(let j=0;j<2;j++)
    s+=edge(FX[i]+24, FY[i], HX[j]-24, HY[j], x[i]*W1[i][j]);
  for(let j=0;j<2;j++) for(let k=0;k<2;k++)
    s+=edge(HX[j]+24, HY[j], OX[k]-38, OY[k], a[j]*W2[j][k]);

  s+=box(50,163, dogWins?"&#128054;":"&#128049;", true);
  s+=`<text x="50" y="222" font-size="12" text-anchor="middle" fill="${GREY}">input</text>`;
  const mx1=Math.max(...x,0.001), mxa=Math.max(...a,0.001);
  s+=unit(FX[0],FY[0],x[0],"ears",mx1);
  s+=unit(FX[1],FY[1],x[1],"snout",mx1);
  s+=unit(HX[0],HY[0],a[0],"a1",mxa);
  s+=unit(HX[1],HY[1],a[1],"a2",mxa);
  s+=box(OX[0],OY[0],"&#128049;", !dogWins);
  s+=`<text x="${OX[0]}" y="${OY[0]+58}" font-size="14" font-weight="600"
      text-anchor="middle" fill="${!dogWins?ACCENT:GREY}">cat ${(p[0]*100).toFixed(0)}%</text>`;
  s+=box(OX[1],OY[1],"&#128021;", dogWins);
  s+=`<text x="${OX[1]}" y="${OY[1]+58}" font-size="14" font-weight="600"
      text-anchor="middle" fill="${dogWins?ACCENT:GREY}">dog ${(p[1]*100).toFixed(0)}%</text>`;
  g("fig").innerHTML=s+`</svg>`;
}
function column(el,title,W,rows,cols,tag){
  let h=`<div class="head">${title}</div>`;
  for(let i=0;i<rows.length;i++) for(let j=0;j<cols.length;j++){
    h+=`<div class="row"><label for="${tag}-${i}-${j}">${rows[i]} &rarr; ${cols[j]}</label>
      <input id="${tag}-${i}-${j}" type="range" min="-3" max="3" step="0.25"
       value="${W[i][j]}"><b id="${tag}-${i}-${j}-v">${W[i][j].toFixed(2)}</b></div>`;
  }
  el.innerHTML=h;
  for(let i=0;i<rows.length;i++) for(let j=0;j<cols.length;j++){
    g(`${tag}-${i}-${j}`).addEventListener("input", e=>{
      const v=parseFloat(e.target.value);
      (tag==="w1"?W1:W2)[i][j]=v;
      g(`${tag}-${i}-${j}-v`).textContent=v.toFixed(2);
      draw();
    });
  }
}
function columns(){
  column(g("c1"),"W1",W1,["ears","snout"],["a1","a2"],"w1");
  column(g("c2"),"W2",W2,["a1","a2"],["cat","dog"],"w2");
}
g("bdog").addEventListener("click",()=>{g("x0").value=0.2;g("x1").value=0.9;draw();});
g("bcat").addEventListener("click",()=>{g("x0").value=0.9;g("x1").value=0.1;draw();});
g("reset").addEventListener("click",()=>{
  W1=D1.map(r=>r.slice()); W2=D2.map(r=>r.slice()); columns(); draw();
});
columns(); draw();
</script></body></html>
"""


def show_weights(width=720, height=600):
    """Show a small network with weights that the student can change."""
    # The network has 2 features, 2 hidden units and 2 classes.
    # All the biases are 0.
    display(HTML(
        '<div><iframe srcdoc="' + html.escape(_WEIGHTS_PAGE, quote=True) + '" '
        'width="' + str(width) + '" height="' + str(height) + '" '
        'style="border:none" sandbox="allow-scripts"></iframe></div>'
    ))


# The page below shows a middle layer of two neurons, two outputs and the graph of the relu function.
# Each weight is on a connection. Each neuron has its own bias.
# The orange circles are the neurons. The blue lines are the signal.
# The legend gives the colors.
_RELU_PAGE = """
<!doctype html><html><head><meta charset="utf-8"><style>
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:#3c4043}
 .bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:2px 0 6px 4px;font-size:13px}
 .grp{display:flex;align-items:center;gap:10px;padding:4px 10px;border:1px solid #edeef1;
   border-radius:10px}
 .grp>span{color:#8a8f98}
 .ctl{display:flex;align-items:center;gap:6px}
 .ctl b{min-width:30px;color:#2f6fed;text-align:right}
 .n1 .ctl b, .n2 .ctl b{color:#e8710a}
 input[type=range]{width:88px;accent-color:#2f6fed}
 input[type=checkbox]{accent-color:#2f6fed}
 .n1 input[type=range], .n2 input[type=range]{accent-color:#e8710a}
 #sum{font-size:14px;color:#3c4043;padding:6px 0 0 4px;line-height:1.7}
</style></head><body>
<div class="bar">
 <div class="grp"><span>input</span>
  <div class="ctl"><label for="x">x</label>
   <input id="x" type="range" min="-3" max="3" step="0.1" value="2"><b id="xv"></b></div></div>
 <div class="grp n1"><span>neuron 1</span>
  <div class="ctl"><label for="w1">w1</label>
   <input id="w1" type="range" min="-2" max="2" step="0.1" value="1"><b id="w1v"></b></div>
  <div class="ctl"><label for="b1">b1</label>
   <input id="b1" type="range" min="-2" max="2" step="0.1" value="0"><b id="b1v"></b></div></div>
 <div class="grp n2"><span>neuron 2</span>
  <div class="ctl"><label for="w2">w2</label>
   <input id="w2" type="range" min="-2" max="2" step="0.1" value="-1"><b id="w2v"></b></div>
  <div class="ctl"><label for="b2">b2</label>
   <input id="b2" type="range" min="-2" max="2" step="0.1" value="0.5"><b id="b2v"></b></div></div>
 <div class="grp"><label><input id="sm" type="checkbox"> softmax</label></div>
</div>
<div id="fig"></div>
<div id="sum"></div>
<script>
const BLUE="#2f6fed", ORANGE="#e8710a", GREY="#8a8f98", DIM="#c9d0dd";
const g=id=>document.getElementById(id);
const X0=392, X1=640, Y0=52, Y1=214;
const sx=z=>X0+(z+8)*(X1-X0)/16;
const sy=a=>Y1-a*(Y1-Y0)/8;
const IN={x:56,y:126}, N1={x:190,y:62}, N2={x:190,y:190}, O1={x:314,y:62}, O2={x:314,y:190};

function node(c,r,val,col,t){
  const rgb = col===ORANGE ? "232,113,10" : "47,111,237";
  return `<circle cx="${c.x}" cy="${c.y}" r="${r}" fill="rgba(${rgb},${(0.06+0.5*Math.min(1,t)).toFixed(3)})"
    stroke="${col}" stroke-width="2"/><text x="${c.x}" y="${c.y+5}" font-size="12"
    text-anchor="middle" fill="#26303d">${val}</text>`;
}
function outbox(c,e,on){
  return `<g opacity="${on?1:0.45}"><rect x="${c.x-32}" y="${c.y-32}" width="64" height="64"
    rx="16" fill="#eef3ff" stroke="${BLUE}" stroke-width="2"/><text x="${c.x}" y="${c.y+3}"
    font-size="32" text-anchor="middle" dominant-baseline="middle">${e}</text></g>`;
}
function cap(x,y,t,col,size,anchor){
  return `<text x="${x}" y="${y}" font-size="${size||12}" text-anchor="${anchor||"middle"}"
    fill="${col||GREY}">${t}</text>`;
}
function link(a,b,ra,rb,col,dash){
  const dx=b.x-a.x, dy=b.y-a.y, L=Math.hypot(dx,dy);
  const p1={x:a.x+dx/L*ra, y:a.y+dy/L*ra}, p2={x:b.x-dx/L*rb, y:b.y-dy/L*rb};
  return {line:`<line x1="${p1.x.toFixed(1)}" y1="${p1.y.toFixed(1)}"
    x2="${p2.x.toFixed(1)}" y2="${p2.y.toFixed(1)}" stroke="${col}" stroke-width="1.8"
    ${dash?'stroke-dasharray="4 3"':""}/>`,
    mid:{x:a.x+dx*0.42, y:a.y+dy*0.42-6}};
}
function draw(){
  const x=+g("x").value, w1=+g("w1").value, b1=+g("b1").value,
        w2=+g("w2").value, b2=+g("b2").value;
  for(const id of ["x","w1","b1","w2","b2"]) g(id+"v").textContent=(+g(id).value).toFixed(1);
  const z1=w1*x+b1, a1=Math.max(z1,0), z2=w2*x+b2, a2=Math.max(z2,0), y1=a1, y2=a2;
  const sm=g("sm").checked, e1x=Math.exp(y1), e2x=Math.exp(y2);
  const p1=e1x/(e1x+e2x), p2=e2x/(e1x+e2x);
  const o1 = sm ? p1 : y1, o2 = sm ? p2 : y2;

  let s=`<svg viewBox="0 0 660 366" width="100%" style="max-width:660px">`;
  const e1=link(IN,N1,22,28,BLUE), e2=link(IN,N2,22,28,BLUE);
  const e5=link(N1,O1,28,32,a1>0?BLUE:DIM), e6=link(N2,O2,28,32,a2>0?BLUE:DIM);
  s+=e1.line+e2.line+e5.line+e6.line;
  s+=cap(e1.mid.x-6,e1.mid.y-10,"w1: "+w1.toFixed(1),BLUE);
  s+=cap(e2.mid.x-6,e2.mid.y+34,"w2: "+w2.toFixed(1),BLUE);

  s+=node(IN,22,x.toFixed(1),BLUE,Math.abs(x)/3);
  s+=cap(IN.x,IN.y+38,"input x");
  s+=node(N1,28,a1.toFixed(2),ORANGE,a1/8);
  s+=cap(N1.x,N1.y-38,"neuron 1",ORANGE);
  s+=cap(N1.x,N1.y+42,"bias 1: "+b1.toFixed(1),GREY);
  s+=cap(N1.x+34,N1.y-10,"z1: "+z1.toFixed(2),GREY,11,"start");
  s+=cap(N2.x,N2.y-40,"bias 2: "+b2.toFixed(1),GREY);
  s+=node(N2,28,a2.toFixed(2),ORANGE,a2/8);
  s+=cap(N2.x,N2.y+44,"neuron 2",ORANGE);
  s+=cap(N2.x+34,N2.y-10,"z2: "+z2.toFixed(2),GREY,11,"start");
  const show = o => sm ? Math.round(o*100)+"%" : o.toFixed(2);
  s+=outbox(O1,"&#128049;",o1>=o2);
  s+=`<g opacity="${o1>=o2?1:0.45}" font-weight="600">`+cap(O1.x,O1.y+50,"cat "+show(o1),BLUE,15)+`</g>`;
  s+=outbox(O2,"&#128021;",o2>=o1);
  s+=`<g opacity="${o2>=o1?1:0.45}" font-weight="600">`+cap(O2.x,O2.y+50,"dog "+show(o2),BLUE,15)+`</g>`;

  s+=`<line x1="356" y1="40" x2="356" y2="250" stroke="#ecedf0" stroke-width="1"/>`;
  s+=`<line x1="${X0}" y1="${Y1}" x2="${X1+6}" y2="${Y1}" stroke="#d8dade" stroke-width="1"/>`;
  s+=`<line x1="${sx(0)}" y1="${Y0-8}" x2="${sx(0)}" y2="${Y1+8}" stroke="#d8dade"
      stroke-width="1"/>`;
  s+=`<polyline points="${sx(-8)},${sy(0)} ${sx(0)},${sy(0)} ${sx(8)},${sy(8)}"
      fill="none" stroke="${ORANGE}" stroke-width="2.5"/>`;
  s+=cap(X1+2,Y1+18,"z");
  s+=cap(sx(0)-30,Y0+2,"ReLU(z)");
  s+=cap(sx(-8)+8,Y1+18,"-8"); s+=cap(sx(8)-4,Y1+18,"8");
  for(const [z,a,nm] of [[z1,a1,"1"],[z2,a2,"2"]]){
    const px=sx(z), py=sy(a);
    s+=`<line x1="${px}" y1="${py}" x2="${px}" y2="${Y1}" stroke="${ORANGE}"
        stroke-width="1" stroke-dasharray="3 3" opacity="0.5"/>`;
    s+=`<circle cx="${px}" cy="${py}" r="6.5" fill="#fff" stroke="${ORANGE}"
        stroke-width="3"/>`;
    s+=cap(px,py-13,nm,ORANGE,12);
  }

  const LY=290;
  s+=`<circle cx="30" cy="${LY}" r="9" fill="rgba(232,113,10,0.18)" stroke="${ORANGE}"
      stroke-width="2"/>`;
  s+=cap(46,LY+4,"neuron","#5f6368",12,"start");
  s+=`<line x1="120" y1="${LY}" x2="140" y2="${LY}" stroke="${BLUE}" stroke-width="1.8"/>`;
  s+=cap(148,LY+4,"signal","#5f6368",12,"start");
  g("fig").innerHTML=s+`</svg>`;

  const one=(n,w,b,z,a)=>`neuron ${n}: z${n} = ${w.toFixed(1)} &times; ${x.toFixed(1)} `
    +`${b<0?"&minus;":"+"} ${Math.abs(b).toFixed(1)} = ${z.toFixed(2)}`
    +` &nbsp;&#8594;&nbsp; a${n} = ReLU(${z.toFixed(2)}) = <b>${a.toFixed(2)}</b>`;
  g("sum").innerHTML = one(1,w1,b1,z1,a1) + "<br>" + one(2,w2,b2,z2,a2)
    + `<br>outputs (logits): cat = a1 = <b>${y1.toFixed(2)}</b>, dog = a2 = <b>${y2.toFixed(2)}</b>`
    + (sm ? `<br>softmax: p(cat) = exp(a1) / (exp(a1) + exp(a2)) = <b>${p1.toFixed(2)}</b>,`
      + ` p(dog) = <b>${p2.toFixed(2)}</b>` : "");
}
for(const id of ["x","w1","b1","w2","b2","sm"]) g(id).addEventListener("input", draw);
draw();
</script></body></html>
"""


def show_relu(width=720, height=600):
    """Show a layer of two relu neurons, and the relu graph."""
    # The student changes the input x, and the weight and bias of each neuron.
    # Each neuron computes z = wx + b, then a = ReLU(z).
    # There is one output per class, cat and dog. Each neuron feeds one output, with weight 1.
    # The outputs have no activation function.
    # The softmax box, off at the start, turns the two outputs into probabilities.
    display(HTML(
        '<div><iframe srcdoc="' + html.escape(_RELU_PAGE, quote=True) + '" '
        'width="' + str(width) + '" height="' + str(height) + '" '
        'style="border:none" sandbox="allow-scripts"></iframe></div>'
    ))


# The page below lights up the layers of a network one after the other.
# It shows the path of the signal to one output per class. The orange circles are the neurons.
# The blue lines are the signal. The legend gives the colors.
# The row at the top names the weights and the biases of each layer.
_FLOW_PAGE = """
<!doctype html><html><head><meta charset="utf-8"><style>
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:#3c4043}
 .bar{display:flex;align-items:center;gap:10px;padding:2px 0 6px 4px;font-size:14px}
 button{font:inherit;font-size:14px;padding:4px 12px;border:1px solid #d3d6db;
   border-radius:8px;background:#fff;cursor:pointer}
 button:hover{border-color:#2f6fed;color:#2f6fed}
 svg g.on{transition:opacity 420ms ease}
</style></head><body>
<div class="bar"><button id="toggle">pause</button><button id="again">replay</button>
 <button id="prev">&#9664; previous</button><button id="next">next &#9654;</button></div>
<div id="fig"></div>
<script>
const ACCENT="#2f6fed", ORANGE="#e8710a", DIMN="#e4e5e9", DIME="#eceef2", GREY="#8a8f98";
const g=id=>document.getElementById(id);
const SIZES=[2,5,3,4], XS=[60,190,320,450], OUTX=584, CY=150, R=14;
const PDOG=__PDOG__;

function ys(n,gap){
  const out=[];
  for(let i=0;i<n;i++) out.push(CY+(i-(n-1)/2)*gap);
  return out;
}
const POS=SIZES.map((n,i)=>ys(n, n>4?40:52).map(y=>({x:XS[i],y})));
const OUTS=[{x:OUTX,y:CY-58,e:"&#128049;",name:"cat",p:1-PDOG},
            {x:OUTX,y:CY+58,e:"&#128021;",name:"dog",p:PDOG}];

function dot(c,r,lit,col){
  const on = col||ACCENT;
  const rgb = on===ORANGE ? "232,113,10" : "47,111,237";
  return `<circle cx="${c.x}" cy="${c.y}" r="${r}" fill="${lit?`rgba(${rgb},0.18)`:"#fbfbfc"}"
    stroke="${lit?on:DIMN}" stroke-width="${lit?2:1.5}"/>`;
}
function wire(a,b,ra,rb,lit){
  const dx=b.x-a.x, dy=b.y-a.y, L=Math.hypot(dx,dy);
  return `<line x1="${(a.x+dx/L*ra).toFixed(1)}" y1="${(a.y+dy/L*ra).toFixed(1)}"
    x2="${(b.x-dx/L*rb).toFixed(1)}" y2="${(b.y-dy/L*rb).toFixed(1)}"
    stroke="${lit?ACCENT:DIME}" stroke-width="${lit?1.6:1}"
    ${lit?'opacity="0.55"':""}/>`;
}
function outbox(o,lit){
  return `<rect x="${o.x-32}" y="${o.y-32}" width="64" height="64" rx="16"
    fill="${lit?"#eef3ff":"#fbfbfc"}" stroke="${lit?ACCENT:DIMN}" stroke-width="2"/>
   <text x="${o.x}" y="${o.y+3}" font-size="32" text-anchor="middle"
    dominant-baseline="middle">${o.e}</text>`;
}
function layerWires(i,lit){
  let s="";
  if(i===SIZES.length){
    for(const a of POS[SIZES.length-1]) for(const o of OUTS) s+=wire(a,o,R,32,lit);
  } else {
    for(const a of POS[i-1]) for(const b of POS[i]) s+=wire(a,b,i===1?16:R,R,lit);
  }
  return s;
}
function build(){
  let s=`<svg viewBox="0 0 660 310" width="100%" style="max-width:660px">`;
  for(let i=1;i<=SIZES.length;i++) s+=layerWires(i,false);
  for(let i=0;i<SIZES.length;i++) for(const c of POS[i]) s+=dot(c,i===0?16:R,false);
  for(const o of OUTS) s+=outbox(o,false);
  const ALLX=XS.concat([OUTX]);
  for(let i=0;i<ALLX.length-1;i++){
    s+=`<text x="${(ALLX[i]+ALLX[i+1])/2}" y="24" font-size="13" font-weight="600"
        text-anchor="middle" fill="${ACCENT}">W<tspan baseline-shift="super" font-size="9">(${i+1})</tspan></text>`;
    s+=`<text x="${ALLX[i+1]}" y="24" font-size="13" font-weight="600"
        text-anchor="middle" fill="${ORANGE}">b<tspan baseline-shift="super" font-size="9">(${i+1})</tspan></text>`;
  }
  s+=`<text x="${XS[0]}" y="${CY+72}" font-size="13" text-anchor="middle"
      fill="${GREY}">features x</text>`;
  s+=`<text x="${OUTX}" y="${CY+140}" font-size="13" text-anchor="middle"
      fill="${GREY}">prediction</text>`;

  s+=`<g class="on" id="on-0" opacity="0">`;
  for(const c of POS[0]) s+=dot(c,16,true);
  s+=`</g>`;
  for(let i=1;i<=SIZES.length;i++){
    s+=`<g class="on" id="on-${i}" opacity="0">`+layerWires(i,true);
    if(i<SIZES.length){ for(const c of POS[i]) s+=dot(c,R,true,ORANGE); }
    else for(const o of OUTS){
      const best = o.p >= 1-o.p;
      s+=`<g opacity="${best?1:0.45}">`+outbox(o,true);
      s+=`<text x="${o.x}" y="${o.y+50}" font-size="15" font-weight="600"
          text-anchor="middle" fill="${ACCENT}">${o.name} ${Math.round(o.p*100)}%</text></g>`;
    }
    s+=`</g>`;
  }
  const LY=274;
  s+=`<circle cx="30" cy="${LY}" r="9" fill="rgba(232,113,10,0.18)" stroke="${ORANGE}"
      stroke-width="2"/>`;
  s+=`<text x="46" y="${LY+4}" font-size="12" fill="#5f6368">neuron</text>`;
  s+=`<line x1="120" y1="${LY}" x2="140" y2="${LY}" stroke="${ACCENT}" stroke-width="1.8"
      opacity="0.55"/>`;
  s+=`<text x="148" y="${LY+4}" font-size="12" fill="#5f6368">signal</text>`;
  g("fig").innerHTML=s+`</svg>`;
}
function setStep(k){
  for(let i=0;i<=SIZES.length;i++) g("on-"+i).setAttribute("opacity", i<=k?"1":"0");
}
let step=-1, timer=null;
function tick(){
  step=(step+1)%7;
  if(step<=4) setStep(step);
  else if(step===5) setStep(4);
  else setStep(-1);
}
// The layer that is lit now: -1 (none) to 4. Steps 5 and 6 of tick hold the picture and clear it.
function shown(){ return step<=4 ? step : (step===5 ? 4 : -1); }
function start(){ if(!timer){ timer=setInterval(tick,850); g("toggle").textContent="pause"; } }
function stop(){ if(timer){ clearInterval(timer); timer=null; g("toggle").textContent="play"; } }
g("toggle").addEventListener("click",()=>{ timer?stop():start(); });
g("again").addEventListener("click",()=>{ stop(); step=-1; setStep(-1); start(); });
// The previous and next buttons stop the animation and move one layer.
g("next").addEventListener("click",()=>{ stop(); const s=shown(); step = s===4 ? -1 : s+1; setStep(step); });
g("prev").addEventListener("click",()=>{ stop(); const s=shown(); step = s===-1 ? 4 : s-1; setStep(step); });
build(); setStep(-1); start();
</script></body></html>
"""


def show_flow(probability=0.71, width=720, height=380):
    """Show a network that lights up layer by layer, and its prediction."""
    # The network has 2 inputs, 3 middle layers and 2 outputs, one per class.
    # probability: the predicted probability of dog. The probability of cat is the rest.
    # The animation repeats. The buttons stop it and start it again.
    # The previous and next buttons stop it and move one layer at a time.
    page = _FLOW_PAGE.replace("__PDOG__", repr(float(probability)))
    display(HTML(
        '<div><iframe srcdoc="' + html.escape(page, quote=True) + '" '
        'width="' + str(width) + '" height="' + str(height) + '" '
        'style="border:none" sandbox="allow-scripts"></iframe></div>'
    ))


# The page below is the flow of show_flow in the opposite direction.
# The forward pass is already done, and it stays visible in pale colors.
# The gradient (purple) goes from the output back to the input, one layer at a time.
# When the gradient passes a layer, the weights and the bias of that layer get a purple mark: they are updated.
# After the input, the next training step starts with a better prediction and a lower loss.
_BACKPROP_PAGE = """
<!doctype html><html><head><meta charset="utf-8"><style>
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:#3c4043}
 .bar{display:flex;align-items:center;gap:10px;padding:2px 0 6px 4px;font-size:14px}
 button{font:inherit;font-size:14px;padding:4px 12px;border:1px solid #d3d6db;
   border-radius:8px;background:#fff;cursor:pointer}
 button:hover{border-color:#2f6fed;color:#2f6fed}
 #stat{color:#5f6368;margin-left:6px}
 #stat b{color:#9334e6}
 #cap{font-size:14px;line-height:1.6;min-height:46px;padding:2px 0 0 4px}
 svg g.on{transition:opacity 420ms ease}
</style></head><body>
<div class="bar"><button id="toggle">pause</button><button id="again">replay</button>
 <button id="prev">&#9664; previous</button><button id="next">next &#9654;</button>
 <span id="stat"></span></div>
<div id="fig"></div>
<div id="cap"></div>
<script>
const ACCENT="#2f6fed", ORANGE="#e8710a", PURPLE="#9334e6";
const DIMN="#e4e5e9", GREY="#8a8f98";
const RGB={[ACCENT]:"47,111,237",[ORANGE]:"232,113,10",[PURPLE]:"147,52,230"};
const g=id=>document.getElementById(id);
const SIZES=[2,5,3,4], XS=[60,190,320,450], OUTX=584, CY=150, R=14;
const ALLX=XS.concat([OUTX]);
const PDOGS=__PDOGS__;
const LAST=6;

function ys(n,gap){
  const out=[];
  for(let i=0;i<n;i++) out.push(CY+(i-(n-1)/2)*gap);
  return out;
}
const POS=SIZES.map((n,i)=>ys(n, n>4?40:52).map(y=>({x:XS[i],y})));
const OUTS=[{x:OUTX,y:CY-58,e:"&#128049;",name:"cat"},
            {x:OUTX,y:CY+58,e:"&#128021;",name:"dog"}];

function dot(c,r,col){
  return `<circle cx="${c.x}" cy="${c.y}" r="${r}" fill="rgba(${RGB[col]},0.18)"
    stroke="${col}" stroke-width="2"/>`;
}
function wire(a,b,ra,rb,col,w,op){
  const dx=b.x-a.x, dy=b.y-a.y, L=Math.hypot(dx,dy);
  return `<line x1="${(a.x+dx/L*ra).toFixed(1)}" y1="${(a.y+dy/L*ra).toFixed(1)}"
    x2="${(b.x-dx/L*rb).toFixed(1)}" y2="${(b.y-dy/L*rb).toFixed(1)}"
    stroke="${col}" stroke-width="${w}" opacity="${op}"/>`;
}
function layerWires(i,col,w,op){
  let s="";
  if(i===SIZES.length){
    for(const a of POS[SIZES.length-1]) for(const o of OUTS) s+=wire(a,o,R,32,col,w,op);
  } else {
    for(const a of POS[i-1]) for(const b of POS[i]) s+=wire(a,b,i===1?16:R,R,col,w,op);
  }
  return s;
}
function outbox(o,col){
  return `<rect x="${o.x-32}" y="${o.y-32}" width="64" height="64" rx="16"
    fill="#eef3ff" stroke="${col}" stroke-width="2"/>
   <text x="${o.x}" y="${o.y+3}" font-size="32" text-anchor="middle"
    dominant-baseline="middle">${o.e}</text>`;
}
function tag(x,y,t,col){
  return `<text x="${x}" y="${y}" font-size="13" font-weight="600"
    text-anchor="middle" fill="${col}">${t}</text>`;
}
function sup(v,i){
  return `${v}<tspan baseline-shift="super" font-size="9">(${i})</tspan>`;
}
function pill(x,y,t){
  return `<rect x="${x-19}" y="${y-15}" width="38" height="21" rx="10" fill="${PURPLE}"/>`
    +tag(x,y,t,"#fff");
}
function build(p){
  let s=`<svg viewBox="0 0 660 310" width="100%" style="max-width:660px">`;
  s+=`<defs><marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6"
      markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"
      fill="${PURPLE}"/></marker></defs>`;

  // The forward pass is already done. It stays in pale colors.
  for(let i=1;i<=SIZES.length;i++) s+=layerWires(i,ACCENT,1,0.22);
  for(const c of POS[0]) s+=dot(c,16,ACCENT);
  for(let i=1;i<SIZES.length;i++) for(const c of POS[i]) s+=dot(c,R,ORANGE);
  for(const o of OUTS){
    const q = o.name==="dog" ? p : 1-p;
    s+=`<g opacity="${q>=1-q?1:0.45}">`+outbox(o,ACCENT)
      +tag(o.x,o.y+50,`${o.name} ${Math.round(q*100)}%`,ACCENT)+`</g>`;
  }
  s+=`<text x="${OUTX}" y="${CY+126}" font-size="12" text-anchor="middle"
      fill="${GREY}">target: dog</text>`;
  s+=`<text x="${XS[0]}" y="${CY+72}" font-size="13" text-anchor="middle"
      fill="${GREY}">features x</text>`;
  for(let i=1;i<ALLX.length;i++){
    s+=tag((ALLX[i-1]+ALLX[i])/2,24,sup("W",i),ACCENT);
    s+=tag(ALLX[i],24,sup("b",i),ORANGE);
  }

  // The backward pass. Group bk-0 is the error at the output.
  // Group bk-i is the gradient that passes layer i, with the update marks for w_i and b_i.
  s+=`<g class="on" id="bk-0" opacity="0">`;
  for(const o of OUTS) s+=`<rect x="${o.x-37}" y="${o.y-37}" width="74" height="74" rx="19"
      fill="none" stroke="${PURPLE}" stroke-width="2.5"/>`;
  s+=`</g>`;
  for(let i=SIZES.length;i>=1;i--){
    s+=`<g class="on" id="bk-${i}" opacity="0">`+layerWires(i,PURPLE,1.8,0.7);
    if(i>1) for(const c of POS[i-1]) s+=dot(c,R,PURPLE);
    s+=pill((ALLX[i-1]+ALLX[i])/2,24,sup("W",i))+pill(ALLX[i],24,sup("b",i));
    s+=`</g>`;
  }

  const LY=284;
  s+=`<circle cx="30" cy="${LY}" r="9" fill="rgba(232,113,10,0.18)" stroke="${ORANGE}"
      stroke-width="2"/>`;
  s+=`<text x="46" y="${LY+4}" font-size="12" fill="#5f6368">neuron</text>`;
  s+=`<line x1="120" y1="${LY}" x2="140" y2="${LY}" stroke="${ACCENT}" stroke-width="1.8"
      opacity="0.4"/>`;
  s+=`<text x="148" y="${LY+4}" font-size="12" fill="#5f6368">signal (forward)</text>`;
  s+=`<line x1="282" y1="${LY}" x2="256" y2="${LY}" stroke="${PURPLE}" stroke-width="2"
      marker-end="url(#ab)"/>`;
  s+=`<text x="290" y="${LY+4}" font-size="12" fill="#5f6368">gradient (backward)</text>`;
  s+=`<rect x="430" y="${LY-10}" width="22" height="16" rx="8" fill="${PURPLE}"/>`;
  s+=`<text x="460" y="${LY+4}" font-size="12" fill="#5f6368">updated</text>`;
  g("fig").innerHTML=s+`</svg>`;
}

// One training step has the phases 0 to LAST.
// 0: the prediction and the loss. 1: the error at the output.
// 2 to 5: the gradient passes layer 4, 3, 2 and 1. LAST: all parameters took one step.
function caption(k,p){
  const loss=(-Math.log(p)).toFixed(2), i=SIZES.length+2-k;
  if(k===0) return `Forward pass: the network predicts dog ${Math.round(p*100)}%. `
    +`The target is dog, so the loss is &minus;log ${p.toFixed(2)} = <b>${loss}</b>.`;
  if(k===1) return `The backward pass starts at the output, with the error P &minus; Y.`;
  if(k<LAST) return `The gradient passes layer ${i}: `
    +`&part;L/&part;W<sup>(${i})</sup> and &part;L/&part;b<sup>(${i})</sup> are known, `
    +`so <b style="color:${PURPLE}">W<sup>(${i})</sup> and b<sup>(${i})</sup> are updated</b>: `
    +`<span style="white-space:nowrap">W<sup>(${i})</sup> &larr; W<sup>(${i})</sup> &minus; &eta; &part;L/&part;W<sup>(${i})</sup>.</span>`;
  return `All weights and biases took one step against their gradient. `
    +`The next training step starts from the new weights.`;
}
let t=0, k=0, timer=null;
function show(){
  const p=PDOGS[t];
  for(let n=0;n<=SIZES.length;n++){
    const order = n===0 ? 1 : SIZES.length+2-n;
    g("bk-"+n).setAttribute("opacity", k>=order?"1":"0");
  }
  g("cap").innerHTML=caption(k,p);
  g("stat").innerHTML=`training step <b>${t+1}</b> of ${PDOGS.length} &middot; `
    +`loss <b>${(-Math.log(p)).toFixed(2)}</b>`;
}
function tick(){
  if(k<LAST){ k++; show(); return; }
  t=(t+1)%PDOGS.length; k=0; build(PDOGS[t]); show();
}
function back(){
  if(k>0){ k--; show(); return; }
  t=(t-1+PDOGS.length)%PDOGS.length; k=LAST; build(PDOGS[t]); show();
}
function start(){ if(!timer){ timer=setInterval(tick,1300); g("toggle").textContent="pause"; } }
function stop(){ if(timer){ clearInterval(timer); timer=null; g("toggle").textContent="play"; } }
g("toggle").addEventListener("click",()=>{ timer?stop():start(); });
g("again").addEventListener("click",()=>{ stop(); t=0; k=0; build(PDOGS[0]); show(); start(); });
// The previous and next buttons stop the animation and move one phase.
g("next").addEventListener("click",()=>{ stop(); tick(); });
g("prev").addEventListener("click",()=>{ stop(); back(); });
build(PDOGS[0]); show(); start();
</script></body></html>
"""


def show_backprop(probabilities=(0.52, 0.61, 0.69, 0.76, 0.82, 0.86), width=720, height=430):
    """Show the gradient that goes back through the network, and the update of each layer."""
    # The network is the network of show_flow: 2 inputs, 3 middle layers and 2 outputs.
    # The target class is dog.
    # probabilities: the predicted probability of dog at each training step.
    # The animation shows one backward pass per training step, and then goes to the next step.
    # The previous and next buttons stop it and move one phase at a time.
    page = _BACKPROP_PAGE.replace("__PDOGS__", repr([float(p) for p in probabilities]))
    display(HTML(
        '<div><iframe srcdoc="' + html.escape(page, quote=True) + '" '
        'width="' + str(width) + '" height="' + str(height) + '" '
        'style="border:none" sandbox="allow-scripts"></iframe></div>'
    ))

# The page below shows where the indices i, k and j live.
# i is the example (a row of X), k is the feature (a column of X and a row of W1),
# and j is the neuron (a column of W1). The student picks each index with a slider,
# or clicks a cell of X or W1.
_INDICES_PAGE = """
<!doctype html><html><head><meta charset="utf-8"><style>
 body{margin:0;font-family:system-ui,-apple-system,sans-serif;color:#3c4043}
 .bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:2px 0 6px 4px;font-size:14px}
 .ctl{display:flex;align-items:center;gap:6px;padding:4px 10px;border:1px solid #edeef1;
   border-radius:10px}
 .ctl b{min-width:12px}
 input[type=range]{width:90px}
 #ci{accent-color:#1e8e3e} #ck{accent-color:#2f6fed} #cj{accent-color:#e8710a}
 #sum{font-size:14px;line-height:1.8;padding:4px 0 0 4px}
 .i{color:#1e8e3e;font-weight:600} .k{color:#2f6fed;font-weight:600} .j{color:#e8710a;font-weight:600}
 svg rect.pick{cursor:pointer}
</style></head><body>
<div class="bar">
 <div class="ctl"><label for="ci">example <span class="i">i</span></label>
  <input id="ci" type="range" min="1" max="3" step="1" value="2"><b id="civ" class="i"></b></div>
 <div class="ctl"><label for="ck">feature <span class="k">k</span></label>
  <input id="ck" type="range" min="1" max="3" step="1" value="1"><b id="ckv" class="k"></b></div>
 <div class="ctl"><label for="cj">neuron <span class="j">j</span></label>
  <input id="cj" type="range" min="1" max="4" step="1" value="3"><b id="cjv" class="j"></b></div>
</div>
<div id="fig"></div>
<div id="sum"></div>
<script>
const GREEN="#1e8e3e", BLUE="#2f6fed", ORANGE="#e8710a", GREY="#8a8f98", DIM="#e4e5e9";
const N=3, P=3, H=4;
const g=id=>document.getElementById(id);
const sub=t=>`<tspan baseline-shift="sub" font-size="10">${t}</tspan>`;
const XL=40, XT=84, XW=44, XH=30;
const WL=440, WT=84, WW=44, WH=30;
const FX=218, NX=338;
const FY=[64,114,164], NY=[48,92,136,180];

const TINT={[GREEN]:"30,142,62",[ORANGE]:"232,113,10"};
function cell(x,y,w,h,text,level,col,pick){
  const fill = level===2 ? "rgba(47,111,237,0.28)" : level===1 ? `rgba(${TINT[col]},0.10)` : "#fff";
  const line = level===2 ? BLUE : level===1 ? col : DIM;
  return `<rect ${pick?`class="pick" data-pick="${pick}"`:""} x="${x}" y="${y}" width="${w}"
    height="${h}" fill="${fill}" stroke="${line}" stroke-width="${level===2?2:1}"/>
    <text x="${x+w/2}" y="${y+h/2+5}" font-size="13" text-anchor="middle"
    pointer-events="none" fill="#26303d">${text}</text>`;
}
function t(x,y,s,col,size,anchor,weight){
  return `<text x="${x}" y="${y}" font-size="${size||12}" text-anchor="${anchor||"middle"}"
    font-weight="${weight||400}" fill="${col||GREY}">${s}</text>`;
}
function draw(){
  const i=+g("ci").value, k=+g("ck").value, j=+g("cj").value;
  g("civ").textContent=i; g("ckv").textContent=k; g("cjv").textContent=j;
  let s=`<svg viewBox="0 0 660 250" width="100%" style="max-width:660px">`;

  // X: rows are examples i, columns are features k
  s+=t(XL+XW*P/2,34,"X",GREY,15,"middle",600);
  for(let c=1;c<=P;c++) s+=t(XL+XW*(c-0.5),XT-8,c,BLUE,12,"middle",c===k?700:400);
  for(let r=1;r<=N;r++){
    s+=t(XL-10,XT+XH*(r-0.5)+5,r,GREEN,12,"end",r===i?700:400);
    for(let c=1;c<=P;c++){
      const lv = r===i && c===k ? 2 : r===i ? 1 : 0;
      s+=cell(XL+XW*(c-1),XT+XH*(r-1),XW,XH,"X"+sub(r+","+c),lv,GREEN,"x-"+r+"-"+c);
    }
  }
  s+=t(XL+XW*P/2,XT+XH*N+24,"rows: examples "+`<tspan fill="${GREEN}">i</tspan>`);
  s+=t(XL+XW*P/2,XT+XH*N+42,"columns: features "+`<tspan fill="${BLUE}">k</tspan>`);

  // The network: one feature node per k, one neuron per j
  for(let c=1;c<=P;c++) for(let n=1;n<=H;n++){
    const lv = c===k && n===j ? 2 : n===j ? 1 : 0;
    s+=`<line x1="${FX+23}" y1="${FY[c-1]}" x2="${NX-16}" y2="${NY[n-1]}"
        stroke="${lv===2?BLUE:lv?ORANGE:DIM}" stroke-width="${lv===2?3:lv?1.6:1}"
        opacity="${lv===1?0.5:1}"/>`;
  }
  for(let c=1;c<=P;c++){
    const on=c===k;
    s+=`<circle cx="${FX}" cy="${FY[c-1]}" r="23" fill="${on?"rgba(47,111,237,0.18)":"#fff"}"
        stroke="${BLUE}" stroke-width="${on?2.5:1.5}"/>`;
    s+=t(FX-3,FY[c-1]+3,"X"+sub(i+","+c),"#26303d",12);
  }
  for(let n=1;n<=H;n++){
    const on=n===j;
    s+=`<circle cx="${NX}" cy="${NY[n-1]}" r="16" fill="${on?"rgba(232,113,10,0.18)":"#fff"}"
        stroke="${ORANGE}" stroke-width="${on?2.5:1.5}"/>`;
    s+=t(NX,NY[n-1]+5,n,ORANGE,12,"middle",on?700:400);
  }
  const mid=(FX+NX)/2;
  s+=t(mid,34,"example "+`<tspan fill="${GREEN}" font-weight="700">${i}</tspan>`,GREY,13);
  s+=t(FX,212,"features "+`<tspan fill="${BLUE}">k</tspan>`);
  s+=t(NX,212,"neurons "+`<tspan fill="${ORANGE}">j</tspan>`);

  // W1: rows are features k, columns are neurons j
  s+=t(WL+WW*H/2,34,"W"+sub(1),GREY,15,"middle",600);
  for(let c=1;c<=H;c++) s+=t(WL+WW*(c-0.5),WT-8,c,ORANGE,12,"middle",c===j?700:400);
  for(let r=1;r<=P;r++){
    s+=t(WL-10,WT+WH*(r-0.5)+5,r,BLUE,12,"end",r===k?700:400);
    for(let c=1;c<=H;c++){
      const lv = r===k && c===j ? 2 : c===j ? 1 : 0;
      s+=cell(WL+WW*(c-1),WT+WH*(r-1),WW,WH,"w"+sub(r+","+c),lv,ORANGE,"w-"+r+"-"+c);
    }
  }
  s+=t(WL+WW*H/2,WT+WH*P+24,"rows: features "+`<tspan fill="${BLUE}">k</tspan>`);
  s+=t(WL+WW*H/2,WT+WH*P+42,"columns: neurons "+`<tspan fill="${ORANGE}">j</tspan>`);
  g("fig").innerHTML=s+`</svg>`;

  const I=`<span class="i">${i}</span>`, K=c=>`<span class="k">${c}</span>`, J=`<span class="j">${j}</span>`;
  const terms=[1,2,3].map(c=>{
    const term=`X<sub>${I},${K(c)}</sub> w<sub>${K(c)},${J}</sub>`;
    return c===k ? `<b>${term}</b>` : term;
  }).join(" + ");
  g("sum").innerHTML =
    `Example <span class="i">i</span> = ${I} is row ${I} of X: its features are the inputs of the network.<br>`
   +`Weight w<sub>${K(k)},${J}</sub> sits on the connection from feature <span class="k">k</span> = ${K(k)}`
   +` to neuron <span class="j">j</span> = ${J}, in row ${K(k)} and column ${J} of W<sub>1</sub>.<br>`
   +`Neuron ${J} uses all of column ${J}: (z<sub>1</sub>)<sub>${J}</sub> = ${terms} + b<sup>(${J})</sup>`;

  for(const el of document.querySelectorAll("rect.pick")){
    el.addEventListener("click",()=>{
      const [m,r,c]=el.dataset.pick.split("-");
      if(m==="x"){ g("ci").value=r; g("ck").value=c; }
      else { g("ck").value=r; g("cj").value=c; }
      draw();
    });
  }
}
for(const id of ["ci","ck","cj"]) g(id).addEventListener("input", draw);
draw();
</script></body></html>
"""


def show_indices(width=720, height=420):
    """Show where the indices i, k and j live in X, in the network and in W1."""
    # The network has 3 features and 4 neurons. X holds 3 examples.
    # Click a cell of X or W1, or move the sliders, to pick the indices.
    display(HTML(
        '<div><iframe srcdoc="' + html.escape(_INDICES_PAGE, quote=True) + '" '
        'width="' + str(width) + '" height="' + str(height) + '" '
        'style="border:none" sandbox="allow-scripts"></iframe></div>'
    ))
