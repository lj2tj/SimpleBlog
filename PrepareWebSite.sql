use myblog;

insert into blog_appsettings (`name`, `value`, `comment`) values('WebSiteName','YourWebSiteName','YourWebSiteDescription');
insert into blog_appsettings (`name`, `value`, `comment`) values('ICP','京ICP证1234567号','备案');

insert into blog_trademode (mode, description) values('WeChat', '微信');
insert into blog_trademode (mode, description) values('ZhiFuBao', '支付宝');
insert into blog_trademode (mode, description) values('Bank', '银行转账');
insert into blog_trademode (mode, description) values('CreditCard', '信用卡');
insert into blog_trademode (mode, description) values('Other', '其它');

insert into blog_jobtitle (job_title) values('初级');
insert into blog_jobtitle (job_title) values('中级');
insert into blog_jobtitle (job_title) values('高级');

insert into blog_jobposition (job_title) values('护士');
insert into blog_jobposition (job_title) values('护士长');
insert into blog_jobposition (job_title) values('护理部主任');

insert into blog_websitelevel (levels, description) values('A', '初出茅庐');
insert into blog_websitelevel (levels, description) values('B', '小有成就');
insert into blog_websitelevel (levels, description) values('C', '远近闻名');
insert into blog_websitelevel (levels, description) values('D', '江湖传说');

