/*   
@jszack  

江湖小说 无限刷

定时一小时一次 

安卓IOS都有 ios没有提现入口 安卓应用商店 下载 绑定支付宝 忘记抓提现 没写提现  登录后随便往书架添加几本书 不然不会上传阅读时间

抓包freeapp-api.zhangdu.com 域名 任意链接里面得 数据 

以 userid#token#device_token 直接填入 JHXSCookie 变量里面
 
CK示例 

6331xxx#dedbf3adce9160563a67xxx#C837350D-21FD-4430-B4D4-xxxx
*/
const $ = new Env('江湖小说');
    let envSplitor = ['@', '\n'], ckName = 'JHXSCookie' 
    let httpResult, httpReq, httpResp , lw=60 , userList = [], userIdx = 0, userCount = 0 , _1=[...Array(lw)].map((a,_)=>_+1)
    let userCookie = ($.isNode() ? process.env[ckName] : $.getdata(ckName)) || '';
    ///////////////////////////////////////////////////////////////////
    class UserInfo {
        constructor(str) {
            this.index = ++userIdx
            this.c1 = str.split('#')[0], this.c2 = str.split('#')[1]
            this.idx = `账号 [${this.index}]`
            this.dev=str.split('#')[2]
        }
                async reward() {
                let url = `https://freeapp-api.zhangdu.com/api/user/add-read-length?user_id=${this.c1}&token=${this.c2}&client_type=1&version_name=1.6.0.1&channel_id=14&system_version=10.0&device_token=${this.dev}`
                let body = `book_id=${this.id}&chapter_id=5567688&is_local=0&length=60`
                this.h = {
      "Host": "freeapp-api.zhangdu.com",
      "accept-encoding": "gzip",
      "user-agent": "okhttp/4.9.3"
    }
                let urlObject = popu(url, this.h, body)
                await httpRequest('post', urlObject)
                let result = httpResult;
                if (result.errno==0)console.log(`${this.idx}阅读奖励 上传并领取成功 [等待60秒上传下次时间]`)
        }
     async space() {
                let url = `https://freeapp-api.zhangdu.com/api/user-space/space?to_user_id=${this.c1}&user_id=${this.c1}&token=${this.c2}&client_type=1&version_name=1.6.0.1&channel_id=14&system_version=10.0&device_token=${this.dev}`
                let body = ``
                this.h = {
      "Host": "freeapp-api.zhangdu.com",
      "accept-encoding": "gzip",
      "user-agent": "okhttp/4.9.3"
    }
                let urlObject = popu(url, this.h, body)
                await httpRequest('get', urlObject)
                let result = httpResult;
                for (let a of result.data.bookshelf){
                    this.id=a.book_id
                    await this.reward()
                }
        }
     async sigg() {
                let url = `https://freeapp-api.zhangdu.com/api/welfare/info?user_id=${this.c1}&token=${this.c2}&client_type=1&version_name=1.6.0.1&channel_id=14&system_version=10.0&device_token=${this.dev}`
                let body = ``
                this.h = {
      "Host": "freeapp-api.zhangdu.com",
      "accept-encoding": "gzip",
      "user-agent": "okhttp/4.9.3"
    }
                let urlObject = popu(url, this.h, body)
                await httpRequest('get', urlObject)
                let result = httpResult;
                if (result.errno==0)console.log(`${this.idx}签到成功 `)
        }
                     async welfare() {
                let url = `https://freeapp-api.zhangdu.com/api/welfare/do-task?user_id=${this.c1}&token=${this.c2}&client_type=1&version_name=1.6.0.1&channel_id=14&system_version=10.0&device_token=${this.dev}`
                this.max=$.randomString(1, '4567')
                let body = `task=android_alert`
                this.h = {
      "Host": "freeapp-api.zhangdu.com",
      "accept-encoding": "gzip",
      "user-agent": "okhttp/4.9.3"
    }
                let urlObject = popu(url, this.h, body)
                await httpRequest('post', urlObject)
                let result = httpResult;
                if (result.errno==0)console.log(`${this.idx}视频奖励 ${result.data.coin} `)
                }
                     async info() {
                let url = `https://freeapp-api.zhangdu.com/api/user/info?user_id=${this.c1}&token=${this.c2}&client_type=1&version_name=1.6.0.1&channel_id=14&system_version=10.0&device_token=${this.dev}`
                let body = ``
                this.h = {
      "Host": "freeapp-api.zhangdu.com",
      "accept-encoding": "gzip",
      "user-agent": "okhttp/4.9.3"
    }
                let urlObject = popu(url, this.h, body)
                await httpRequest('get', urlObject)
                let result = httpResult;
                console.log(`${this.idx}用户名 [${result.data.nickname}] 金币余额 [${result.data.coin}] 阅读时间 [${result.data.today_read_length/60}] 分钟`)
                }
                     async task() {
                    await this.info()
                    await this.sigg()
                    for (let a of _1) await this.welfare()
                    for (let a of _1)await this.space(), await $.wait(60000)
                    await this.info()
                    }
} !(async () => {
            if (!(await checkEnv())) return;
            if(userList.length>0){for(let l of(taskll=[],
            userList))taskll.push(l.task());await Promise.all(taskll)}
    })()
        .catch((e) => console.log(e))
        .finally(() => $.done())
