def ping(update, context):
    user_data = context.user_data
    print(user_data.items() + 'from search')
    return 2