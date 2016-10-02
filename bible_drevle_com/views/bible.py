from pyramid.view import view_config, view_defaults
import pyramid.httpexceptions as exc

from bible_drevle_com.models import (
    Session, engine, Book, Chapter, Kathisma, Psalm, Pericope
)


DBSession = Session(bind=engine)


@view_config(route_name='home', renderer='../templates/index.jinja2')
def home(request):
    books = DBSession.query(Book).order_by(Book.book_id).all()
    return {'books': books}


class BookResource(object):

    def __getitem__(self, book_slug):
        if book_slug:
            return BookDetailResource()

    def __json__(self, request):
        return Book.get_bible_books()


class BookDetailResource(BookResource):

    def __getitem__(self, arg):
        if str(arg).isdigit():
            return ChapterDetailResource()
        if str(arg) == 'kathismas':
            return KathismaResource()
        if str(arg) == 'pericopes':
            return PericopeResource()

    def __json__(self, request):
        book_slug = request.matchdict['traverse'][1]
        book = Book.get_detail(book_slug)
        if not book:
            raise exc.HTTPNotFound()
        return book


class ChapterDetailResource(BookDetailResource):

    def __json__(self, request):
        book_slug = request.matchdict['traverse'][1]
        chapter_id = request.matchdict['traverse'][2]
        item = Chapter.get_detail(book_slug, chapter_id)

        if not item:
            raise exc.HTTPNotFound()
        return item


class KathismaResource(BookDetailResource):

    def __getitem__(self, kathisma_id):
        if str(kathisma_id).isdigit():
            return KathismaDetailResource()

    def __json__(self, request):
        kathismas = Kathisma.get_kathismas()

        if not kathismas:
            raise exc.HTTPNotFound()
        return kathismas


class KathismaDetailResource(KathismaResource):

    def __getitem__(self, psalm_id):
        if str(psalm_id).isdigit():
            return PsalmDetailResource()

    def __json__(self, request):
        kathisma_id = request.matchdict['traverse'][3]
        kathisma = Kathisma.get_detail(kathisma_id)

        if not kathisma:
            raise exc.HTTPNotFound()
        return kathisma


class PsalmDetailResource(KathismaResource):

    def __json__(self, request):
        psalm_id = request.matchdict['traverse'][4]
        psalm = Psalm.get_detail(psalm_id)

        if not psalm:
            raise exc.HTTPNotFound()
        return psalm


class PericopeResource(BookDetailResource):

    def __getitem__(self, pericope_id):
        if str(pericope_id).isdigit():
            return PericopeDetailResource()

    def __json__(self, request):

        book_slug = request.matchdict['traverse'][1]

        if book_slug not in ['matthew', 'mark', 'luke', 'john', 'apostle']:
            raise exc.HTTPNotFound()

        pericopes = Pericope.get_list(book_slug)

        if not pericopes:
            raise exc.HTTPNotFound()
        return pericopes


class PericopeDetailResource(KathismaResource):

    def __json__(self, request):
        book_slug = request.matchdict['traverse'][1]
        pericope_id = request.matchdict['traverse'][3]

        pericope = Pericope.get_detail(book_slug, pericope_id)
        if not pericope:
            raise exc.HTTPNotFound()
        return pericope


@view_defaults(
    route_name='rest_api',
    renderer='jsonify',
    context=BookResource
)
class RESTViewBible(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        return self.context


def rest_factory(request):
    return {
        'books': BookResource(),
    }
