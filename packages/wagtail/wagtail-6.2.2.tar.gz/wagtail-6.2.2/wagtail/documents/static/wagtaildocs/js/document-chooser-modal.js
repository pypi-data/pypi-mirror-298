(()=>{"use strict";var e,o={4186:(e,o,r)=>{var t=r(1669),n=r.n(t),a=r(2614);class i extends a.C4{ajaxifyLinks(e,o){super.ajaxifyLinks(e,o),n()("a.upload-one-now").on("click",(e=>{const o=n()("#id_collection_id").val();o&&n()("#id_document-chooser-upload-collection").val(o),e.preventDefault()}))}}window.DOCUMENT_CHOOSER_MODAL_ONLOAD_HANDLERS=new i({searchInputDelay:50,creationFormFileFieldSelector:"#id_document-chooser-upload-file",creationFormTitleFieldSelector:"#id_document-chooser-upload-title",creationFormTabSelector:"#tab-upload",creationFormEventName:"wagtail:documents-upload"}).getOnLoadHandlers();class l extends a.ZZ{onloadHandlers=window.DOCUMENT_CHOOSER_MODAL_ONLOAD_HANDLERS}window.DocumentChooserModal=l},1669:e=>{e.exports=jQuery}},r={};function t(e){var n=r[e];if(void 0!==n)return n.exports;var a=r[e]={exports:{}};return o[e](a,a.exports,t),a.exports}t.m=o,e=[],t.O=(o,r,n,a)=>{if(!r){var i=1/0;for(u=0;u<e.length;u++){for(var[r,n,a]=e[u],l=!0,d=0;d<r.length;d++)(!1&a||i>=a)&&Object.keys(t.O).every((e=>t.O[e](r[d])))?r.splice(d--,1):(l=!1,a<i&&(i=a));if(l){e.splice(u--,1);var c=n();void 0!==c&&(o=c)}}return o}a=a||0;for(var u=e.length;u>0&&e[u-1][2]>a;u--)e[u]=e[u-1];e[u]=[r,n,a]},t.n=e=>{var o=e&&e.__esModule?()=>e.default:()=>e;return t.d(o,{a:o}),o},t.d=(e,o)=>{for(var r in o)t.o(o,r)&&!t.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:o[r]})},t.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),t.o=(e,o)=>Object.prototype.hasOwnProperty.call(e,o),t.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},t.j=884,(()=>{var e={884:0};t.O.j=o=>0===e[o];var o=(o,r)=>{var n,a,[i,l,d]=r,c=0;if(i.some((o=>0!==e[o]))){for(n in l)t.o(l,n)&&(t.m[n]=l[n]);if(d)var u=d(t)}for(o&&o(r);c<i.length;c++)a=i[c],t.o(e,a)&&e[a]&&e[a][0](),e[a]=0;return t.O(u)},r=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];r.forEach(o.bind(null,0)),r.push=o.bind(null,r.push.bind(r))})();var n=t.O(void 0,[321],(()=>t(4186)));n=t.O(n)})();