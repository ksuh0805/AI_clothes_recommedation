-- by 이수현, 안지영
-- 뭐입지니 db (mysql) 테이블 생성문
-- 사용자(user), 상의(top), 하의(bottom) 테이블
CREATE DATABASE wtw_genie default CHARACTER SET UTF8;
use wtw_genie;

-- user 테이블
-- attributes: *u_name, age, sex, height, weight
create table user(
   u_name varchar(20) not null,
   age int not null,
   sex char(10) not null,
   height float not null,
   weight float not null,
   primary key (u_name)
);

-- top 테이블
-- attributes: *item_id, u_name, color, item_shape
create table top(
   item_id varchar(20) not null,
   u_name varchar(20) not null,
   color varchar(20),
   item_shape varchar(40) not null,
   primary key(item_id),
   foreign key(u_name) references user(u_name)
);

-- bottom 테이블
-- attributes: *item_id, u_name, color, item_shape
create table bottom(
   item_id varchar(20) not null,
   u_name varchar(20) not null,
   color varchar(20),
   item_shape varchar(40) not null,
   primary key(item_id),
   foreign key(u_name) references user(u_name)
);

-- sample insertion
INSERT INTO user VALUES ('user000', 40, 'male', 170, 70);
INSERT INTO user VALUES ('user001', 25, 'male', 185, 70);
INSERT INTO user VALUES ('user002', 40, 'female', 165, 60);
INSERT INTO user VALUES ('user003', 25, 'female', 155, 50);

INSERT INTO top VALUES ('user000_topitem000', 'user000', NULL, 'short_shirt');
INSERT INTO top VALUES ('user000_topitem001', 'user000', NULL, 'short_tee');
INSERT INTO bottom VALUES ('user000_botitem000', 'user000', NULL, 'short_shirt');
INSERT INTO top VALUES ('user000_topitem002', 'user000', NULL, 'long_shirt');
INSERT INTO top VALUES ('user000_topitem003', 'user000', NULL, 'short_sports');

INSERT INTO top VALUES ('user001_topitem000', 'user001', NULL, 'short_tee');
INSERT INTO top VALUES ('user001_topitem001', 'user001', NULL, 'short_shirt');
INSERT INTO top VALUES ('user001_topitem002', 'user001', NULL, 'long_shirt');
INSERT INTO top VALUES ('user001_topitem003', 'user001', NULL, 'sweater');
INSERT INTO top VALUES ('user001_topitem004', 'user001', NULL, 'long_tee');
INSERT INTO bottom VALUES ('user001_botitem000', 'user001', NULL, 'long_chino');
INSERT INTO bottom VALUES ('user001_botitem001', 'user001', NULL, 'long_denim');
INSERT INTO bottom VALUES ('user001_botitem002', 'user001', NULL, 'short_chino');
INSERT INTO bottom VALUES ('user001_botitem003', 'user001', NULL, 'long_chino');
INSERT INTO bottom VALUES ('user001_botitem004', 'user001', NULL, 'short_chino');
INSERT INTO bottom VALUES ('user001_botitem005', 'user001', NULL, 'short_chino');

INSERT INTO top VALUES ('user002_topitem000', 'user002', NULL, 'short_tee');
INSERT INTO top VALUES ('user002_topitem001', 'user002', NULL, 'long_shirt');
INSERT INTO top VALUES ('user002_topitem002', 'user002', NULL, 'short_shirt');
INSERT INTO top VALUES ('user002_topitem003', 'user002', NULL, 'long_tee');
INSERT INTO top VALUES ('user002_topitem004', 'user002', NULL, 'short_sports');
INSERT INTO top VALUES ('user002_topitem005', 'user002', NULL, 'long_sports');
INSERT INTO bottom VALUES('user002_botitem001', 'user002', NULL, 'long_chino');
INSERT INTO bottom VALUES('user002_botitem003', 'user002', NULL, 'long_denim');
INSERT INTO bottom VALUES('user002_botitem004', 'user002', NULL, 'short_chino');
INSERT INTO bottom VALUES('user002_botitem005', 'user002', NULL, 'long_chino');
INSERT INTO bottom VALUES('user002_botitem007', 'user002', NULL, 'leggings');
INSERT INTO bottom VALUES('user002_botitem008', 'user002', NULL, 'long_skirt');

INSERT INTO bottom VALUES('user003_botitem000', 'user003', NULL, 'short_chino');
INSERT INTO bottom VALUES('user003_botitem001', 'user003', NULL, 'long_chino');
INSERT INTO bottom VALUES('user003_botitem002', 'user003', NULL, 'long_skirt');
INSERT INTO bottom VALUES('user003_botitem003', 'user003', NULL, 'long_denim');
INSERT INTO bottom VALUES('user003_botitem004', 'user003', NULL, 'short_skirt');
INSERT INTO bottom VALUES('user003_botitem005', 'user003', NULL, 'long_denim');
INSERT INTO top VALUES ('user003_topitem000', 'user003', NULL, 'short_shirt');
INSERT INTO top VALUES ('user003_topitem001', 'user003', NULL, 'long_blouse');
INSERT INTO top VALUES ('user003_topitem002', 'user003', NULL, 'short_tee');
INSERT INTO top VALUES ('user003_topitem003', 'user003', NULL, 'long_tee');
INSERT INTO top VALUES ('user003_topitem004', 'user003', NULL, 'short_tee');
INSERT INTO top VALUES ('user003_topitem005', 'user003', NULL, 'long_shirt');
INSERT INTO top VALUES ('user003_topitem006', 'user003', NULL, 'short_blouse');
INSERT INTO top VALUES ('user003_topitem007', 'user003', NULL, 'short_sports');



