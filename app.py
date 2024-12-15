from aiohttp import web
from datetime import datetime

app = web.Application()
ads = {}
ad_id_counter = 1


async def create_ad(request):
    global ad_id_counter

    try:
        data = await request.json()
    except Exception as e:
        return web.json_response({'error': 'Invalid JSON'}, status=400)

    if not data.get('title') or not data.get('description') or not data.get('owner'):
        return web.json_response({'error': 'Missing required fields'}, status=400)

    ad = {
        'id': ad_id_counter,
        'title': data['title'],
        'description': data['description'],
        'created_at': datetime.now().isoformat(),
        'owner': data['owner']
    }
    ads[ad_id_counter] = ad
    ad_id_counter += 1

    return web.json_response(ad, status=201)


async def get_ad(request):
    ad_id = int(request.match_info['ad_id'])
    ad = ads.get(ad_id)
    if not ad:
        return web.json_response({'error': 'Ad not found'}, status=404)
    return web.json_response(ad)


async def delete_ad(request):
    ad_id = int(request.match_info['ad_id'])
    ad = ads.pop(ad_id, None)
    if not ad:
        return web.json_response({'error': 'Ad not found'}, status=404)
    return web.json_response({'message': 'Ad deleted successfully'})


async def update_ad(request):
    ad_id = int(request.match_info['ad_id'])
    ad = ads.get(ad_id)
    if not ad:
        return web.json_response({'error': 'Ad not found'}, status=404)

    try:
        data = await request.json()
    except Exception as e:
        return web.json_response({'error': 'Invalid JSON'}, status=400)

    ad['title'] = data.get('title', ad['title'])
    ad['description'] = data.get('description', ad['description'])
    ad['owner'] = data.get('owner', ad['owner'])

    return web.json_response(ad)


app.router.add_post('/ads', create_ad)
app.router.add_get('/ads/{ad_id}', get_ad)
app.router.add_delete('/ads/{ad_id}', delete_ad)
app.router.add_put('/ads/{ad_id}', update_ad)

if __name__ == '__main__':
    web.run_app(app)
