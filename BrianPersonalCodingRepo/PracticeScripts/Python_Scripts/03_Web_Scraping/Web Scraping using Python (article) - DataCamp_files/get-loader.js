(function(){'use strict';var constants={cookieMaxSize:3072,loggerMaxSize:1000,msInDay:24*60*60*1000,msIn30Days:30*24*60*60*1000,visitsMaxSize:10};var WisePopsStorage={cid:'42073',siteHash:'VswVJn7o4J',baseUrl:{app:'//app.wisepops.com',popup:'//popup.wisepops.com',tracking:'//tracking.wisepops.com'},gaTrackedEvents:'',browserStorageUsed:false,cookieNamePersistent:'wisepops',cookieNameSession:'wisepops_session',cookieNameProperties:'wisepops_props',cookieNameVisits:'wisepops_visits',cookieNameNoShow:'wisepops_noshow',arrivalOnPage:null,lastRequestInterval:null,noShow:null,persistentData:{csd:1,popups:{},sub:0,ucrn:null,cid:null,v:4},sessionData:{arrivalOnSite:null,mtime:null,pageviews:0,popups:{},src:null,utm:{}},customProperties:{},visits:[],getCookie:function(keyName){var name=keyName+'=';var ca=document.cookie.split(';');for(var i=0;i<ca.length;i++){var c=ca[i];while(c.charAt(0)==' '){c=c.substring(1);}
if(c.indexOf(name)==0){c=c.substring(name.length,c.length);if(c.charAt(0)==='{'||c.charAt(0)==='['){c=unescape(c);}else{c=decodeURIComponent(c);}
return c;}}
return null;},getBrowserStorage:function(keyName){var storage=(keyName===this.cookieNameSession?window.sessionStorage:window.localStorage);if(storage){return storage.getItem(keyName);}else{return null;}},getStorage:function(keyName){if(this.isBrowserStorageUsed()){return this.getBrowserStorage(keyName);}else{return this.getCookie(keyName);}},setCookie:function(keyName,value,isSession,path,noCrossSubDomain){var expirationDate='';if(!isSession||typeof isSession==='number'){var d=new Date();var daysBeforeExpire=isSession||(365*2);d.setTime(d.getTime()+(daysBeforeExpire*constants.msInDay));expirationDate='expires='+d.toUTCString();}
var domain='';var hostname=this.getHostname(true);if(!noCrossSubDomain&&this.getCrossSubDomain()&&hostname.subDomainSkipped){domain='domain=.'+hostname.hostname+'; ';}
if(typeof path==='undefined'){path='path=/; ';}else if(typeof path==='string'){path='path='+path+'; ';}else{path='';}
var cookieValue=keyName+'='+encodeURIComponent(value)+'; '+path+domain+expirationDate;if(cookieValue.length>constants.cookieMaxSize){throw 'Cookie is too big ('+keyName+')';}
document.cookie=cookieValue;return true;},setBrowserStorage:function(keyName,value,isSession){var storage=isSession?window.sessionStorage:window.localStorage;if(!storage){return false;}
storage.setItem(keyName,value);return true;},setStorage:function(keyName,value,isSession){if(this.isBrowserStorageUsed()){return this.setBrowserStorage(keyName,value,isSession);}else{return this.setCookie(keyName,value,isSession);}},testStorage:function(){var keyName='wisepops_test';var isSuccess=this.setStorage(keyName,'test',true);if(isSuccess){this.removeStorage(keyName);}
return isSuccess;},removeCookie:function(keyName){this.setCookie(keyName,'',-1);this.setCookie(keyName,'',-1,false);this.setCookie(keyName,'',-1,window.location.pathname);this.setCookie(keyName,'',-1,undefined,true);this.setCookie(keyName,'',-1,false,true);this.setCookie(keyName,'',-1,window.location.pathname,true);},removeBrowserStorage:function(keyName){if(window.localStorage){window.localStorage.removeItem(keyName);}
if(window.sessionStorage){window.sessionStorage.removeItem(keyName);}},removeStorage:function(keyName){if(this.isBrowserStorageUsed()){this.removeBrowserStorage(keyName);}else{this.removeCookie(keyName);}},isBrowserStorageUsed:function(checkRealStorage){if(checkRealStorage){return!!this.getBrowserStorage(this.cookieNamePersistent);}else{return this.browserStorageUsed;}},setBrowserStorageUsed:function(useBrowserStorage,migrate){var hasChanged=useBrowserStorage!==this.browserStorageUsed;if(hasChanged&&migrate){if(!this.testStorage()){throw 'Storage engine not available';}
this.removeStorage(this.cookieNamePersistent);this.removeStorage(this.cookieNameSession);this.removeStorage(this.cookieNameProperties);this.removeStorage(this.cookieNameVisits);this.removeStorage(this.cookieNameNoShow);}
this.browserStorageUsed=useBrowserStorage;if(hasChanged&&migrate){this._save();}
return hasChanged;},getHostname:function(skipSubDomain,hostname){hostname=hostname||window.location.hostname;var subDomainSkipped=skipSubDomain;if(skipSubDomain){var domain=hostname.match(/[a-z0-9][a-z0-9\-]+\.[a-z.]{2,6}$/i);if(domain&&domain[0]){hostname=domain[0];}else{subDomainSkipped=false;}}
return{hostname:hostname,subDomainSkipped:subDomainSkipped};},getUrlParameter:function(name,query){query=query||window.location.search.substr(1);var vars=query.split('&');for(var i=0;i<vars.length;i++){var pair=vars[i].split('=');pair[0]=decodeURIComponent(pair[0]);if(pair[0]===name&&pair[1]){return decodeURIComponent(pair[1]);}}
return null;},getPageViewCount:function(){return this.sessionData.pageviews;},incrementPageViewCount:function(){if(this.isReferrerExternal()&&!WisePopsApi.pageviewCalled){this.sessionData.pageviews=1;}else{this.sessionData.pageviews++;}
this._saveSession();},isReferrerExternal:function(referrer,hostname){referrer=referrer||document.referrer;var external=(referrer==='');if(referrer!==''){var currentHostname=this.getHostname(this.getCrossSubDomain(),hostname).hostname;var parsedReferrer=document.createElement('a');parsedReferrer.href=referrer;external=(parsedReferrer.hostname.indexOf(currentHostname)===-1);}
return external;},setSource:function(referrer,hostname){referrer=referrer||document.referrer;if(this.isReferrerExternal(referrer,hostname)&&referrer){this.sessionData.src=referrer;this._saveSession();}},getSource:function(){return this.sessionData.src;},setUtmParameters:function(query){var parameters=['source','medium','campaign','term','content','gclid'];var specials=['gclid'];for(var i=0;i<parameters.length;i++){var paramName=parameters[i];if(specials.indexOf(paramName)===-1){paramName='utm_'+paramName;}
var value=this.getUrlParameter(paramName,query);if(value){if(specials.indexOf(paramName)>-1){value='yes';}
this.sessionData.utm[parameters[i]]=value;}}},getUtmParameters:function(){return this.sessionData.utm;},setArrivalOnPage:function(){var date=new Date();if(!this.arrivalOnPage&&WisePopsApi.object){date.setTime(WisePopsApi.object.l);}
this.arrivalOnPage=date;},getArrivalOnPage:function(){if(!this.arrivalOnPage){this.setArrivalOnPage();}
return this.arrivalOnPage;},setArrivalOnSite:function(){if(!this.sessionData.arrivalOnSite||this.isReferrerExternal()){this.sessionData.arrivalOnSite=this.getArrivalOnPage().toJSON();}},getArrivalOnSite:function(){if(!this.sessionData.arrivalOnSite){this.setArrivalOnSite();}
if(typeof this.sessionData.arrivalOnSite!=='object'){try{this.sessionData.arrivalOnSite=new Date(this.sessionData.arrivalOnSite);}catch(exception){WisePopsApi.log('error','Invalid date format for arrival on site');}}
return this.sessionData.arrivalOnSite;},addVisit:function(){if(this.isReferrerExternal()||!this.visits.length){if(this.visits.unshift(this.getArrivalOnPage().toJSON())>constants.visitsMaxSize){this.visits=this.visits.slice(0,constants.visitsMaxSize);}
this._saveVisits();}},getVisits:function(){return this.visits;},getDoNotDisplay:function(){return!!this.noShow;},setDoNotDisplay:function(doNotDisplay){if(typeof doNotDisplay==='undefined'){doNotDisplay=true;}
if(doNotDisplay){var noShowUntil=new Date();noShowUntil.setTime(noShowUntil.getTime()+constants.msIn30Days);this.noShow=noShowUntil.toJSON();}else{this.noShow=null;}
this._saveNoShow();},getPopup:function(popId){if(this.persistentData.popups[popId]){return this.persistentData.popups[popId];}},getPopupIds:function(){return Object.keys(this.persistentData.popups);},getSessionPopups:function(){return this.sessionData.popups;},addSessionPopupId:function(popId){this.sessionData.popups[popId]=0;this._saveSession();},incrementSessionPagesElapsed:function(){for(var popId in this.sessionData.popups){if(this.sessionData.popups.hasOwnProperty(popId)){this.sessionData.popups[popId]++;}}
this._saveSession();},getDisplayCount:function(popId){if(this.getPopup(popId)&&this.getPopup(popId).dc){return this.getPopup(popId).dc;}else{return 0;}},getLastDisplayedInterval:function(popId){if(this.getPopup(popId)){var diff=Math.abs(new Date(this.getPopup(popId).d)-new Date());return Math.floor((diff/1000)/60);}else{return 0;}},setDisplayed:function(popId){var date=(new Date()).toJSON();if(this.getPopup(popId)){this.getPopup(popId).dc++;this.getPopup(popId).d=date;}else{this.persistentData.popups[popId]={dc:1,d:date};}
this._saveStored();this.addSessionPopupId(popId);return true;},isConverted:function(popId){return!!(this.getPopup(popId)&&this.getPopup(popId).c);},setConverted:function(popId){if(this.getPopup(popId)){var date=new Date();this.getPopup(popId).c=date.toJSON();this._saveStored();return true;}else{return false;}},hasAnySubscription:function(){return!!this.persistentData.sub;},setSubscribed:function(popId){if(this.getPopup(popId)){this.persistentData.sub=1;this._saveStored();return true;}else{return false;}},getLastDisplayedAndConvertedPopups:function(){var displayPopId=null;var displayDate=null;var convertPopId=null;var convertDate=null;var date=null;for(var popId in this.persistentData.popups){if(this.persistentData.popups.hasOwnProperty(popId)){date=new Date(this.persistentData.popups[popId].d);if(displayDate===null||date.getTime()>displayDate.getTime()){displayPopId=popId;displayDate=date;}
if(this.persistentData.popups[popId].c){date=new Date(this.persistentData.popups[popId].c);if(convertDate===null||date.getTime()>convertDate.getTime()){convertPopId=popId;convertDate=date;}}}}
return{displayPopId:displayPopId,displayDate:displayDate,convertPopId:convertPopId,convertDate:convertDate};},removeOldestTrackedPopup:function(){var popIdToRemove=null;var oldestDisplayDate=null;for(var popId in this.persistentData.popups){if(this.persistentData.popups.hasOwnProperty(popId)){var displayDate=new Date(this.persistentData.popups[popId].d);if(oldestDisplayDate===null||displayDate.getTime()<oldestDisplayDate.getTime()){oldestDisplayDate=displayDate;popIdToRemove=popId;}}}
if(popIdToRemove){delete this.persistentData.popups[popIdToRemove];}
return popIdToRemove;},getUcrn:function(){if(this.persistentData.ucrn){return this.persistentData.ucrn;}
return false;},generateUcrn:function(){return this.persistentData.ucrn=Math.floor(Math.random()*100);},getCustomProperties:function(){for(var key in this.customProperties){if(this.customProperties.hasOwnProperty(key)){return this.customProperties;}}
return null;},addCustomProperties:function(properties,reset){if(reset){this.customProperties=properties;}else{this.customProperties=this.mergeObjects(this.customProperties,properties);}
this._saveCustomProperties();},dropCustomProperties:function(properties){for(var i=0;i<properties.length;i++){if(this.customProperties.hasOwnProperty(properties[i])){delete this.customProperties[properties[i]];}}
this._saveCustomProperties();},getCrossSubDomain:function(){return!!this.persistentData.csd;},setCrossSubDomain:function(crossSubDomain){this.persistentData.csd=crossSubDomain*1;},isEventGATracked:function(event){return!!event&&event.length&&this.gaTrackedEvents.indexOf(event)>-1;},_init:function(){this._initBrowserStorageUsed();this._initStored();this._initSession();this._initCustomProperties();this._initVisits();this._initNoShow();this.migrateCookieFormat();},_initBrowserStorageUsed:function(){this.setBrowserStorageUsed(this.isBrowserStorageUsed(true),false);},_initStored:function(){var cookie=this.getStorage(this.cookieNamePersistent);if(cookie){try{cookie=JSON.parse(cookie);if(cookie.cid&&cookie.cid!==this.cid){WisePopsApi.log('error','Conflict between accounts: '+cookie.cid+'/'+this.cid);}
cookie.cid=this.cid;if(!cookie.v){cookie.v=0;}
this.persistentData=this.mergeObjects(this.persistentData,cookie);}catch(exception){WisePopsApi.log('error','Cookie format corrupted');cookie=null;}}
if(!cookie){this.persistentData.cid=this.cid;this.generateUcrn();}
this._saveStored();if(!this.isBrowserStorageUsed()&&!this.getCookie(this.cookieNamePersistent)&&this.getCrossSubDomain()){this.setCrossSubDomain(false);this._initStored();}},_initSession:function(){var cookie=this.getStorage(this.cookieNameSession);if(cookie){try{cookie=JSON.parse(cookie);if(this.isSessionCookieRecent(cookie.mtime,Date.now())){this.sessionData=this.mergeObjects(this.sessionData,cookie);}}catch(exception){cookie=null;}}
this.setSource();this.setUtmParameters();this._saveSession();},isSessionCookieRecent:function(mtime,now){mtime=Date.parse(mtime);var diff=(mtime?now-mtime:0);return diff<2*60*60*1000;},_initCustomProperties:function(){var cookie=this.getStorage(this.cookieNameProperties);if(cookie){try{cookie=JSON.parse(cookie);this.customProperties=this.mergeObjects(this.customProperties,cookie);}catch(exception){cookie=null;}}},_initVisits:function(){var cookie=this.getStorage(this.cookieNameVisits);if(cookie){try{cookie=JSON.parse(cookie);this.visits=cookie;}catch(exception){cookie=null;}}},_initNoShow:function(){var value=this.getStorage(this.cookieNameNoShow);if(value==1){this.setDoNotDisplay(true);}else if(value){if(this.isNoShowDateReached(value,Date.now())){this.removeStorage(this.cookieNameNoShow);}else{this.noShow=value;}}},isNoShowDateReached:function(noShowUntil,now){noShowUntil=Date.parse(noShowUntil);return isNaN(noShowUntil)||noShowUntil<now;},mergeObjects:function(obj1,obj2){for(var propName in obj2){if(obj2.hasOwnProperty(propName)){obj1[propName]=obj2[propName];}}
return obj1;},migrateCookieFormat:function(){var hasChange=false;if(!this.persistentData.v||this.persistentData.v<4){hasChange=true;this.persistentData.v=4;delete this.persistentData.version;this.persistentData.csd=this.persistentData.cross_subdomain*1;delete this.persistentData.cross_subdomain;if(this.visits.length===0&&this.persistentData.last_req_date){this.visits.push(this.persistentData.last_req_date);}
delete this.persistentData.last_req_date;this.migratePopupsKeys();this.removeStorage(this.cookieNamePersistent);this.removeStorage(this.cookieNameProperties);}
if(hasChange){this._save();}},migratePopupsKeys:function(){if(this.persistentData.popins){for(var popId in this.persistentData.popins){if(this.persistentData.popins.hasOwnProperty(popId)){this.persistentData.popups[popId]={d:this.persistentData.popins[popId].display_date,dc:this.persistentData.popins[popId].display_count};if(this.persistentData.popins[popId].converted){this.persistentData.popups[popId].c=this.persistentData.popins[popId].converted;}
if(this.persistentData.popins[popId].subscribed){this.persistentData.sub=1;}}}
delete this.persistentData.popins;}
if(this.sessionData.popins){this.sessionData.popups=this.sessionData.popins;delete this.sessionData.popins;}},_save:function(){this._saveStored();this._saveSession();this._saveCustomProperties();this._saveVisits();this._saveNoShow();},_saveStored:function(){try{var jsonData=JSON.stringify(this.persistentData);this.setStorage(this.cookieNamePersistent,jsonData);}catch(exception){if(this.getPopupIds().length){var removedPopId=this.removeOldestTrackedPopup();WisePopsApi.log('warn','Removing info about popup #'+removedPopId+' to make persistent cookie lighter');this._saveStored();}else{throw exception;}}},_saveSession:function(){try{this.sessionData.mtime=(new Date()).toJSON();var jsonData=JSON.stringify(this.sessionData);this.setStorage(this.cookieNameSession,jsonData,true);}catch(exception){if(Object.keys(this.getSessionPopups()).length){WisePopsApi.log('warn',exception);this.sessionData.popups={};this._saveSession();}else{throw exception;}}},_saveCustomProperties:function(){var jsonData=JSON.stringify(this.customProperties);if(jsonData.length<=2){this.removeStorage(this.cookieNameProperties);}else{this.setStorage(this.cookieNameProperties,jsonData);}},_saveVisits:function(){this.setStorage(this.cookieNameVisits,JSON.stringify(this.visits));},_saveNoShow:function(){if(this.noShow){this.setStorage(this.cookieNameNoShow,this.noShow);}else{this.removeStorage(this.cookieNameNoShow);}}};var WisePopsApi={objectName:window['WisePopsObject'],object:null,disabled:false,pageviewCalled:false,trackSignupCalled:{},logger:[],loggerLevels:['none','error','warn','info','debug','trace'],loggerDisplayLevel:null,_init:function(){if(!this.objectName){this._initObject();}
this.object=window[this.objectName];if(this.object._api){this.object._api.log('warn','Loader already initialized, consider using wisepops("pageview") instead');this.object._api.pageviewAction();}else{this.object._api=WisePopsApi;this.object._storage=WisePopsStorage;var insideIframe=false;try{insideIframe=(window.self!==window.top);}catch(e){insideIframe=true;}
if(navigator.cookieEnabled!==true){this.log('error','Cookies need to be enabled');this.disabled=true;}else if(insideIframe){this.log('info','Disabled inside iframe');this.disabled=true;}else if(WisePopsStorage.getDoNotDisplay()){this.log('info','Disabled for 30 days');this.disabled=true;}
this._initQueue();if(this.loggerDisplayLevel===null){this.logAction('error');}}},_initObject:function(){var retry=5;while((!this.objectName||window[this.objectName])&&retry--){this.objectName='wisepops'+Math.floor(Math.random()*1000);}
if(window[this.objectName]){throw 'Wisepops - Could not initialize function because of name conflict';}
var that=this;window['WisePopsObject']=this.objectName;window[this.objectName]=function(){(window[that.objectName].q=window[that.objectName].q||[]).push(arguments);};window[this.objectName].l=1*new Date();},_initQueue:function(){var that=this;this.object.q=this.object.q||[];var qOldPush=this.object.q.push;this.object.q.push=function(args){if(that.object.q.length){qOldPush.apply(that.object.q,arguments);}else{that._dispatch(args);}};this._initLoaderCallback();for(var i=0;i<this.object.q.length;i++){this._dispatch(this.object.q[i]);}
this.object.q.length=0;if(!this.pageviewCalled){this.pageviewAction();}},_initLoaderCallback:function(){var that=this;function executeLoaderCallback(callback){if(typeof callback==='function'){try{callback(that.object);}catch(exception){that.log('error','LoaderCallback - '+exception);}}}
executeLoaderCallback(window['WisePopsLoaderCallback']);Object.defineProperty(window,'WisePopsLoaderCallback',{set:executeLoaderCallback});},_dispatch:function(args){this.log('debug','Dispatch',{functionName:args[0],properties:args[1],value:args[2]});var actionName=args[0]+'Action';if(!args[0]||!this[actionName]){this.log('error','Unkown method "'+args[0]+'"');}else{this[actionName](args[1],args[2]);}},pageviewAction:function(){WisePopsStorage.setArrivalOnPage();if(!this.pageviewCalled){WisePopsStorage.setArrivalOnSite();WisePopsStorage.addVisit();}
if(!this.disabled){WisePopsStorage.incrementPageViewCount();WisePopsStorage.incrementSessionPagesElapsed();this._myWisepop();}
this.pageviewCalled=true;},eventAction:function(eventName){if(!eventName||typeof eventName!=='string'){this.log('error','Method "event" requires an event name as 2nd parameter');}else if(!this.disabled){if(eventName.length>50){this.log('warn','The event name cannot exceed 50 characters');eventName=eventName.substr(0,50);}
this._myWisepop(eventName);}},_myWisepop:function(event){var logMsg='Resolving display scenarios for '+(event?'custom event "'+event+'"':'pageview');var customProperties=WisePopsStorage.getCustomProperties();this.log('info',logMsg,customProperties);var params={cid:WisePopsStorage.cid,site:WisePopsStorage.siteHash,ucrn:WisePopsStorage.getUcrn(),url:document.location,ref:document.referrer,pageviews:WisePopsStorage.getPageViewCount(),v:WisePopsStorage.getVisits().join(',')};if(WisePopsStorage.getSource()){params.src=WisePopsStorage.getSource();}
if(event){params.e=event;}
if(WisePopsStorage.getPopupIds()){var popupIds=WisePopsStorage.getPopupIds();for(var i=0;i<popupIds.length;i++){var popupId=popupIds[i];params['d['+popupId+']']=WisePopsStorage.getLastDisplayedInterval(popupId);if(WisePopsStorage.isConverted(popupId)){params['c['+popupId+']']=1;}
params['dc['+popupId+']']=WisePopsStorage.getDisplayCount(popupId);}}
var sessionPopups=WisePopsStorage.getSessionPopups();for(var popId in sessionPopups){if(sessionPopups.hasOwnProperty(popId)){params['ds['+popId+']']=sessionPopups[popId];}}
if(WisePopsStorage.hasAnySubscription()){params.sub=1;}
var utm=WisePopsStorage.getUtmParameters();for(var key1 in utm){if(utm.hasOwnProperty(key1)){params['utm['+encodeURIComponent(key1)+']']=utm[key1];}}
if(customProperties){for(var key2 in customProperties){if(customProperties.hasOwnProperty(key2)){params['p['+encodeURIComponent(key2)+']']=customProperties[key2];}}}
this._myWisepopsCall(params);},_myWisepopsCall:function(params){var that=this;var url=WisePopsStorage.baseUrl.popup+'/my-wisepop';var paramString='';for(var key in params){if(params.hasOwnProperty(key)){paramString+=key+'='+encodeURIComponent(params[key])+'&';}}
if(paramString.length){paramString=paramString.slice(0,-1);}
var xhr=null;if(window.XMLHttpRequest){xhr=new window.XMLHttpRequest();if(!('withCredentials'in xhr)){xhr=null;}else{xhr.withCredentials=true;}}
if(!xhr&&window.XDomainRequest){xhr=new window.XDomainRequest();this.log('info','Using XDomainRequest instead of XMLHttpRequest CORS');}
if(xhr){xhr.onload=function(){var response=JSON.parse(this.responseText);if(response.status==='ok'){var popupIds=[];var version=null;for(var i=0;i<response.popups.length;i++){popupIds.push(response.popups[i].id);version=response.popups[i].v;}
if(popupIds.length){var s=document.createElement('script');s.type='text/javascript';s.async=true;s.src=WisePopsStorage.baseUrl.app+'/shared/wisepops/'+response.hashPath+'/'
+popupIds.join('-')+'.js?v='+encodeURIComponent(version);var s2=document.getElementsByTagName('script')[0];s2.parentNode.insertBefore(s,s2);}else{that.log('info','No matching scenario');}}else{that.log('error',response.message||'An internal error occurred');}};xhr.open('POST',url,true);xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');xhr.setRequestHeader('Accept','application/json');xhr.send(paramString);}else{this.log('warn','Cannot use XMLHttpRequest CORS');url+='?'+paramString;var s=document.createElement('script');s.type='text/javascript';s.async=true;s.src=url;var s2=document.getElementsByTagName('script')[0];s2.parentNode.insertBefore(s,s2);}},propertiesAction:function(properties,reset){if(!properties||!(properties instanceof Object)){this.log('error','Method "properties" requires an object as 2nd parameter');}else{var verifiedProperties={};var droppedProperties=[];var allowedTypes=['string','number'];for(var key in properties){if(properties.hasOwnProperty(key)){if(properties[key]===null||properties[key]===undefined){droppedProperties.push(key);}else if(allowedTypes.indexOf(typeof properties[key])===-1&&!(properties[key]instanceof Date)){this.log('error','Property "'+key+'" cannot an instance of "'+typeof properties[key]+'"');}else if(key.length>50||properties[key].toString().length>255){this.log('error','Property "'+key+'" is too long');}else{if(properties[key]instanceof Date){verifiedProperties[key]=properties[key].toJSON();}else{verifiedProperties[key]=properties[key];}}}}
if(!reset&&droppedProperties.length){WisePopsStorage.dropCustomProperties(droppedProperties);}
WisePopsStorage.addCustomProperties(verifiedProperties,reset);}},goalAction:function(goalName,revenue){if(goalName&&typeof goalName!=='string'){this.log('error','Method "goal" accepts a goal name as optional 2nd parameter');goalName=null;}else if(goalName&&goalName.length>50){this.log('warn','The goal name cannot exceed 50 characters');goalName=goalName.substr(0,50);}
if(revenue&&isNaN(revenue)){this.log('error','Method "goal" accepts a revenue amount as optional 3rd parameter');revenue=null;}
if(revenue&&revenue>1000000){this.log('warn','The revenue cannot exceed 1,000,000');revenue=1000000;}
var logMsg='Tracking goal';if(goalName){logMsg+=' named "'+goalName+'"';}
if(revenue){logMsg+=' with revenue "'+revenue+'"';}
this.log('info',logMsg);var lastPopups=WisePopsStorage.getLastDisplayedAndConvertedPopups();if(lastPopups.displayPopId||lastPopups.convertPopId){var params={e:'g'};if(goalName){params.n=goalName;}
if(revenue){params.r=revenue;}
if(lastPopups.displayPopId){params.pd=lastPopups.displayPopId;params.dd=lastPopups.displayDate.toJSON();}
if(lastPopups.convertPopId){params.pc=lastPopups.convertPopId;params.dc=lastPopups.convertDate.toJSON();}
this._trackCall(params);}},trackDisplay:function(popId,popLabel,callback){WisePopsStorage.setDisplayed(popId);this._trackGA('Display',popLabel);this._trackCall({e:'d',p:popId},callback);},trackClick:function(popId,popLabel,callback){if(WisePopsStorage.setConverted(popId)){this._trackGA('Click',popLabel);this._trackCall({e:'c',p:popId},callback);}},trackSignup:function(popId,popLabel,email,additionalFields,callback){if(this.trackSignupCalled[popId]){callback();return;}
this.trackSignupCalled[popId]=true;if(WisePopsStorage.setConverted(popId)&&WisePopsStorage.setSubscribed(popId)){this._trackGA('Signup',popLabel);var params={e:'c',p:popId,d:email};for(var i=0;i<additionalFields.length;i++){additionalFields[i].name=''+additionalFields[i].name;additionalFields[i].value=''+additionalFields[i].value;additionalFields[i].tag=''+additionalFields[i].tag;params['add-data['+i+'][name]']=additionalFields[i].name;params['add-data['+i+'][value]']=additionalFields[i].value;if(additionalFields[i].tag==''){params['add-data['+i+'][tag]']=additionalFields[i].name.replace(/\s+/,'_').toLowerCase();}else{params['add-data['+i+'][tag]']=additionalFields[i].tag;}}
this._trackCall(params,callback);}},_trackCall:function(params,callback){callback=callback||function(){};var url=WisePopsStorage.baseUrl.tracking+'/_.gif?';for(var key in params){if(params.hasOwnProperty(key)){url+=key+'='+encodeURIComponent(params[key])+'&';}}
url=url.slice(0,-1);if(navigator.sendBeacon&&navigator.sendBeacon(url)){callback();}else{var tag=document.createElement('img');tag.onload=callback;tag.src=url+'&un='+Math.floor(Math.random()*1000);tag.style.display='none';document.body.appendChild(tag);}},_trackGA:function(event,popLabel){if(WisePopsStorage.isEventGATracked(event)){var ga=window[window.GoogleAnalyticsObject||'ga'];if(typeof ga==='function'&&typeof ga.getAll==='function'){ga(function(){var trackingIds=[];ga.getAll().forEach(function(tracker){if(trackingIds.indexOf(tracker.get('trackingId'))===-1){trackingIds.push(tracker.get('trackingId'));ga(tracker.get('name')+'.'+'send','event','WisePops',event,popLabel,{nonInteraction:true});}});});}else if(window._gaq&&typeof window._gaq.push==='function'){window._gaq.push(['_trackEvent','WisePops',event,popLabel,undefined,true]);}}},logAction:function(level){if(!level||this.loggerLevels.indexOf(level)===-1){level='info';}
this.loggerDisplayLevel=this.loggerLevels.indexOf(level);for(var i=0;i<this.logger.length;i++){this._displayLogLine(this.logger[i]);}},log:function(level,message,properties){if(this.loggerLevels.indexOf(level)===-1){level='info';}
var line={level:this.loggerLevels.indexOf(level),msg:message,prop:properties};if(this.logger.length<constants.loggerMaxSize){this.logger.push(line);}
this._displayLogLine(line);},_displayLogLine:function(line){if(this.loggerDisplayLevel!==null){if(line.level<=this.loggerDisplayLevel&&console[this.loggerLevels[line.level]]){var logLine='WisePops - '+line.msg;if(line.prop){logLine={message:logLine,properties:line.prop};}
console[this.loggerLevels[line.level]](logLine);}}},optionsAction:function(options){for(var optionName in options){if(options.hasOwnProperty(optionName)){var optionMethod='_'+optionName+'Option';if(!this[optionMethod]){this.log('error','Unkown option "'+optionName+'"');}else{this[optionMethod](options[optionName]);}}}},_browserStorageOption:function(enable){try{if(WisePopsStorage.setBrowserStorageUsed(!!enable,true)){this.log('info','Browser storage has been '+(enable?'enabled':'disabled'));}}catch(e){this.log('warn',e);}}};WisePopsStorage._init();WisePopsApi._init();})();var wiseStorage={isConverted:function(popId){return this._getObj()._storage.isConverted(popId);},setConverted:function(popId){return this._getObj()._storage.setConverted(popId);},setDisplayed:function(popId){return this._getObj()._storage.setDisplayed(popId);},_getObj:function(){return window[window['WisePopsObject']];}};function WisepopsAddToCookiePage(){}