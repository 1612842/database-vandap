create database demo2;
use demo2;

create table if not exists users(
    user_id int auto_increment primary key,
    username varchar(20),
    display_name nvarchar(50),
    password varchar(20), 
    avatar int,
	status boolean
    /* false(Offline), true(Online)*/
);


create table if not exists groups(
    group_id int auto_increment primary key,
    avatar int,
    groupname nvarchar(50),
    member_number tinyint
);


create table if not exists messages(
    message_id int auto_increment primary key, 
    sender int not null, 
    /* sender := user(user_id)*/
    receiver int not null,
    /* receiver := user(user_id) IF receiver_type IS 'U' ELSE group(group_id)*/
    receiver_type CHAR(1),
    /*  receiver_type:= 'U' IF sendto(user) ELSE 'G' -> sendto(group) */ 
    message_time datetime,
    message_content nvarchar(255)
);


create table if not exists notifications(
    notification_id int auto_increment primary key,
    time datetime,
    sender int not null,
    sender_type  char(1),
    receiver int not null,
    receiver_type char(1),
    content nvarchar(50),
    status char(1)
    /*N - waiting for accepting, Y - already accepted*/
);

create table if not exists contacts(
    id   int primary key,
    user int not null,
    type    CHAR(1), /* (U)User, (G)Group*/
    detail int not null
    /*detail := user(user_id) IF type IS 'U' ELSE group(group_id) */
);


create table if not exists group_with_user(
    group_id int not null,  
    /* Ref group(group_id)*/
    user_id int not null,
    /* Ref user(user_id)*/
    primary key(group_id,user_id)
);


ALTER TABLE notifications
    ADD FOREIGN KEY (sender) REFERENCES users(user_id);
ALTER TABLE notifications
    ADD FOREIGN KEY (receiver) REFERENCES users(user_id);

ALTER TABLE messages
    ADD FOREIGN KEY (sender) REFERENCES users(user_id);


ALTER TABLE group_with_user
    ADD FOREIGN KEY (group_id) REFERENCES groups(group_id);
ALTER TABLE group_with_user
    ADD FOREIGN KEY (user_id) REFERENCES users(user_id);


ALTER TABLE contacts
    ADD FOREIGN KEY (user) REFERENCES users(user_id);


CREATE PROCEDURE `getMsg`(idsend int, idreceive int)
BEGIN
select * 
from users join messages on users.user_id = messages.sender
where (sender=idsend and receiver =idreceive) or (sender=idreceive and receiver =idsend)
order by message_id asc;
END


