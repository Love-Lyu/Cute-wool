
const jsname = '快手极速版'
const $ = Env(jsname);
const notify = $.isNode() ? require('./sendNotify') : '';      // 这里是 node（青龙属于node环境）通知相关的
const { default: Request } = require('got/dist/source/core');
const { request } = require('http');
const querystring = require('querystring');
const { get } = require('request');
const internal = require('stream');
const Notify = 1; //0为关闭通知，1为打开通知,默认为1
const debug = 0; //0为关闭调试，1为打开调试,默认为0
let ksgscookie = ''             // 这里是 从青龙的 配置文件 读取你写的变量
let kscookieArr = [];
let cookie = '';
let msg = '';
let index = 0;
let nameArr = [];
let nickname = ''
let lid = '0';
let withdraw = false;
let withdrawtime = '';
let sp_161 = true;
let sp_11 = true;
let sp_161_80 = true;
let sp_11_80 = true;
let sp_259 = true;
let fenge = 506;
let enc = ''
let sig, sig3, tokensig, salt, didi, apist, ud, apihost, token = ''
let ssid = ""
let signum = 0
let jbdh, tx = 'false'
!(async () => {
    if ($.isNode) {
        ksgscookie = $.isNode() ? process.env.ksjsbcookie : ''
        $.jbdh = $.isNode() ? (process.env.jbdh ? process.env.ksjsbjbdh : 'false') : 'false'
    }
    else {
        ksgscookie = $.getdata('ksjsbcookie')
        $.jbdh = $.getdata('jbdh')
    }
    if (debug) {
        console.log(ksgscookie)
    }
    if (!(await Envs()))  	//多账号分割 判断变量是否为空  初步处理多账号
        return;
    else {
        console.log(`\n\n=========================================    \n脚本执行 - 北京时间(UTC+8)：${new Date(
            new Date().getTime() + new Date().getTimezoneOffset() * 60 * 1000 +
            8 * 60 * 60 * 1000).toLocaleString()} \n=========================================\n`);
        console.log(`\n设定自动兑换金币:${$.jbdh}\n\n`)
        console.log(`\n=================== 共找到 ${kscookieArr.length} 个账号 ===================`)
        console.log(`\n========= 获取账号信息 =========\n`)
        let now = new Date().getHours().toString()
        if (now == $.withdrawtime && $.tx == true) {
            withdraw = true
        }
        for (let i = 0; i < kscookieArr.length; i++) {
            $.index = i + 1
            let ck = kscookieArr[i].replace(/;/g, '&')
            let cktemp = querystring.parse(ck)
            if (cktemp.did && cktemp['kuaishou.api_st']) {
                $.didi = cktemp.did
                $.apist = cktemp['kuaishou.api_st']
                $.cookie = `kpn=NEBULA; kpf=ANDROID_PHONE;c=XIAOMI; ver=10.3; appver=10.3.31.3276; client_key=2ac2a76d; language=zh-cn; countryCode=CN; sys=ANDROID_9; mod=Xiaomi%28MI+6%29; net=WIFI; deviceName=Xiaomi%28MI+6%29; isp=; did_tag=7;kcv=1458; app=0; bottom_navigation=true; android_os=0; boardPlatform=msm8998; androidApiLevel=28; newOc=XIAOMI; slh=0; country_code=cn; nbh=0; hotfix_ver=; did_gt=1652302313321; keyconfig_state=2; max_memory=256; oc=XIAOMI; sh=1920; app_status=3; ddpi=480; deviceBit=0; browseType=3; power_mode=0; socName=Qualcomm+MSM8998; sw=1080; ftt=; apptype=22; abi=arm64; cl=0; userRecoBit=0; device_abi=arm64; totalMemory=5724; grant_browse_type=AUTHORIZED; iuid=; rdid=${$.didi}; sbh=72; darkMode=false; kuaishou.api_st=${$.apist}; kuaishou.h5_st=${$.apist}; is_background=0; did=${$.didi}; oDid=TEST_${$.didi};`     // 这里是分割你每个账号的每个小项   
                await getUserInfo();
                //await $.wait(1 * 1000);
            } else {
                console.log(`第 [ ${$.index} ]个账号cookie错误，请确认。`)
                return
            }
        }
        //console.log(ckk)
        //return
        await SendMsg(msg); // 与发送通知有关系
    }

})().catch((e) => { $.log('', `❌ ${$.name}, 失败! 原因: ${e}!`, '') }).finally(() => { $.done(); })


