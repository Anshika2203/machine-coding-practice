import uuid

class Post:
    def __init__(self, user_id, content):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.content = content
        self.timestamp = uuid.uuid1().time

class SocialMedia:
    def __init__(self):
        self.users = {}  # Stores users and their followers
        self.posts = {}  # Stores posts by post_id
        self.user_posts = {}  # Stores posts by user_id

    def create_post(self, user_id, content):
        if user_id not in self.users:
            self.users[user_id] = set()  # Initialize user if not exists
        post = Post(user_id, content)
        self.posts[post.id] = post
        self.user_posts.setdefault(user_id, []).append(post)
        return post.id

    def delete_post(self, post_id):
        if post_id in self.posts:
            post = self.posts[post_id]
            self.user_posts[post.user_id].remove(post)
            del self.posts[post_id]
        else:
            raise ValueError("Post ID not found.")

    def follow_user(self, user_id, follow_id):
        if user_id not in self.users:
            self.users[user_id] = set()
        if follow_id not in self.users:
            self.users[follow_id] = set()
        self.users[user_id].add(follow_id)

    def unfollow_user(self, user_id, unfollow_id):
        if user_id in self.users and unfollow_id in self.users[user_id]:
            self.users[user_id].remove(unfollow_id)

    def get_feed(self, user_id, limit=None):
        if user_id not in self.users:
            return []
        feed = []
        for followee in self.users[user_id]:
            feed.extend(self.user_posts.get(followee, []))
        feed.sort(key=lambda x: x.timestamp, reverse=True)  # Sort by latest
        return [post.content for post in (feed[:limit] if limit else feed)]

# Example Usage
if __name__ == "__main__":
    sm = SocialMedia()
    sm.follow_user("user1", "user2")
    post_id = sm.create_post("user2", "Hello World!")
    print(sm.get_feed("user1"))  # Should return "Hello World!"