from pyramid.view import view_config, view_defaults
import pyramid.httpexceptions as exc

from bible_drevle_com.models import Book, Chapter, Session, engine


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
        return Book.get_books()


class BookDetailResource(BookResource):

    def __getitem__(self, chapter_id):
        if str(chapter_id).isdigit():
            return ChapterDetailResource()

    def __json__(self, request):
        book_slug = request.matchdict['traverse'][1]
        book = Book.get_book(book_slug)
        if not book:
            raise exc.HTTPNotFound()
        return book


class ChapterDetailResource(BookDetailResource):

    def __json__(self, request):
        book_slug = request.matchdict['traverse'][1]
        chapter_id = request.matchdict['traverse'][2]
        chapter = Chapter.get_chapter_text(book_slug, chapter_id)

        if not chapter:
            raise exc.HTTPNotFound()
        return chapter


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
