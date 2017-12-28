from auth import read_token

TOKEN = read_token()


headers = {
    'User-Agent':'Happn/19.1.0 AndroidSDK/19',
    'platform': 'android',
    'Host':'api.happn.fr',
    'connection' : 'Keep-Alive',
    'Accept-Encoding':'gzip',
    'Content-Type'  : 'application/json'
    'Authorization': 'OAth="{}"'.format(TOKEN)
}




def recommendations(limit=16, offset=0):
    query = '{"types":"468","limit":'+str(limit)+',"offset":'+str(offset)+',"fields":"id,modification_date,notification_type,nb_times,notifier.fields(id,job,is_accepted,workplace,my_relation,distance,gender,my_conversation,is_charmed,nb_photos,first_name,age,profiles.mode(1).width(360).height(640).fields(width,height,mode,url))"}'

    
