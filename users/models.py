from django.db import models

'''
mysql> desc user;
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | int(11)      | NO   | PRI | NULL    | auto_increment |
| created_date   | datetime     | YES  |     | NULL    |                |
| email          | varchar(50)  | YES  |     | NULL    |                |
| password       | varchar(255) | YES  |     | NULL    |                |
| referral_code  | varchar(50)  | YES  |     | NULL    |                |
| referrer_code  | varchar(50)  | YES  |     | NULL    |                |
| username       | varchar(15)  | NO   | UNI | NULL    |                |
| wallet_balance | varchar(10)  | YES  |     | NULL    |                |
| status         | int(1)       | NO   |     | 0       |                |
| authtoken      | varchar(55)  | NO   |     | NULL    |                |
+----------------+--------------+------+-----+---------+----------------+
10 rows in set (0.00 sec)
'''

class User(models.Model):
    id = models.AutoField(primary_key=True)
    referral_code = models.CharField(max_length=50, null=True)
    referrer_code = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=30, unique= True, null=True)
    password = models.CharField(max_length=100, null=True)
    authtoken = models.CharField(max_length=55, null=False)
    username = models.CharField(max_length=15, null=False) #phone
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    status = models.BooleanField(default=False)
    wallet_balance = models.CharField(max_length = 30, null = False)

    USERNAME_FIELD = 'email'

    class Meta:
        managed = False
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

'''
mysql> desc session;
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| id          | int(11)     | NO   | PRI | NULL    | auto_increment |
| token       | varchar(50) | NO   | UNI | NULL    |                |
| expire_date | datetime    | NO   |     | NULL    |                |
+-------------+-------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)

'''
class Session(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=50, null=False)
    expire_date = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'session'
        verbose_name = 'session'
        verbose_name_plural = 'sessions'
