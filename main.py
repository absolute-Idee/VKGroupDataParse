from users_info import get_json, collect_info, get_users, write_csv
from post_info import getjson, get_all_posts, write_2csv, make_posts

group_id = '108291890'
token = ''

def write_users_info_csv(token, group_id):
    users, count_users = get_users(token, group_id, 'sex, bdate, city')
    info = collect_info(users, group_id)
    write_csv(info)

def write_posts_info_csv(token, group_id):
    all_posts, count_posts = get_all_posts (token, group_id)
    pposts = make_posts(all_posts)
    write_2csv(pposts)

if __name__=='__main__':
    #write_users_info_csv(token=token, group_id=group_id)
    write_posts_info_csv(token, group_id)