async function checkEnv(){if(!userCookie)return console.log(`变量 [${ckName}] 未找到账号`),!1;{let e=envSplitor[0];for(let t of envSplitor)if(userCookie.indexOf(t)>-1){e=t;break}for(let n of userCookie.split(e))n&&userList.push(new UserInfo(n));userCount=userList.length}return console.log(`找到${userCount}个账号`),!0}function popu(e,t,n=""){e.replace("//","/").split("/")[1];let l={url:e,headers:t,timeout:32e3};return n&&(l.body=n),l}async function httpRequest(e,t){return httpResult=null,httpReq=null,httpResp=null,new Promise(n=>{$.send(e,t,async(e,t,l)=>{try{if(httpReq=t,httpResp=l,e);else if(l.body){if("object"==typeof l.body)httpResult=l.body;else try{httpResult=JSON.parse(l.body)}catch(o){httpResult=l.body}}}catch(r){console.log(r)}finally{n()}})})}
    function Env(a, b) {
        return "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0), new class {
            constructor(a, b) {
                this.name = a, this.notifyStr = "", this.startTime = (new Date).getTime(), Object.assign(this, b), console.log(`${this.name} 开始运行：
    `)
            } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } getdata(b) { let a = this.getval(b); if (/^@/.test(b)) { let [, c, f] = /^@(.*?)\.(.*?)$/.exec(b), d = c ? this.getval(c) : ""; if (d) try { let e = JSON.parse(d); a = e ? this.lodash_get(e, f, "") : a } catch (g) { a = "" } } return a } setdata(c, d) { let a = !1; if (/^@/.test(d)) { let [, b, e] = /^@(.*?)\.(.*?)$/.exec(d), f = this.getval(b), i = b ? "null" === f ? null : f || "{}" : "{}"; try { let g = JSON.parse(i); this.lodash_set(g, e, c), a = this.setval(JSON.stringify(g), b) } catch (j) { let h = {}; this.lodash_set(h, e, c), a = this.setval(JSON.stringify(h), b) } } else a = this.setval(c, d); return a } getval(a) { return this.isSurge() || this.isLoon() ? $persistentStore.read(a) : this.isQuanX() ? $prefs.valueForKey(a) : this.isNode() ? (this.data = this.loaddata(), this.data[a]) : this.data && this.data[a] || null } setval(b, a) { return this.isSurge() || this.isLoon() ? $persistentStore.write(b, a) : this.isQuanX() ? $prefs.setValueForKey(b, a) : this.isNode() ? (this.data = this.loaddata(), this.data[a] = b, this.writedata(), !0) : this.data && this.data[a] || null } send(b, a, f = () => { }) { if ("get" != b && "post" != b && "put" != b && "delete" != b) { console.log(`无效的http方法：${b}`); return } if ("get" == b && a.headers ? (delete a.headers["Content-Type"], delete a.headers["Content-Length"]) : a.body && a.headers && (a.headers["Content-Type"] || (a.headers["Content-Type"] = "application/x-www-form-urlencoded")), this.isSurge() || this.isLoon()) { this.isSurge() && this.isNeedRewrite && (a.headers = a.headers || {}, Object.assign(a.headers, { "X-Surge-Skip-Scripting": !1 })); let c = { method: b, url: a.url, headers: a.headers, timeout: a.timeout, data: a.body }; "get" == b && delete c.data, $axios(c).then(a => { let { status: b, request: c, headers: d, data: e } = a; f(null, c, { statusCode: b, headers: d, body: e }) }).catch(a => console.log(a)) } else if (this.isQuanX()) a.method = b.toUpperCase(), this.isNeedRewrite && (a.opts = a.opts || {}, Object.assign(a.opts, { hints: !1 })), $task.fetch(a).then(a => { let { statusCode: b, request: c, headers: d, body: e } = a; f(null, c, { statusCode: b, headers: d, body: e }) }, a => f(a)); else if (this.isNode()) { this.got = this.got ? this.got : require("got"); let { url: d, ...e } = a; this.instance = this.got.extend({ followRedirect: !1 }), this.instance[b](d, e).then(a => { let { statusCode: b, request: c, headers: d, body: e } = a; f(null, c, { statusCode: b, headers: d, body: e }) }, b => { let { message: c, response: a } = b; f(c, a, a && a.body) }) } } time(a) { let b = { "M+": (new Date).getMonth() + 1, "d+": (new Date).getDate(), "h+": (new Date).getHours(), "m+": (new Date).getMinutes(), "s+": (new Date).getSeconds(), "q+": Math.floor(((new Date).getMonth() + 3) / 3), S: (new Date).getMilliseconds() }; for (let c in /(y+)/.test(a) && (a = a.replace(RegExp.$1, ((new Date).getFullYear() + "").substr(4 - RegExp.$1.length))), b) new RegExp("(" + c + ")").test(a) && (a = a.replace(RegExp.$1, 1 == RegExp.$1.length ? b[c] : ("00" + b[c]).substr(("" + b[c]).length))); return a } async showmsg() { if (!this.notifyStr) return; let a = this.name + " \u8FD0\u884C\u901A\u77E5\n\n" + this.notifyStr; if ($.isNode()) { var b = require("./sendNotify"); console.log("\n============== \u63A8\u9001 =============="), await b.sendNotify(this.name, a) } else this.msg(a) } logAndNotify(a) { console.log(a), this.notifyStr += a, this.notifyStr += "\n" } msg(d = t, a = "", b = "", e) { let f = a => { if (!a) return a; if ("string" == typeof a) return this.isLoon() ? a : this.isQuanX() ? { "open-url": a } : this.isSurge() ? { url: a } : void 0; if ("object" == typeof a) { if (this.isLoon()) { let b = a.openUrl || a.url || a["open-url"], c = a.mediaUrl || a["media-url"]; return { openUrl: b, mediaUrl: c } } if (this.isQuanX()) { let d = a["open-url"] || a.url || a.openUrl, e = a["media-url"] || a.mediaUrl; return { "open-url": d, "media-url": e } } if (this.isSurge()) return { url: a.url || a.openUrl || a["open-url"] } } }; this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(d, a, b, f(e)) : this.isQuanX() && $notify(d, a, b, f(e))); let c = ["", "============== \u7CFB\u7EDF\u901A\u77E5 =============="]; c.push(d), a && c.push(a), b && c.push(b), console.log(c.join("\n")) } getMin(a, b) { return a < b ? a : b } getMax(a, b) { return a < b ? b : a } padStr(e, b, f = "0") { let a = String(e), g = b > a.length ? b - a.length : 0, c = ""; for (let d = 0; d < g; d++)c += f; return c + a } json2str(b, e, f = !1) { let c = []; for (let d of Object.keys(b).sort()) { let a = b[d]; a && f && (a = encodeURIComponent(a)), c.push(d + "=" + a) } return c.join(e) } str2json(e, f = !1) { let d = {}; for (let a of e.split("#")) { if (!a) continue; let b = a.indexOf("="); if (-1 == b) continue; let g = a.substr(0, b), c = a.substr(b + 1); f && (c = decodeURIComponent(c)), d[g] = c } return d } randomString(d, a = "abcdef0123456789") { let b = ""; for (let c = 0; c < d; c++)b += a.charAt(Math.floor(Math.random() * a.length)); return b } randomList(a) { let b = Math.floor(Math.random() * a.length); return a[b] } wait(a) { return new Promise(b => setTimeout(b, a)) } done(a = {}) {
                let b = (new Date).getTime(), c = (b - this.startTime) / 1e3; console.log(`
    ${this.name} 运行结束，共运行了 ${c} 秒！`), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(a)
            }
        }(a, b)
    }