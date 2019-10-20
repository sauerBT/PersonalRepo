module.exports=__NEXT_REGISTER_PAGE("/_error",function(){var e=webpackJsonp([34],{813:function(e,t,r){e.exports=r(814)},814:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:true});var a=r(1);var n=r.n(a);var o=r(2);var i=r.n(o);var s=r(3);var l=r.n(s);var c=r(235);var m=r.n(c);var p=r(15);var u=r.n(p);var f=r(602);var h=r(10);var d=r(4);var b=["*{box-sizing:border-box;}","html,body{min-height:100vh;margin:0;padding:0;"+d["a"].white+";}",".ErrorPage{width:100vw;height:100vh;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-flex-direction:row;-ms-flex-direction:row;flex-direction:row;-webkit-box-pack:center;-webkit-justify-content:center;-ms-flex-pack:center;justify-content:center;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;text-align:center;}",".centered{-webkit-flex:0 0 auto;-ms-flex:0 0 auto;flex:0 0 auto;}","p{margin-bottom:0;}",".image{margin-bottom:30px;}",".image img{max-width:75vw;max-height:40vh;}"];b.__hash="1330784656";b.__scoped=["*.jsx-2570729873{box-sizing:border-box;}","html.jsx-2570729873,body.jsx-2570729873{min-height:100vh;margin:0;padding:0;"+d["a"].white+";}",".ErrorPage.jsx-2570729873{width:100vw;height:100vh;display:-webkit-box;display:-webkit-flex;display:-ms-flexbox;display:flex;-webkit-flex-direction:row;-ms-flex-direction:row;flex-direction:row;-webkit-box-pack:center;-webkit-justify-content:center;-ms-flex-pack:center;justify-content:center;-webkit-align-items:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center;text-align:center;}",".centered.jsx-2570729873{-webkit-flex:0 0 auto;-ms-flex:0 0 auto;flex:0 0 auto;}","p.jsx-2570729873{margin-bottom:0;}",".image.jsx-2570729873{margin-bottom:30px;}",".image.jsx-2570729873 img.jsx-2570729873{max-width:75vw;max-height:40vh;}"];b.__scopedHash="2570729873";var v=b;var x=["#__next-error{display:none;}"];x.__hash="2261150928";x.__scoped=["#__next-error.jsx-3720468689{display:none;}"];x.__scopedHash="3720468689";var g=x;var y=function e(){return n.a.createElement(l.a,{styleId:g.__hash,css:g})};var w=function e(t){var r=t.statusCode,a=t.isDevelopment;return n.a.createElement("div",{className:"ErrorPage"},n.a.createElement(m.a,null,n.a.createElement("meta",{charSet:"utf-8"}),n.a.createElement("meta",{httpEquiv:"X-UA-Compatible",content:"IE=edge,chrome=1"}),n.a.createElement("meta",{name:"viewport",content:"width=device-width, initial-scale=1, user-scalable=no"}),n.a.createElement("title",null,"Oops...")),n.a.createElement("div",{className:"centered"},n.a.createElement("h1",null,"Oops..."),n.a.createElement("p",null,n.a.createElement("small",null,"Looks like something crashed.")),n.a.createElement("div",{className:"image"},n.a.createElement("img",{src:"http://datacamp-community.s3.amazonaws.com/"+(r>=500?"9d763934-a825-4f34-857e-a325b1b1e6df":"79dc8289-58bd-4669-ab8b-10a9f16a583b"),alt:""})),n.a.createElement(u.a,{href:"/community"},n.a.createElement(h["a"],{primary:true},"Take Me Back to Safety"))),!a&&y(),n.a.createElement(l.a,{styleId:v.__hash,css:v}),n.a.createElement(l.a,{styleId:f["a"].__hash,css:f["a"]}),n.a.createElement("link",{href:"https://fonts.googleapis.com/css?family=Lato:300,700",rel:"stylesheet"}))};var _=w;var E=r(6);var k=r.n(E);var j=function(){function e(e,t){for(var r=0;r<t.length;r++){var a=t[r];a.enumerable=a.enumerable||false;a.configurable=true;if("value"in a)a.writable=true;Object.defineProperty(e,a.key,a)}}return function(t,r,a){if(r)e(t.prototype,r);if(a)e(t,a);return t}}();function O(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function C(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t&&("object"===typeof t||"function"===typeof t)?t:e}function P(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:false,writable:true,configurable:true}});if(t)Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t}var I=r(844)(E["SENTRY_KEY"],E["SENTRY_CONFIG"]);var N=function(e){P(t,e);function t(){var e;var r,a,o;O(this,t);for(var i=arguments.length,s=Array(i),l=0;l<i;l++)s[l]=arguments[l];return o=(r=(a=C(this,(e=t.__proto__||Object.getPrototypeOf(t)).call.apply(e,[this].concat(s))),a),a.callSentry=function(){I.captureException(a.props.error&&a.props.error.message||"",{extra:{isDevelopment:a.props.isDevelopment,statusCode:a.props.statusCode,pathname:a.props.pathname,query:a.props.query,error:a.props.error}})},a.render=function(){return n.a.createElement(_,a.props)},r),C(a,o)}j(t,null,[{key:"getInitialProps",value:function e(t){var r=t.req,a=t.res,n=t.jsonPageRes,o=t.err,i=t.pathname,s=t.query;var l=r.clientConfig.isDevelopment;var c=a?a.statusCode:n?n.status:o?o.statusCode:null;return{isDevelopment:l,statusCode:c,pathname:i,query:s,error:o}}}]);return t}(n.a.Component);var S=t["default"]=N},844:function(e,t){e.exports=function(e,t){}}},[813]);return{page:e.default}});