
def register_views(bp):

    @bp.route('/')
    def index():
        return 'Hello, World!'