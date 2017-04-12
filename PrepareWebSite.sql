use myblog;

insert into blog_appsettings (`name`, `value`, `comment`) values('WebSiteName','YourWebSiteName','YourWebSiteDescription');
insert into blog_appsettings (`name`, `value`, `comment`) values('ICP','京ICP证1234567号','备案');
insert into blog_trademode (mode, description) values('WeChat', '微信');
insert into blog_trademode (mode, description) values('ZhiFuBao', '支付宝');
insert into blog_trademode (mode, description) values('Bank', '银行转账');
insert into blog_trademode (mode, description) values('CreditCard', '信用卡');
insert into blog_trademode (mode, description) values('Other', '其它');
