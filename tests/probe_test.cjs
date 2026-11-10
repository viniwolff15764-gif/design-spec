const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync('skills/design-spec/scripts/probe.js', 'utf8');
function run(compact, count = 80) {
  let reads = 0;
  const rect = {x:10,y:10,width:100,height:30,top:10,bottom:40,left:10,right:110};
  const style = {display:'block',visibility:'visible',opacity:'1',color:'rgb(255, 255, 255)',fontSize:'16px',fontFamily:'sans-serif',backgroundColor:'rgb(0, 0, 0)'};
  const root = {tagName:'MAIN',id:'main',classList:[],getAttribute:()=>null,getBoundingClientRect:()=>rect,parentElement:null,getAnimations:()=>[]};
  const children = Array.from({length:count-1},(_,i)=>({ ...root,tagName:'DIV',id:'n'+i,parentElement:root }));
  root.querySelectorAll=()=>children;
  const context = {document:{querySelector:()=>root,documentElement:{clientWidth:1440,clientHeight:900}},innerWidth:1440,innerHeight:900,devicePixelRatio:1,scrollX:0,scrollY:0,
    getComputedStyle:(el,pseudo)=>{reads++;return pseudo?(el.id==='n2'?{...style,content:'"dot"'}:{content:'none'}):{...style,...(el.id==='n3'?{visibility:'hidden'}:{})};}};
  const probe=vm.runInNewContext('('+source+')',context);
  const result=JSON.parse(JSON.stringify(probe({limit:80,compact})));
  return {result,reads};
}
const expanded=run(false), compact=run(true);
const restored=structuredClone(compact.result.nodes);
for(const node of restored){node.styles=compact.result.styleTable[node.styleRef];delete node.styleRef;for(const key of Object.keys(node.pseudos)){node.pseudos[key]=compact.result.styleTable[node.pseudos[key].styleRef];}}
assert.deepEqual(restored,expanded.result.nodes,'Compact data must preserve every collected style and rectangle');
assert(!restored.some(n=>n.id==='n3'),'Hidden elements must stay excluded');
assert.equal(compact.result.truncated,false);
assert.equal(run(true,100).result.truncated,true,'Limits must be disclosed');
assert(compact.reads < 80*4,'Computed styles should be reused within an invocation');
const expandedBytes=Buffer.byteLength(JSON.stringify(expanded.result));
const compactBytes=Buffer.byteLength(JSON.stringify(compact.result));
assert(compactBytes<expandedBytes);
console.log(JSON.stringify({fixture:'80 DOM nodes, repeated styles, one hidden',visible:restored.length,expandedBytes,compactBytes,reductionPercent:Math.round((1-compactBytes/expandedBytes)*100),assertions:'passed'}));
