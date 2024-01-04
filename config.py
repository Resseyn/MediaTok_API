postgres_query = "dbname=padro user=postgres password=7595"
api_secret_key = "e75b4c583b1d0da31d36305be816484b46890f27df690f7badc03b6832c3"


class Example:
    def __init__(self):
        print("initialized")
    def __call__(self, *args, **kwargs):
        print("Called", args, kwargs)

prikol = Example() # initialized
prikol(123)  # Called 123