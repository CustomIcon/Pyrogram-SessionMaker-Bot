from pyrogram import filters


def dynamic_data_filter(data):
    async def func(flt, _, query):
        return flt.data == query.data

    return filters.create(func, data=data)