function getUserInfo(timeout = 3 * 1000) {
    return new Promise((resolve) => {
        let url = {
            url: `https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/basicInfo`,
            headers: {
                'Accept-Encoding': `gzip, deflate`,
                'Cookie': $.cookie,
                'Connection': `keep-alive`,
                'Accept': `*/*`,
                'Host': `nebula.kuaishou.com`,
                'Accept-Language': `en-us`,
                "User-Agent": `Kwai-android aegon/3.4.0`,
            }

        }
        $.get(url, async (err, resp, data) => {
            try {
                data = JSON.parse(data)
                //console.log(data)
                if (data.result == 1) {
                    $.nickname = data.data.userData.nickname
                    console.log(`账号  ${$.index}  [${data.data.userData.nickname}]账户余额${data.data.totalCash}元，${data.data.totalCoin}金币`)
                    if ($.jbdh == 'true' && parseInt(data.data.totalCoin) > 100) {
                        console.log(`账号  ${$.index}  [${$.nickname}]切换为手动兑换金币`)
                        await coinchange(2)
                        console.log(`账号  ${$.index}  [${$.nickname}]手动兑换[${data.data.totalCoin}]金币`)
                        await coin2cash(data.data.totalCoin)
                        console.log(`账号  ${$.index}  [${$.nickname}]切换为自动兑换金币`)
                        await coinchange(0)
                    }
                    $.nickname = data.data.userData.nickname
                    msg += (`账号  ${$.index}  [${data.data.userData.nickname}]账户余额${data.data.totalCash}元，${data.data.totalCoin}金币\n`)
                    if (parseInt(data.data.totalCash) + parseInt(data.data.totalCoin / 10000) >= 3) {
                        if (parseInt(data.data.totalCash) + parseInt(data.data.totalCoin / 10000) >= 50) {
                            console.log(`账号  ${$.index}  [${data.data.userData.nickname}]尝试提现50元`)
                            msg += (`账号  ${$.index}  [${data.data.userData.nickname}]尝试提现50元到微信\n`)
                            await u_withdraw(50, 'ALIPAY')

                        } else if (parseInt(data.data.totalCash) + parseInt(data.data.totalCoin / 10000) >= 20) {
                            console.log(`账号  ${$.index}  [${data.data.userData.nickname}]尝试提现30元`)
                            msg += (`账号  ${$.index}  [${data.data.userData.nickname}]尝试提现30元到微信\n`)
                            await u_withdraw(20, 'ALIPAY')
                        } else if (parseInt(data.data.totalCash) + parseInt(data.data.totalCoin / 10000) >= 10) {
                            console.log(`账号  ${$.index}  [${data.data.userData.nickname}]尝试提现10元`)
                            msg += (`账号  ${$.index}  [${data.data.userData.nickname}]尝试提现10元到微信\n`)
                            await u_withdraw(10, 'ALIPAY')
                        } else if (parseInt(data.data.totalCash) + parseInt(data.data.totalCoin / 10000) >= 3) {
                            console.log(`账号  ${$.index}  [${data.data.userData.nickname}]尝试提现3元`)
                            msg += (`账号  ${$.index}  [${data.data.userData.nickname}]尝试提现3元到微信\n`)
                            await u_withdraw(3, 'ALIPAY')
                        }
                    }


                } else {
                    console.log(`第【${$.index}】个账号获取信息失败，${data.error_msg}`)
                }
            } catch (e) {
                $.logErr(e, resp);
            } finally {
                resolve()
            }
        }, timeout)
    })
}


