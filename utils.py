from datetime import datetime

async def check_online_status(app, user_id):
        try:
            user = await app.get_users(user_id)

            print(user)

            if str(user.status) == "UserStatus.ONLINE":
                print(f"User {user_id} is currently online")
                return 1
            elif str(user.status) == "UserStatus.OFFLINE":
                now = datetime.now()
                parsed_date = user.last_online_date

                diff = now - parsed_date
                minutes = diff.total_seconds() / 60

                if minutes < 2:
                    print(f"User {user_id} was less than minute ago")
                    return 2
                else:
                    print(f"User {user_id} is offline. Last seen: {user.last_online_date}")
                    return 0

        except Exception as e:
            print(f"Error checking user status: {e}")
            return 0