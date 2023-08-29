___________________ Test05ReviewAPI.test_01_review_not_auth ___________________

self = <tests.test_05_review.Test05ReviewAPI object at 0x000001CA30C42610>
client = <django.test.client.Client object at 0x000001CA30A98B90>
admin_client = <rest_framework.test.APIClient object at 0x000001CA30A9B810>
admin = <User: TestAdmin>
user_client = <rest_framework.test.APIClient object at 0x000001CA30A9B590>
user = <User: TestUser>
moderator_client = <rest_framework.test.APIClient object at 0x000001CA30A98C50>
moderator = <User: TestModerator>

    def test_01_review_not_auth(self, client, admin_client, admin, user_client,
                                user, moderator_client, moderator):
        author_map = {
            admin: admin_client,
            user: user_client,
            moderator: moderator_client
        }
>       reviews, titles = create_reviews(admin_client, author_map)

tests\test_05_review.py:20:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests\utils.py:248: in create_reviews
    titles, _, _ = create_titles(admin_client)
tests\utils.py:217: in create_titles
    genres = create_genre(admin_client)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

admin_client = <rest_framework.test.APIClient object at 0x000001CA30A9B810>

    def create_genre(admin_client):
        result = []
        data = {'name': '▒▒▒▒▒', 'slug': 'horror'}
        result.append(data)
        response = admin_client.post('/api/v1/genres/', data=data)
>       assert response.status_code == HTTPStatus.CREATED, (
            '▒▒▒▒ POST-▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ▒ `/api/v1/genres/` ▒▒▒▒▒▒▒▒ '
            '▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒ - ▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒ ▒▒ ▒▒▒▒▒▒▒▒ 201.'
        )
E       AssertionError: ▒▒▒▒ POST-▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒ ▒ `/api/v1/genres/` ▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒▒ - ▒▒▒▒▒▒ ▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒ ▒▒ ▒▒▒▒▒▒▒▒ 201.