async function u_withdraw(cash, type = 'ALIPAY', timeout = 3 * 1000) {
    return new Promise((resolve) => {
        let url = {
            url: `https://nebula.kuaishou.com/rest/n/nebula/outside/withdraw/apply`,
            headers: {
                'Origin': `https://nebula.kuaishou.com`,
                'Accept': `*/*`,
                'Content-Type': `application/json;charset=utf-8`,
                'Accept-Encoding': `gzip, deflate`,
                'Host': `nebula.kuaishou.com`,
                'User-Agent': `Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1`,
                'Accept-Language': `en-us`,
                'Connection': `keep-alive`,
                'Cookie': $.cookie,
            },
            body: JSON.stringify({
                "channel": type,
                "amount": cash
            })
        }
        $.post(url, async (err, resp, data) => {
            try {
                data = JSON.parse(data)
                //console.log(data)
                if (data.result == 1) {
                    console.log(`账号  ${$.index}  [${$.nickname}]提现${cash}到${type}成功`)
                    msg += (`账号  ${$.index}  [${$.nickname}]提现${cash}到${type}成功\n`)
                } else {
                    if (type == 'ALIPAY') {
                        console.log(`账号  ${$.index}  [${$.nickname}]提现到${type}失败，${data.error_msg}，尝试提现到支付宝`)
                        msg += (`账号  ${$.index}  [${$.nickname}]提现到${type}失败，${data.error_msg}，尝试提现到支付宝\n`)
                        await u_withdraw(cash, 'WECHAT')
                    } else {
                        console.log(`账号  ${$.index}  [${$.nickname}]提现到${type}失败,${data.error_msg}`)
                        msg += (`账号  ${$.index}  [${$.nickname}]提现到${type}失败,${data.error_msg}\n`)
                    }

                }
            } catch (e) {
                $.logErr(e, resp);
            } finally {
                resolve()
            }
        }, timeout)
    })
}
async function coinchange(type, timeout = 3 * 1000) {
    return new Promise((resolve) => {
        let url = {
            url: `https://nebula.kuaishou.com/rest/n/nebula/exchange/changeExchangeType`,
            headers: {
                'Accept-Encoding': `gzip, deflate`,
                'Cookie': $.cookie,
                'Connection': `keep-alive`,
                'Accept': `*/*`,
                //'Host': `nebula.kuaishou.com`,
                'Accept-Language': `en-us`,
                "User-Agent": `Kwai-android aegon/3.4.0`,
                'Content-Type': 'application/json'
            },
            body: `{"type":${type}}`
        }
        $.post(url, async (err, resp, data) => {
            try {
                data = JSON.parse(data)
                //console.log(data)
                if (data.result == 1) {
                    //await share2()
                } else {
                }
            } catch (e) {
                $.logErr(e, resp);
            } finally {
                resolve()
            }
        }, timeout)
    })
}

async function coin2cash(coin, timeout = 3 * 1000) {
    return new Promise((resolve) => {
        let url = {
            url: `https://nebula.kuaishou.com/rest/n/nebula/exchange/coinToCash/submit`,
            headers: {
                'Accept-Encoding': `gzip, deflate`,
                'Cookie': $.cookie,
                'Connection': `keep-alive`,
                'Accept': `*/*`,
                //'Host': `nebula.kuaishou.com`,
                'Accept-Language': `en-us`,
                "User-Agent": `Kwai-android aegon/3.4.0`,
                'Content-Type': 'application/json'
            },
            body: `{"token":"rE2zK-Cmc82uOzxMJW7LI2-wTGcKMqqAHE0PhfN0U4bJY4cAM5Inxw","coinAmount":${coin}}`
        }
        //console.log(url.body)
        $.post(url, async (err, resp, data) => {
            try {
                data = JSON.parse(data)
                //console.log(data)
                if (data.result == 1) {
                    //await share2()
                } else {
                }
            } catch (e) {
                $.logErr(e, resp);
            } finally {
                resolve()
            }
        }, timeout)
    })
}



async function getip( timeout = 3 * 1000) {
    return new Promise((resolve) => {
        let url = {
            url: `http://pv.sohu.com/cityjson?ie=utf-8`,
            headers: {
                'Accept-Encoding': `gzip, deflate`,
                'Cookie': $.cookie,
                'Connection': `keep-alive`,
                'Accept': `*/*`,
                //'Host': `nebula.kuaishou.com`,
                'Accept-Language': `en-us`,
                "User-Agent": `Kwai-android aegon/3.4.0`,
                'Content-Type': 'application/json'
            }
        }
        //console.log(url.body)
        $.get(url, async (err, resp, data) => {
            try {
                //console.log(data)
                data = JSON.parse(data.replace('var returnCitySN = ','').replace(';',''))
                $.ip = data.cip
                console.log('你的IP： '+data.cip)
            } catch (e) {
                $.logErr(e, resp);
            } finally {
                resolve()
            }
        }, timeout)
    })
}
//#region 固定代码 可以不管他
// ============================================变量检查============================================ \\
async function Envs() {
    if (ksgscookie) {
        if (ksgscookie.indexOf("@") != -1) {
            ksgscookie.split("@").forEach((item) => {
                if (item) {
                    kscookieArr.push(`${item}`);
                }
            });
        } else if (ksgscookie.indexOf('\n') != -1) {
            ksgscookie.split('\n').forEach((item) => {
                if (item) {
                    kscookieArr.push(`${item}`);
                }
            });
        } else {
            if (ksgscookie) {
                kscookieArr.push(`${ksgscookie}`);
            }
        }
    } else {
        console.log(`\n 【${$.name}】：未填写变量 ksgscookie`)
        return;
    }
    return true;
}

// ============================================发送消息============================================ \\
async function SendMsg(message) {
    if (!message)
        return;

    if (Notify > 0) {
        if ($.isNode()) {
            var notify = require('./sendNotify');
            await notify.sendNotify($.name, message);
        } else {
            $.msg(message);
        }
    } else {
        console.log(message);
    }
}


// prettier-ignore   固定代码  不用管他
function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }