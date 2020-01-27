# Computer-ticket
# 电脑小票
### 来一份数字“电脑小票”吧

# 摘要：
> 本 API (以下简称“接口”)可用于生成一份不可篡改的文本签名，签名结果可用于校验源文本是否被篡改。基于这一思路，可将这个流程看作是一次交易行为交易凭证(以下简称[电脑小票])。

## 详细说明：  
> 该接口可方便地对一份文本T进行签名并得到和发布签名hash(T)，通过hash(T)可再通过接口获取T。

## 这样形式实现的[电脑小票]的优点是：
> 1.不可篡改性。签名结果 hash(T) 会发布到 PRESSone 公链上，不可篡改，而T并不会上链。现在的数字支付记录，平台方完全可以通过更改数据库而篡改交易记录，甚至删除交易记录。  
2.储存环保健康经济。T 的储存不依赖纸质媒介，数字化储存所消耗的磁盘空间和时间可以灵活计费。而热敏纸小票的保存时间受其物理性质限制，并且热敏纸本身是致癌物质。  
3.海量内容。T 的数据量没有限制。这样可以在[电脑小票]中添加各种内容，如，此次交易适用的法律法规条例，以及享有的售后服务细则，报税税号。  
4.高拓展性。为团体购物集体付款的凭证实现创造可能。可以拥有代购方、付款方、提货方的内容于其中，甚至拥有交接现场的视频的链接。  

# API
## GET /api/v1/creat_id/


## POST /api/v1/pub/
  > pintoken : String, genarate by /api/v1/creat_id/  
  > userid : String, genarate by /api/v1/creat_id/  
  > private_key : String, genarate by /api/v1/creat_id/  
  > sessionid : String, genarate by /api/v1/creat_id/  
  > pin : String, befor changed by user is '000000'  
  > data : String

```// cURL Example
curl -i -H "Content-Type: application/json"  
-X POST --data '{'userid':'a935fb65-3ac0-3a2b-b5ff-79b8848c3659', 'data':'theContent',   
'pintoken':'iBg10iO7itdSHK7dW2nv1w+oE+XS9dj9EtLtUo7EPDzK/7fUJCA3OCPLMRjoVF9Z+YBNJe8X1bHOkV3Asv24x1gCJSIBE0flm6heQfOcupsNk4arOdvbVhmf5hRkqItUWmsBwR67b4wH5gkwaoxmFgPd7lvd7jdyW9jIn6rUBx4=',  
'private_key':'''-----BEGIN RSA PRIVATE KEY-----\r\nMIICWwIBAAKBgQCW6rohnxwLm1MS+ouvZx4W2f5j4GnjvsYlgXlr+cHSso238Q9A\r\n/2MkyNW/U0iYnRK47urxQyAd6EEgkT3v2cHOKqQMjCKR3RLTlzsqBLWLMyWJEXnc\r\nhJMMig2DO3pFVa9ezII/jUd8m/33PLs2w2uunlFDP/KIL0xptWwoIDvv1QIDAQAB\r\nAoGAC84fsjqWgIftZyonHBjmXyY9QoXO8qw9JrjqjRoz4a3q7Q0TwuNXV4zIP5ed\r\nsaZzzPiPc0DrdbtxwMDrxePUR5QDT2QSk/jdEw8mIN4Z1fPQe1Tw83eifgKOzcgP\r\nOdo4pOw8tSjrKx6CRuWhejjcPt2QbnvwF6M6u0vI9EklUdECQQC9MSJBXkD0jz5E\r\nu8rEixbp9z0KAhtNNOytgW66eM8MQsrK5qLiPN1DFPxctaITpWxv/ItutQnvPumT\r\n8wQ0d2+9AkEAzDWMRG0sqD5Gb60WlNkhO9nfMjlwPWMV/xzUUTdMUVbZOW4zJVHh\r\nTgEN2wjPHtwrXpRvSnuCunqV88TKbfjV+QJAGCpVeMoEO/ir+HWQMcieVaYp2sRo\r\nHlV7QbI9pX3W3HcPlhkdhw5FKNNeZK0ilaXUkv1MBgkDytZbWXV5/QWgdQJAYamu\r\nZr9L3z7BUwGVziQ117jwHMYJnuI3j+XKyPjIYBJIG0ZP4aZSOYsZhEqnO9wSRc55\r\nl0aQk/yyoH3aTlP2iQJALZhoLRDINOVyijl46izDC46uaIwxHDxs522DH/fBobje\r\nbvuw7LSwj9YZjvcMXtQxmalJdlPOUL1CjLdFmNQ5Fw==\r\n-----END RSA PRIVATE KEY-----\r\n''',  
'pin':'000000',  
'sessionid': '224e5a92-d313-467a-ab34-49d13b5ccbd3'}'
```
