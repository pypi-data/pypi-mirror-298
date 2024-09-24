(()=>{"use strict";var t,e={7290:(t,e,i)=>{var s=i(2833),n=i(6032);class r{constructor(t,e,i,s,n,r){const a=t.forEach?t:[t],o=`:is(input,select,textarea,button)[name="${e}"]`;for(let t=0;t<a.length;t+=1){const e=a[t];if(e.nodeType===Node.ELEMENT_NODE){if(e.matches(o)){this.input=e;break}{const t=e.querySelector(o);if(t){this.input=t;break}}}}this.idForLabel=i,this.setState(s),this.parentCapabilities=n||new Map,this.options=r}getValue(){return this.input.value}getState(){return this.input.value}setState(t){this.input.value=t}getTextLabel(t){const e=this.getValue();if("string"!=typeof e)return null;const i=t&&t.maxLength;return i&&e.length>i?e.substring(0,i-1)+"…":e}focus(){this.input.focus()}setCapabilityOptions(t,e){Object.assign(this.parentCapabilities.get(t),e)}}class a{constructor(t,e){this.html=t,this.idPattern=e}boundWidgetClass=r;render(t,e,i,s,r,a={}){const o=this.html.replace(/__NAME__/g,e).replace(/__ID__/g,i),l=this.idPattern.replace(/__ID__/g,i),c=document.createElement("div");c.innerHTML=o.trim();const u=Array.from(c.childNodes);t.replaceWith(...u);const h=u.filter((t=>t.nodeType===Node.ELEMENT_NODE));return h.forEach((t=>{(0,n.v)(t)})),"object"==typeof a?.attributes&&Object.entries(a.attributes).forEach((([t,e])=>{h[0].setAttribute(t,e)})),new this.boundWidgetClass(1===h.length?h[0]:u,e,l,s,r,a)}}window.telepath.register("wagtail.widgets.Widget",a);class o extends r{getValue(){return this.input.checked}getState(){return this.input.checked}setState(t){this.input.checked=t}}window.telepath.register("wagtail.widgets.CheckboxInput",class extends a{boundWidgetClass=o});class l{constructor(t,e,i,s){this.element=t,this.name=e,this.idForLabel=i,this.isMultiple=!!this.element.querySelector(`input[name="${e}"][type="checkbox"]`),this.selector=`input[name="${e}"]:checked`,this.setState(s)}getValue(){return this.isMultiple?Array.from(this.element.querySelectorAll(this.selector)).map((t=>t.value)):this.element.querySelector(this.selector)?.value}getState(){return Array.from(this.element.querySelectorAll(this.selector)).map((t=>t.value))}setState(t){const e=this.element.querySelectorAll(`input[name="${this.name}"]`);for(let i=0;i<e.length;i+=1)e[i].checked=t.includes(e[i].value)}focus(){this.element.querySelector(`input[name="${this.name}"]`)?.focus()}}window.telepath.register("wagtail.widgets.RadioSelect",class extends a{boundWidgetClass=l});class c extends r{getTextLabel(){return Array.from(this.input.selectedOptions).map((t=>t.text)).join(", ")}getValue(){return this.input.multiple?Array.from(this.input.selectedOptions).map((t=>t.value)):this.input.value}getState(){return Array.from(this.input.selectedOptions).map((t=>t.value))}setState(t){const e=this.input.options;for(let i=0;i<e.length;i+=1)e[i].selected=t.includes(e[i].value)}}window.telepath.register("wagtail.widgets.Select",class extends a{boundWidgetClass=c});class u{constructor(t,e,i,s){this.widget=t,this.blockDef=e,this.addSibling=i,this.split=s,this.blockMax=i.getBlockMax(e.name),this.icon=e.meta.icon,this.description=e.meta.label,this.type=e.name}render({option:t}){const e="number"==typeof blockMax?` (${this.addSibling.getBlockCount(this.blockDef.name)}/${this.blockMax})`:"";return`${t.description}${e}`}onSelect({editorState:t}){const e=window.draftail.splitState(window.draftail.DraftUtils.removeCommandPalettePrompt(t));e.stateAfter.getCurrentContent().hasText()?setTimeout((()=>{e&&this.split.fn(e.stateBefore,e.stateAfter,e.shouldMoveCommentFn),setTimeout((()=>{this.addSibling.fn({type:this.blockDef.name})}),20)}),50):(this.widget.setState(e.stateBefore),setTimeout((()=>{this.addSibling.fn({type:this.blockDef.name})}),20))}}class h{constructor(t,e){this.widget=t,this.split=e,this.description=(0,s.AP)("Split block")}icon="cut";type="split";onSelect({editorState:t}){const e=window.draftail.splitState(window.draftail.DraftUtils.removeCommandPalettePrompt(t));setTimeout((()=>{e&&this.split.fn(e.stateBefore,e.stateAfter,e.shouldMoveCommentFn)}),50)}}class p{constructor(t,e,i){this.input=t,this.capabilities=new Map(i),this.options=e;const[,s]=draftail.initEditor("#"+this.input.id,this.getFullOptions(),document.currentScript);this.setDraftailOptions=s}getValue(){return this.input.value}getState(){return this.input.draftailEditor.getEditorState()}setState(t){this.input.draftailEditor.onChange(t)}getTextLabel(t){const e=t&&t.maxLength;if(!this.input.value)return"";const i=JSON.parse(this.input.value);if(!i||!i.blocks)return"";let s="";for(const t of i.blocks)if(t.text&&(s+=s?" "+t.text:t.text,e&&s.length>e))return s.substring(0,e-1)+"…";return s}focus(){setTimeout((()=>{this.input.draftailEditor.focus()}),50)}setCapabilityOptions(t,e){const i=Object.assign(this.capabilities.get(t),e);this.capabilities.set(t,i),this.setDraftailOptions(this.getFullOptions())}getCapabilityOptions(t){const e={},i=t,n=i.get("split"),r=i.get("addSibling");let a=[];return n&&(a=(r&&r.enabled&&n.enabled?r.blockGroups:[]).map((([t,e])=>{const i=e.map((t=>new u(this,t,r,n)));return{label:t||(0,s.AP)("Blocks"),type:`streamfield-${t}`,items:i}})),n.enabled&&a.push({label:"Actions",type:"custom-actions",items:[new h(this,n)]})),e.commands=[{type:"blockTypes"},{type:"entityTypes"},...a],e}getFullOptions(){return{...this.options,...this.getCapabilityOptions(this.capabilities)}}}window.telepath.register("wagtail.widgets.DraftailRichTextArea",class{constructor(t){this.options=t}render(t,e,i,s,n,r={}){const a=document.createElement("input");a.type="hidden",a.id=i,a.name=e,"object"==typeof r?.attributes&&Object.entries(r.attributes).forEach((([t,e])=>{a.setAttribute(t,e)}));const o=!!s.getCurrentContent;a.value=o?"null":s,t.appendChild(a);const l=new p(a,{...this.options,...r},n);return o&&l.setState(s),l}});class d extends a{constructor(t){super(),this.options=t}render(t,e,i,s){const n=document.createElement("input");n.type="text",n.name=e,n.id=i,t.replaceWith(n),this.initChooserFn(i,this.options);const r={getValue:()=>n.value,getState:()=>n.value,setState(t){n.value=t},focus(t){t&&t.soft||n.focus()},idForLabel:i};return r.setState(s),r}}window.telepath.register("wagtail.widgets.AdminDateInput",class extends d{initChooserFn=window.initDateChooser}),window.telepath.register("wagtail.widgets.AdminTimeInput",class extends d{initChooserFn=window.initTimeChooser}),window.telepath.register("wagtail.widgets.AdminDateTimeInput",class extends d{initChooserFn=window.initDateTimeChooser}),window.telepath.register("wagtail.errors.ValidationError",class{constructor(t){this.messages=t}})}},i={};function s(t){var n=i[t];if(void 0!==n)return n.exports;var r=i[t]={exports:{}};return e[t](r,r.exports,s),r.exports}s.m=e,t=[],s.O=(e,i,n,r)=>{if(!i){var a=1/0;for(u=0;u<t.length;u++){for(var[i,n,r]=t[u],o=!0,l=0;l<i.length;l++)(!1&r||a>=r)&&Object.keys(s.O).every((t=>s.O[t](i[l])))?i.splice(l--,1):(o=!1,r<a&&(a=r));if(o){t.splice(u--,1);var c=n();void 0!==c&&(e=c)}}return e}r=r||0;for(var u=t.length;u>0&&t[u-1][2]>r;u--)t[u]=t[u-1];t[u]=[i,n,r]},s.n=t=>{var e=t&&t.__esModule?()=>t.default:()=>t;return s.d(e,{a:e}),e},s.d=(t,e)=>{for(var i in e)s.o(e,i)&&!s.o(t,i)&&Object.defineProperty(t,i,{enumerable:!0,get:e[i]})},s.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"==typeof window)return window}}(),s.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),s.r=t=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},s.j=136,(()=>{var t={136:0};s.O.j=e=>0===t[e];var e=(e,i)=>{var n,r,[a,o,l]=i,c=0;if(a.some((e=>0!==t[e]))){for(n in o)s.o(o,n)&&(s.m[n]=o[n]);if(l)var u=l(s)}for(e&&e(i);c<a.length;c++)r=a[c],s.o(t,r)&&t[r]&&t[r][0](),t[r]=0;return s.O(u)},i=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];i.forEach(e.bind(null,0)),i.push=e.bind(null,i.push.bind(i))})();var n=s.O(void 0,[321],(()=>s(7290)));n=s.O(n)})();