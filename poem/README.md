

# 数据库建立

```
CREATE DATABASE spider
use spider
```

# 数据库初始化表

```
# 1.1 poem表 
CREATE TABLE `poem` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `dynasty_id` bigint(20) DEFAULT NULL,
  `dynasty` varchar(255) DEFAULT NULL,
  `poet_name` varchar(255) DEFAULT NULL COMMENT '诗人',
  `poet_url` varchar(255) DEFAULT NULL COMMENT '诗人url',
  `poem_name` varchar(255) DEFAULT NULL COMMENT '作品名称',
  `poem_url` varchar(255) DEFAULT NULL COMMENT '作品url',
  `contents` text COMMENT '诗歌内容',
  `poet_desc` text COMMENT '诗人简介',
  `crawl_url` varchar(500) NOT NULL DEFAULT '' COMMENT '抓取URL',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '抓取入库时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '抓取更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_poet_name` (`poet_name`),
  KEY `idx_dynasty` (`dynasty`),
  KEY `idx_poem_name` (`poem_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='诗词';

# 1.2  dynastys 朝代表

CREATE TABLE `dynastys` (
  `id` int(2) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `dynasty_id` bigint(20) DEFAULT NULL COMMENT '朝代id',
  `dynasty` varchar(255) DEFAULT NULL COMMENT '朝代',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '抓取入库时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '抓取更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_dynasty` (`dynasty`),
  UNIQUE KEY `idx_dynasty_id` (`dynasty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COMMENT='朝代列表';


# 1.3 更新dynastys表
insert into dynastys(dynasty,dynasty_id)values
("先秦",72057594037927936),
("汉代",144115188075855872),
("三国两晋",216172782113783808),
("南北朝",288230376151711744),
("隋代",360287970189639680),
("唐代",432345564227567616),
("宋代",504403158265495552),
("元代",576460752303423488),
("明代",648518346341351424),
("清代",720575940379279360),
("近现代",792633534417207296);

#1.4 更新dynasty_id
update poem as m
join dynastys as q on m.dynasty=q.dynasty
set m.dynasty_id=q.dynasty_id
```

# 运行爬虫

```
修改config/db_global.json下 password以后运行爬虫

scrapy crawl poems
```

# 运行后端

```
进入poem目录，运行

python run.py
进入操作界面，按提示进行操作即可

*初次使用需要进行一次df_all的初始化和储存
```


# 运行网页
```
$env: FLASK_APP = "app"
flask run
```
