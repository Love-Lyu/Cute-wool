 /*
豆伴 安卓版本

安卓抓包 域名  api.imdouban.com

请求头里面的 douban-token 值
请求头里面的 device-id 值

用 & 组合两个值 用 @ 分割多账户
token=123&device=123
例如 
export dbcookie='token=123&device=123@token=456&device=456'

*/
 let name = "0"
 //  修改资料和用户名开关 
 //  一开始运行一次后保持关闭
 //  1 打开 
 const $ = new Env("豆伴-安卓版");
 let envSplitor = ['@']
 let httpResult, httpReq, httpResp
 let userCookie = ($.isNode() ? process.env.dbcookie : $.getdata('dbcookie')) || '';
 let userList = []
 let userIdx = 0
 let userCount = 0
 let idp="android"

 ///////////////////////////////////////////////////////////////////
 class UserInfo
 {
 	constructor(str)
 	{
 		this.index = ++userIdx
 		this.name = this.index
 		this.valid = false
 		this.withdrawFailCount = 0
 		try
 		{
 			this.ck = $.str2json(str)
 			this.ckValid = true
 		}
 		catch (e)
 		{
 			this.ckValid = false
 			$.logAndNotify(`账号[${this.index}]CK无效，请检查格式`)
 		}
 	}
 	async kong()
 	{
 		try
 		{
 			let url = `https://api.imdouban.com/v1/users`
 			this.namex = getRandomName()
 			let body = `education=%E7%A0%94%E7%A9%B6%E7%94%9F&figure=%E9%AB%98%E5%A4%A7%E5%A8%81%E7%8C%9B&height=182cm&occupation=%E5%85%AC%E5%8A%A1%E7%8C%BF&signature=%E4%BD%A0%E5%A5%BD%20&smoking_status=%E5%B7%B2%E5%A9%9A&update_scenario=2&weight=65kg&nickname=${this.namex}&reside=%E6%B9%9B%E6%B1%9F%E5%B8%82`
 			let token = `${this.ck.token}`
 			let device= `${this.ck.device}`
 			let urlObject = populateUrlObject(url, token, body)
 			await httpRequest('post', urlObject)
 			let result = httpResult;
 			nickxname = result.data.nickname
 			await this.label(nickxname)
 			console.log(`账号[${this.name}] ` + nickxname + ` 资料设置为 ` + result.data.reside)
 		}
 		catch (e)
 		{
 			console.log(e)
 		}
 		finally
 		{
 			return Promise.resolve(1);
 		}
 	}
 	async label(nickxname)
 	{
 		try
 		{
 			let url = `https://api.imdouban.com/v1/user-labels`
 			let body = `label_ids=174%7C13%7C16%7C19%7C14%7C17%7C15%7C12%7C18`
 			let token = `${this.ck.token}`
 			let device= `${this.ck.device}`
 			let urlObject = populateUrlObject(url, token,device, body)
 			await httpRequest('post', urlObject)
 			let result = httpResult;
 		}
 		catch (e)
 		{
 			console.log(e)
 		}
 		finally
 		{
 			return Promise.resolve(1);
 		}
 	}
 	async usersi()
 	{
 		try
 		{
 			let url = `https://api.imdouban.com/v1/users/0?uid=0`
 			let body = ``
 			let token = `${this.ck.token}`
 			let device= `${this.ck.device}`
 			let urlObject = populateUrlObject(url, token,device, body)
 			await httpRequest('get', urlObject)
 			let result = httpResult;
 			let nickname = result.data.nickname
 			await this.view(nickname)
 		}
 		catch (e)
 		{
 			console.log(e)
 		}
 		finally
 		{
 			return Promise.resolve(1);
 		}
 	}
 	async receive(nickname)
 	{
 		try
 		{
 			let url = `https://api.imdouban.com/v1/dd-money/receive`
 			let body = ``
 			let token = `${this.ck.token}`
 			let device= `${this.ck.device}`
 			let urlObject = populateUrlObject(url, token,device, body)
 			await httpRequest('post', urlObject)
 			let result = httpResult;
 			this.message = result.message
 			this.code = result.code
 			if(this.code == 200)
 			{
 				console.log(`\n账号[${this.name}] ` + nickname + ` 提现 :` + this.message)
 			}
 			else if(this.code == 400) console.log(`\n账号[${this.name}] ` + nickname + ` 提现 : ` + this.message)
 		}
 		catch (e)
 		{
 			console.log(e)
 		}
 		finally
 		{
 			return Promise.resolve(1);
 		}
 	}
 	async view(nickname)
 	{
 		try
 		{
 			let url = `https://api.imdouban.com/v1/dd-money/view`
 			let body = ``
 			let token = `${this.ck.token}`
 			let device= `${this.ck.device}`
 			let urlObject = populateUrlObject(url, token,device, body)
 			await httpRequest('get', urlObject)
 			let result = httpResult;
 			this.day = result.data.today
 			this.zfb = result.data.zfb_account
 			this.money = result.data.money
 			if(result.data.status == 0)
 			{
 				console.log(`账号[${this.name}] ` + nickname + ` \n绑定支付宝:` + this.zfb + ` 可提金额:` + this.money + `\n`)
 				await this.receive()
 			}
 			else if(result.data.status == 1)
 			{
 				console.log(`账号[${this.name}] ` + nickname + ` \n绑定支付宝:` + this.zfb + ` 已提金额:` + this.money + `\n`)
 			}
 		}
 		catch (e)
 		{
 			console.log(e)
 		}
 		finally
 		{
 			return Promise.resolve(1);
 		}
 	}
 }!(async () =>
 {
 	if(typeof $request !== "undefined")
 	{
 		await GetRewrite()
 	}
 	else
 	{
 		if(!(await checkEnv())) return;
 		let taskall = []
 		let validList = userList.filter(x => x.ckValid)
 		if(validList.length > 0)
 		{
 			if(name == 1)
 			{
 				console.log('\n-------------- 资料 --------------')
 				taskall = []
 				for(let user of validList)
 				{
 					taskall.push(user.kong())
 				}
 				await Promise.all(taskall)
 			}
 			console.log('\n-------------- 豆伴 --------------')
 			taskall = []
 			for(let user of validList)
 			{
 				taskall.push(user.usersi())
 			}
 			await Promise.all(taskall)
 		}
 		await $.showmsg();
 	}
 })()
 .catch((e) => console.log(e))
 	.finally(() => $.done())
 ///////////////////////////////////////////////////////////////////
 async function GetRewrite()
 {
 	if($request.url.indexOf(`api.imdouban.com/v1/users`) > -1)
 	{
 		if(!$request.headers) return;
 		let token = $request.headers['douban-token']
 		if(!token) return false
 		let ck = `${token}`
 		console.log(ck)
 		if(userCookie)
 		{
 			if(userCookie.indexOf(ck) == -1)
 			{
 				userCookie = userCookie + '@' + ck
 				$.setdata(userCookie, 'dbcookie');
 				ckList = userCookie.split('@')
 				$.msg(`获取第${ckList.length}个ck成功: ${ck}`)
 			}
 		}
 		else
 		{
 			$.setdata(ck, 'dbcookie');
 			$.msg(`获取第1个ck成功: ${ck}`)
 		}
 	}
 }

 function getRandomName()
 {
 	let lastDict = ["李", "王", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗", "梁", "宋", "郑", "谢", "韩", "唐", "冯", "于", "董", "萧", "程", "曹", "袁", "邓", "许", "傅", "沈", "曾", "彭", "吕", "苏", "卢", "蒋", "蔡", "贾", "丁", "魏", "薛", "叶", "阎", "余", "潘", "杜", "戴", "夏", "钟", "汪", "田", "任", "姜", "范", "方", "石", "姚", "谭", "廖", "邹", "熊", "金", "陆", "郝", "孔", "白", "崔", "康", "毛", "邱", "秦", "江", "史", "顾", "侯", "邵", "孟", "龙", "万", "段", "漕", "钱", "汤", "尹", "黎", "易", "常", "武", "乔", "贺", "赖", "龚", "文", "庞", "樊", "兰", "殷", "施", "陶", "洪", "翟", "安", "颜", "倪", "严", "牛", "温", "芦", "季", "俞", "章", "鲁", "葛", "伍", "韦", "申", "尤", "毕", "聂", "丛", "焦", "向", "柳", "邢", "路", "岳", "齐", "沿", "梅", "莫", "庄", "辛", "管", "祝", "左", "涂", "谷", "祁", "时", "舒", "耿", "牟", "卜", "路", "詹", "关", "苗", "凌", "费", "纪", "靳", "盛", "童", "欧", "甄", "项", "曲", "成", "游", "阳", "裴", "席", "卫", "查", "屈", "鲍", "位", "覃", "霍", "翁", "隋", "植", "甘", "景", "薄", "单", "包", "司", "柏", "宁", "柯", "阮", "桂", "闵", "欧阳", "解", "强", "柴", "华", "车", "冉", "房", "边"];
 	let firstName = "鑫正涵琛妍芸露楠薇锦彤采初美冬婧桐莲彩洁呈菡怡冰雯雪茜优静萱林馨鹤梅娜璐曼彬芳颖韵曦蔚桂月梦琪蕾依碧枫欣杉丽祥雅欢婷舒心紫芙慧梓香玥菲璟茹昭岚玲云华阳弦莉明珊雨蓓旭钰柔敏家凡花媛歆沛姿妮珍琬彦倩玉柏橘昕桃栀克帆俊惠漫芝寒诗春淑凌珠灵可格璇函晨嘉鸿瑶帛琳文洲娅霞颜康卓星礼远帝裕腾震骏加强运杞良梁逸禧辰佳子栋博年振荣国钊喆睿泽允邦骞哲皓晖福濡佑然升树祯贤成槐锐芃驰凯韦信宇鹏盛晓翰海休浩诚辞轩奇潍烁勇铭平瑞仕谛翱伟安延锋寅起谷稷胤涛弘侠峰材爵楷尧炳乘蔓桀恒桓日坤龙锟天郁吉暄澄中斌杰祜权畅德";
 	let lRandom = randomNum(0, lastDict.length - 1);
 	let fRandom_0 = randomNum(0, firstName.length - 1);
 	let fRandom_1 = randomNum(0, firstName.length - 1);
 	return lastDict[lRandom] + firstName.charAt(fRandom_0) + (Math.random() > 0.3 ? firstName.charAt(fRandom_1) : '');
 }

 function randomNum(minNum, maxNum)
 {
 	switch (arguments.length)
 	{
 		case 1:
 			return parseInt(Math.random() * minNum + 1, 10);
 			break;
 		case 2:
 			return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
 			break;
 		default:
 			return 0;
 			break;
 	}
 }
 async function checkEnv()
 {
 	if(userCookie)
 	{
 		let splitor = envSplitor[0];
 		for(let sp of envSplitor)
 		{
 			if(userCookie.indexOf(sp) > -1)
 			{
 				splitor = sp;
 				break;
 			}
 		}
 		for(let userCookies of userCookie.split(splitor))
 		{
 			if(userCookies) userList.push(new UserInfo(userCookies))
 		}
 		userCount = userList.length
 	}
 	else
 	{
 		console.log('未找到CK')
 		return;
 	}
 	console.log(`共找到${userCount}个账号`)
 	return true
 }
 ////////////////////////////////////////////////////////////////////
 function populateUrlObject(url, token,device, body = '')
 {
 	let host = url.replace('//', '/')
 		.split('/')[1]
 	let urlObject = {
 		url: url,
 		headers:
 		{
 			'Host': host,
 			'device-id': device,
 			'douban-token': token,
 			'douban-channel': "release",
 			'device-type': idp,
 		},
 		timeout: 5000,
 	}
 	//console.log(`${JSON.stringify(urlObject)}`)
 	if(body)
 	{
 		urlObject.body = body
 	}
 	return urlObject;
 }
 async function httpRequest(method, url)
 {
 	httpResult = null, httpReq = null, httpResp = null;
 	return new Promise((resolve) =>
 	{
 		$.send(method, url, async (err, req, resp) =>
 		{
 			try
 			{
 				httpReq = req;
 				httpResp = resp;
 				if(err)
 				{
 					console.log(`${method}请求失败`);
 					console.log(JSON.stringify(err));
 				}
 				else
 				{
 					if(resp.body)
 					{
 						if(typeof resp.body == "object")
 						{
 							httpResult = resp.body;
 						}
 						else
 						{
 							try
 							{
 								httpResult = JSON.parse(resp.body);
 							}
 							catch (e)
 							{
 								httpResult = resp.body;
 							}
 						}
 					}
 				}
 			}
 			catch (e)
 			{
 				console.log(e);
 			}
 			finally
 			{
 				resolve();
 			}
 		});
 	});
 }
 ////////////////////////////////////////////////////////////////////
 function Env(name, env)
 {
 	"undefined" != typeof process && JSON.stringify(process.env)
 		.indexOf("GITHUB") > -1 && process.exit(0);
 	return new class
 	{
 		constructor(name, env)
 		{
 			this.name = name;
 			this.notifyStr = '';
 			this.startTime = (new Date)
 				.getTime();
 			Object.assign(this, env);
 			console.log(`${this.name} 开始运行：\n`);
 		}
 		isNode()
 		{
 			return "undefined" != typeof module && !!module.exports
 		}
 		isQuanX()
 		{
 			return "undefined" != typeof $task
 		}
 		isSurge()
 		{
 			return "undefined" != typeof $httpClient && "undefined" == typeof $loon
 		}
 		isLoon()
 		{
 			return "undefined" != typeof $loon
 		}
 		getdata(t)
 		{
 			let e = this.getval(t);
 			if(/^@/.test(t))
 			{
 				const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t),
 					r = s ? this.getval(s) : "";
 				if(r)
 					try
 					{
 						const t = JSON.parse(r);
 						e = t ? this.lodash_get(t, i, "") : e
 					}
 				catch (t)
 				{
 					e = ""
 				}
 			}
 			return e
 		}
 		setdata(t, e)
 		{
 			let s = !1;
 			if(/^@/.test(e))
 			{
 				const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e),
 					o = this.getval(i),
 					h = i ? "null" === o ? null : o || "{}" : "{}";
 				try
 				{
 					const e = JSON.parse(h);
 					this.lodash_set(e, r, t),
 						s = this.setval(JSON.stringify(e), i)
 				}
 				catch (e)
 				{
 					const o = {};
 					this.lodash_set(o, r, t),
 						s = this.setval(JSON.stringify(o), i)
 				}
 			}
 			else
 			{
 				s = this.setval(t, e);
 			}
 			return s
 		}
 		getval(t)
 		{
 			return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null
 		}
 		setval(t, e)
 		{
 			return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null
 		}
 		send(m, t, e = (() =>
 		{}))
 		{
 			if(m != 'get' && m != 'post' && m != 'put' && m != 'delete')
 			{
 				console.log(`无效的http方法：${m}`);
 				return;
 			}
 			if(m == 'get' && t.headers)
 			{
 				delete t.headers["Content-Type"];
 				delete t.headers["Content-Length"];
 			}
 			else if(t.body && t.headers)
 			{
 				if(!t.headers["Content-Type"]) t.headers["Content-Type"] = "application/x-www-form-urlencoded";
 			}
 			if(this.isSurge() || this.isLoon())
 			{
 				if(this.isSurge() && this.isNeedRewrite)
 				{
 					t.headers = t.headers ||
 					{};
 					Object.assign(t.headers,
 					{
 						"X-Surge-Skip-Scripting": !1
 					});
 				}
 				let conf = {
 					method: m,
 					url: t.url,
 					headers: t.headers,
 					timeout: t.timeout,
 					data: t.body
 				};
 				if(m == 'get') delete conf.data
 				$axios(conf)
 					.then(t =>
 					{
 						const
 						{
 							status: i,
 							request: q,
 							headers: r,
 							data: o
 						} = t;
 						e(null, q,
 						{
 							statusCode: i,
 							headers: r,
 							body: o
 						});
 					})
 					.catch(err => console.log(err))
 			}
 			else if(this.isQuanX())
 			{
 				t.method = m.toUpperCase(), this.isNeedRewrite && (t.opts = t.opts ||
 					{}, Object.assign(t.opts,
 					{
 						hints: !1
 					})),
 					$task.fetch(t)
 					.then(t =>
 					{
 						const
 						{
 							statusCode: i,
 							request: q,
 							headers: r,
 							body: o
 						} = t;
 						e(null, q,
 						{
 							statusCode: i,
 							headers: r,
 							body: o
 						})
 					}, t => e(t))
 			}
 			else if(this.isNode())
 			{
 				this.got = this.got ? this.got : require("got");
 				const
 				{
 					url: s,
 					...i
 				} = t;
 				this.instance = this.got.extend(
 				{
 					followRedirect: false
 				});
 				this.instance[m](s, i)
 					.then(t =>
 					{
 						const
 						{
 							statusCode: i,
 							request: q,
 							headers: r,
 							body: o
 						} = t;
 						e(null, q,
 						{
 							statusCode: i,
 							headers: r,
 							body: o
 						})
 					}, t =>
 					{
 						const
 						{
 							message: s,
 							response: i
 						} = t;
 						e(s, i, i && i.body)
 					})
 			}
 		}
 		time(t)
 		{
 			let e = {
 				"M+": (new Date)
 					.getMonth() + 1,
 				"d+": (new Date)
 					.getDate(),
 				"h+": (new Date)
 					.getHours(),
 				"m+": (new Date)
 					.getMinutes(),
 				"s+": (new Date)
 					.getSeconds(),
 				"q+": Math.floor(((new Date)
 					.getMonth() + 3) / 3),
 				S: (new Date)
 					.getMilliseconds()
 			};
 			/(y+)/.test(t) && (t = t.replace(RegExp.$1, ((new Date)
 					.getFullYear() + "")
 				.substr(4 - RegExp.$1.length)));
 			for(let s in e)
 				new RegExp("(" + s + ")")
 				.test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? e[s] : ("00" + e[s])
 					.substr(("" + e[s])
 						.length)));
 			return t
 		}
 		async showmsg()
 		{
 			if(!this.notifyStr) return;
 			let notifyBody = this.name + " 运行通知\n\n" + this.notifyStr
 			if($.isNode())
 			{
 				var notify = require('./sendNotify');
 				console.log('\n============== 推送 ==============')
 				await notify.sendNotify(this.name, notifyBody);
 			}
 			else
 			{
 				this.msg(notifyBody);
 			}
 		}
 		logAndNotify(str)
 		{
 			console.log(str)
 			this.notifyStr += str
 			this.notifyStr += '\n'
 		}
 		msg(e = t, s = "", i = "", r)
 		{
 			const o = t =>
 			{
 				if(!t)
 					return t;
 				if("string" == typeof t)
 					return this.isLoon() ? t : this.isQuanX() ?
 						{
 							"open-url": t
 						} :
 						this.isSurge() ?
 						{
 							url: t
 						} :
 						void 0;
 				if("object" == typeof t)
 				{
 					if(this.isLoon())
 					{
 						let e = t.openUrl || t.url || t["open-url"],
 							s = t.mediaUrl || t["media-url"];
 						return {
 							openUrl: e,
 							mediaUrl: s
 						}
 					}
 					if(this.isQuanX())
 					{
 						let e = t["open-url"] || t.url || t.openUrl,
 							s = t["media-url"] || t.mediaUrl;
 						return {
 							"open-url": e,
 							"media-url": s
 						}
 					}
 					if(this.isSurge())
 					{
 						let e = t.url || t.openUrl || t["open-url"];
 						return {
 							url: e
 						}
 					}
 				}
 			};
 			this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r)));
 			let h = ["", "============== 系统通知 =============="];
 			h.push(e),
 				s && h.push(s),
 				i && h.push(i),
 				console.log(h.join("\n"))
 		}
 		getMin(a, b)
 		{
 			return ((a < b) ? a : b)
 		}
 		getMax(a, b)
 		{
 			return ((a < b) ? b : a)
 		}
 		padStr(num, length, padding = '0')
 		{
 			let numStr = String(num)
 			let numPad = (length > numStr.length) ? (length - numStr.length) : 0
 			let retStr = ''
 			for(let i = 0; i < numPad; i++)
 			{
 				retStr += padding
 			}
 			retStr += numStr
 			return retStr;
 		}
 		json2str(obj, c, encodeUrl = false)
 		{
 			let ret = []
 			for(let keys of Object.keys(obj)
 				.sort())
 			{
 				let v = obj[keys]
 				if(v && encodeUrl) v = encodeURIComponent(v)
 				ret.push(keys + '=' + v)
 			}
 			return ret.join(c);
 		}
 		str2json(str, decodeUrl = false)
 		{
 			let ret = {}
 			for(let item of str.split('&'))
 			{
 				if(!item) continue;
 				let idx = item.indexOf('=')
 				if(idx == -1) continue;
 				let k = item.substr(0, idx)
 				let v = item.substr(idx + 1)
 				if(decodeUrl) v = decodeURIComponent(v)
 				ret[k] = v
 			}
 			return ret;
 		}
 		randomString(len, charset = 'abcdef0123456789')
 		{
 			let str = '';
 			for(let i = 0; i < len; i++)
 			{
 				str += charset.charAt(Math.floor(Math.random() * charset.length));
 			}
 			return str;
 		}
 		randomList(a)
 		{
 			let idx = Math.floor(Math.random() * a.length)
 			return a[idx]
 		}
 		wait(t)
 		{
 			return new Promise(e => setTimeout(e, t))
 		}
 		done(t = {})
 		{
 			const e = (new Date)
 				.getTime(),
 				s = (e - this.startTime) / 1e3;
 			console.log(`\n${this.name} 运行结束，共运行了 ${s} 秒！`)
 			if(this.isSurge() || this.isQuanX() || this.isLoon()) $done(t)
 		}
 	}(name, env)
 }
