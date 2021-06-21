from neomodel import config

from Technipedia.App.Controlers.User.Crud import *
from Technipedia.App.Controlers.User.Other import *
from Technipedia.App.Models.UserModel import User

config.DATABASE_URL = "bolt://neo4j:root@127.0.0.1/7687"  # "bolt://neo4j:dlrs@ensp2018@172.20.10.6/7687"

# user = User.nodes.get_or_none(email='adrientchounkeu10@gmail.com')
# user.locates.disconnect_all()

id = 'e9a77528eed847c9968d9ee35106775e'
# 'e09a74d4bf7d400b89a494a8ffd3eb6b'#'2197ba1badc049948faefa119cfc9676'#'269a66f0de2641d0bee11533090115de'#'5d8683ad9edd4483852e44a69276221b'#'a43cdf615421419e8888d02b7e48e7ba'
"""user = searchUserById(id)
print(user.economicstatus)
print(user.profil_search)
recs = cold_start_second(id, state='new')
for rec in recs:
    print("-----------")
    print(rec[0].economicstatus)
    print(rec[0].profil_search)

print("@@@@@@@@@@@@@")
recs = cold_start_second(id, state='old')
for rec in recs:
    print("-----------")
    print(rec[0].economicstatus)
    print(rec[0].profil_search)"""

id_opp = 'f792d5fbc00c47c59ce1791351c39504'  # 'e7477d785b474565a0c4aea10f9060f1'

user = searchUserById(id)
print(user.economicstatus)
print(user.profil_search)
recs_users_opp = recommendUsersToUserForOpportinuity(id, id_opp)
for rec in recs_users_opp:
    print("-----------")
    print(rec[0].economicstatus)
    print(rec[0].profil_search)
