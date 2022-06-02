import json

import asyncpg
from aiohttp import web
from gino import Gino

app = web.Application()
db = Gino()


class AdsModel(db.Model):
    __tablename__ = 'Ads'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    create_date = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


async def orm_context(app):
    print('Запуск приложения')
    await db.set_bind('postgres://aiohttp:1234@127.0.0.1:5434/aiohttp')
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('Выкл')


class AdsView(web.View):

    async def get(self):
        ads_id = int(self.request.match_info['ads_id'])
        ads = await AdsModel.get(ads_id)
        if not ads:
            raise web.HTTPBadRequest(text=json.dumps({'error': f'user id: {ads_id} does not exist'}), content_type='application/json')
        else:
            return web.json_response({
                'id': ads.id,
                'title': ads.title,
                'description':ads.description,
                'create_date':ads.create_date,
                'user_id':ads.user_id
            })

    async def post(self):
        ads_data = await self.request.json()
        try:
            ads_data = await AdsModel.create(**ads_data)
        except asyncpg.exceptions.UniqueViolationError:
            raise web.HTTPBadRequest(text=json.dumps({'error': 'ads already exists'}), content_type='application/json')
        return web.json_response({
            'id': ads_data.id
        })

    async def put(self):
        new_ads = await self.request.json()
        print(new_ads)
        ads_id = int(self.request.match_info['ads_id'])
        ads = await AdsModel.get(ads_id)
        if not ads:
            raise web.HTTPBadRequest(text=json.dumps({'error': f'user id: {ads_id} does not exist'}),
                                     content_type='application/json')
        else:
            await ads.update(title=new_ads['title'],
            description=new_ads['description'],
            create_date=new_ads['create_date'],
            user_id=new_ads['user_id']).apply()
            return web.json_response({
            'id': ads.id,'title': ads.title,
            'description': ads.description,
            'create_date': ads.create_date,
            'user_id': ads.user_id })

    async def delete(self):
        ads_id = int(self.request.match_info['ads_id'])
        ads = await AdsModel.get(ads_id)
        if not ads:
            raise web.HTTPBadRequest(text=json.dumps({'error': f'user id: {ads_id} does not exist'}),
                                     content_type='application/json')
        else:
                await ads.delete()
                return web.json_response({
                    'status': 'OK'
                })

# async def test_view(request):
#     json_data = await request.json()
#     headers = dict(request.headers)
#     uri_variables = dict(request.match_info)
#     qs = dict(request.query)
#     return web.json_response({
#         'json': json_data,
#         'headers': headers,
#         'uri_variables': uri_variables,
#         'qs': qs})
#

app.router.add_routes(
    [
        web.get('/ads/{ads_id:\d+}/', AdsView),
        web.put('/ads/{ads_id:\d+}/', AdsView),
        web.delete('/ads/{ads_id:\d+}/', AdsView),
        web.post('/ads/', AdsView)
    ]
)
app.cleanup_ctx.append(orm_context)
web.run_app(app)
