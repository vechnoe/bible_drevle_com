from pyramid.config import Configurator
from pyramid.renderers import JSON
from .views import RESTViewBible, rest_factory


def setup_includes(config):
    config.include('bible_drevle_com.bible')


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    settings = {
        'sqlalchemy.url': 'postgresql+psycopg2://bible:123456@localhost/bible'
    }
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_jinja2')
    config.include('pyramid_tm')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_renderer('jsonify', JSON(indent=4, ensure_ascii=False))
    config.add_route('home', '/')

    config.add_route('rest_api', '/api/v1/*traverse', factory=rest_factory)

    config.scan()
    return config.make_wsgi_app()
