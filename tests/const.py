from datetime import timedelta

from app.utils.clock import today

DATE_FROM = str(today() + timedelta(days=30))
DATE_TO = str(today() + timedelta(days=34))

PASSWORD = "password123"
PASSWORD_HASH = "$argon2id$v=19$m=65536,t=3,p=4$5EA2LBGgz4ZnUJav8JcmeA$RyOCu4XpSCph+/TGxhsw54t1/d3fTvjVtHrorbSRDmU"
