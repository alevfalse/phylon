async def evaluateCode(ctx, qzxcode):
    try:
        eval(qzxcode)
        await ctx.send('Looking good!')
    except Exception as e:
        await ctx.send(e)