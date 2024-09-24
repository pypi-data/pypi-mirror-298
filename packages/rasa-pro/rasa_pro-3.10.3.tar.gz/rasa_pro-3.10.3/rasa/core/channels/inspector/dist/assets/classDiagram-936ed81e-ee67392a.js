import{p as G,d as S,s as A}from"./styles-3dcbcfbf-38957613.js";import{c as v,l as y,h as B,i as W,F as $,z as M,G as I}from"./index-a5d3e69d.js";import{G as O,l as P}from"./layout-78cff630.js";import{l as X}from"./line-5038b469.js";import"./array-9f3ba611.js";import"./path-53f90ab3.js";let H=0;const Y=function(i,a,t,o,p){const g=function(e){switch(e){case p.db.relationType.AGGREGATION:return"aggregation";case p.db.relationType.EXTENSION:return"extension";case p.db.relationType.COMPOSITION:return"composition";case p.db.relationType.DEPENDENCY:return"dependency";case p.db.relationType.LOLLIPOP:return"lollipop"}};a.points=a.points.filter(e=>!Number.isNaN(e.y));const s=a.points,c=X().x(function(e){return e.x}).y(function(e){return e.y}).curve($),n=i.append("path").attr("d",c(s)).attr("id","edge"+H).attr("class","relation");let r="";o.arrowMarkerAbsolute&&(r=window.location.protocol+"//"+window.location.host+window.location.pathname+window.location.search,r=r.replace(/\(/g,"\\("),r=r.replace(/\)/g,"\\)")),t.relation.lineType==1&&n.attr("class","relation dashed-line"),t.relation.lineType==10&&n.attr("class","relation dotted-line"),t.relation.type1!=="none"&&n.attr("marker-start","url("+r+"#"+g(t.relation.type1)+"Start)"),t.relation.type2!=="none"&&n.attr("marker-end","url("+r+"#"+g(t.relation.type2)+"End)");let f,h;const x=a.points.length;let b=M.calcLabelPosition(a.points);f=b.x,h=b.y;let u,m,w,k;if(x%2!==0&&x>1){let e=M.calcCardinalityPosition(t.relation.type1!=="none",a.points,a.points[0]),d=M.calcCardinalityPosition(t.relation.type2!=="none",a.points,a.points[x-1]);y.debug("cardinality_1_point "+JSON.stringify(e)),y.debug("cardinality_2_point "+JSON.stringify(d)),u=e.x,m=e.y,w=d.x,k=d.y}if(t.title!==void 0){const e=i.append("g").attr("class","classLabel"),d=e.append("text").attr("class","label").attr("x",f).attr("y",h).attr("fill","red").attr("text-anchor","middle").text(t.title);window.label=d;const l=d.node().getBBox();e.insert("rect",":first-child").attr("class","box").attr("x",l.x-o.padding/2).attr("y",l.y-o.padding/2).attr("width",l.width+o.padding).attr("height",l.height+o.padding)}y.info("Rendering relation "+JSON.stringify(t)),t.relationTitle1!==void 0&&t.relationTitle1!=="none"&&i.append("g").attr("class","cardinality").append("text").attr("class","type1").attr("x",u).attr("y",m).attr("fill","black").attr("font-size","6").text(t.relationTitle1),t.relationTitle2!==void 0&&t.relationTitle2!=="none"&&i.append("g").attr("class","cardinality").append("text").attr("class","type2").attr("x",w).attr("y",k).attr("fill","black").attr("font-size","6").text(t.relationTitle2),H++},J=function(i,a,t,o){y.debug("Rendering class ",a,t);const p=a.id,g={id:p,label:a.id,width:0,height:0},s=i.append("g").attr("id",o.db.lookUpDomId(p)).attr("class","classGroup");let c;a.link?c=s.append("svg:a").attr("xlink:href",a.link).attr("target",a.linkTarget).append("text").attr("y",t.textHeight+t.padding).attr("x",0):c=s.append("text").attr("y",t.textHeight+t.padding).attr("x",0);let n=!0;a.annotations.forEach(function(d){const l=c.append("tspan").text("«"+d+"»");n||l.attr("dy",t.textHeight),n=!1});let r=C(a);const f=c.append("tspan").text(r).attr("class","title");n||f.attr("dy",t.textHeight);const h=c.node().getBBox().height;let x,b,u;if(a.members.length>0){x=s.append("line").attr("x1",0).attr("y1",t.padding+h+t.dividerMargin/2).attr("y2",t.padding+h+t.dividerMargin/2);const d=s.append("text").attr("x",t.padding).attr("y",h+t.dividerMargin+t.textHeight).attr("fill","white").attr("class","classText");n=!0,a.members.forEach(function(l){_(d,l,n,t),n=!1}),b=d.node().getBBox()}if(a.methods.length>0){u=s.append("line").attr("x1",0).attr("y1",t.padding+h+t.dividerMargin+b.height).attr("y2",t.padding+h+t.dividerMargin+b.height);const d=s.append("text").attr("x",t.padding).attr("y",h+2*t.dividerMargin+b.height+t.textHeight).attr("fill","white").attr("class","classText");n=!0,a.methods.forEach(function(l){_(d,l,n,t),n=!1})}const m=s.node().getBBox();var w=" ";a.cssClasses.length>0&&(w=w+a.cssClasses.join(" "));const e=s.insert("rect",":first-child").attr("x",0).attr("y",0).attr("width",m.width+2*t.padding).attr("height",m.height+t.padding+.5*t.dividerMargin).attr("class",w).node().getBBox().width;return c.node().childNodes.forEach(function(d){d.setAttribute("x",(e-d.getBBox().width)/2)}),a.tooltip&&c.insert("title").text(a.tooltip),x&&x.attr("x2",e),u&&u.attr("x2",e),g.width=e,g.height=m.height+t.padding+.5*t.dividerMargin,g},C=function(i){let a=i.id;return i.type&&(a+="<"+I(i.type)+">"),a},Z=function(i,a,t,o){y.debug("Rendering note ",a,t);const p=a.id,g={id:p,text:a.text,width:0,height:0},s=i.append("g").attr("id",p).attr("class","classGroup");let c=s.append("text").attr("y",t.textHeight+t.padding).attr("x",0);const n=JSON.parse(`"${a.text}"`).split(`
`);n.forEach(function(x){y.debug(`Adding line: ${x}`),c.append("tspan").text(x).attr("class","title").attr("dy",t.textHeight)});const r=s.node().getBBox(),h=s.insert("rect",":first-child").attr("x",0).attr("y",0).attr("width",r.width+2*t.padding).attr("height",r.height+n.length*t.textHeight+t.padding+.5*t.dividerMargin).node().getBBox().width;return c.node().childNodes.forEach(function(x){x.setAttribute("x",(h-x.getBBox().width)/2)}),g.width=h,g.height=r.height+n.length*t.textHeight+t.padding+.5*t.dividerMargin,g},_=function(i,a,t,o){const{displayText:p,cssStyle:g}=a.getDisplayDetails(),s=i.append("tspan").attr("x",o.padding).text(p);g!==""&&s.attr("style",a.cssStyle),t||s.attr("dy",o.textHeight)},N={getClassTitleString:C,drawClass:J,drawEdge:Y,drawNote:Z};let T={};const E=20,L=function(i){const a=Object.entries(T).find(t=>t[1].label===i);if(a)return a[0]},R=function(i){i.append("defs").append("marker").attr("id","extensionStart").attr("class","extension").attr("refX",0).attr("refY",7).attr("markerWidth",190).attr("markerHeight",240).attr("orient","auto").append("path").attr("d","M 1,7 L18,13 V 1 Z"),i.append("defs").append("marker").attr("id","extensionEnd").attr("refX",19).attr("refY",7).attr("markerWidth",20).attr("markerHeight",28).attr("orient","auto").append("path").attr("d","M 1,1 V 13 L18,7 Z"),i.append("defs").append("marker").attr("id","compositionStart").attr("class","extension").attr("refX",0).attr("refY",7).attr("markerWidth",190).attr("markerHeight",240).attr("orient","auto").append("path").attr("d","M 18,7 L9,13 L1,7 L9,1 Z"),i.append("defs").append("marker").attr("id","compositionEnd").attr("refX",19).attr("refY",7).attr("markerWidth",20).attr("markerHeight",28).attr("orient","auto").append("path").attr("d","M 18,7 L9,13 L1,7 L9,1 Z"),i.append("defs").append("marker").attr("id","aggregationStart").attr("class","extension").attr("refX",0).attr("refY",7).attr("markerWidth",190).attr("markerHeight",240).attr("orient","auto").append("path").attr("d","M 18,7 L9,13 L1,7 L9,1 Z"),i.append("defs").append("marker").attr("id","aggregationEnd").attr("refX",19).attr("refY",7).attr("markerWidth",20).attr("markerHeight",28).attr("orient","auto").append("path").attr("d","M 18,7 L9,13 L1,7 L9,1 Z"),i.append("defs").append("marker").attr("id","dependencyStart").attr("class","extension").attr("refX",0).attr("refY",7).attr("markerWidth",190).attr("markerHeight",240).attr("orient","auto").append("path").attr("d","M 5,7 L9,13 L1,7 L9,1 Z"),i.append("defs").append("marker").attr("id","dependencyEnd").attr("refX",19).attr("refY",7).attr("markerWidth",20).attr("markerHeight",28).attr("orient","auto").append("path").attr("d","M 18,7 L9,13 L14,7 L9,1 Z")},F=function(i,a,t,o){const p=v().class;T={},y.info("Rendering diagram "+i);const g=v().securityLevel;let s;g==="sandbox"&&(s=B("#i"+a));const c=g==="sandbox"?B(s.nodes()[0].contentDocument.body):B("body"),n=c.select(`[id='${a}']`);R(n);const r=new O({multigraph:!0});r.setGraph({isMultiGraph:!0}),r.setDefaultEdgeLabel(function(){return{}});const f=o.db.getClasses(),h=Object.keys(f);for(const e of h){const d=f[e],l=N.drawClass(n,d,p,o);T[l.id]=l,r.setNode(l.id,l),y.info("Org height: "+l.height)}o.db.getRelations().forEach(function(e){y.info("tjoho"+L(e.id1)+L(e.id2)+JSON.stringify(e)),r.setEdge(L(e.id1),L(e.id2),{relation:e},e.title||"DEFAULT")}),o.db.getNotes().forEach(function(e){y.debug(`Adding note: ${JSON.stringify(e)}`);const d=N.drawNote(n,e,p,o);T[d.id]=d,r.setNode(d.id,d),e.class&&e.class in f&&r.setEdge(e.id,L(e.class),{relation:{id1:e.id,id2:e.class,relation:{type1:"none",type2:"none",lineType:10}}},"DEFAULT")}),P(r),r.nodes().forEach(function(e){e!==void 0&&r.node(e)!==void 0&&(y.debug("Node "+e+": "+JSON.stringify(r.node(e))),c.select("#"+(o.db.lookUpDomId(e)||e)).attr("transform","translate("+(r.node(e).x-r.node(e).width/2)+","+(r.node(e).y-r.node(e).height/2)+" )"))}),r.edges().forEach(function(e){e!==void 0&&r.edge(e)!==void 0&&(y.debug("Edge "+e.v+" -> "+e.w+": "+JSON.stringify(r.edge(e))),N.drawEdge(n,r.edge(e),r.edge(e).relation,p,o))});const u=n.node().getBBox(),m=u.width+E*2,w=u.height+E*2;W(n,w,m,p.useMaxWidth);const k=`${u.x-E} ${u.y-E} ${m} ${w}`;y.debug(`viewBox ${k}`),n.attr("viewBox",k)},z={draw:F},j={parser:G,db:S,renderer:z,styles:A,init:i=>{i.class||(i.class={}),i.class.arrowMarkerAbsolute=i.arrowMarkerAbsolute,S.clear()}};export{j as diagram};
