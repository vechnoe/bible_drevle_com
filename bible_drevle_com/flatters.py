__all__ = [
    'chapter_flatter',
    'book_flatter',
    'kathismas_flatter',
    'psalm_flatter'
]


def chapter_flatter(item):
    return dict(
        title=item.title,
        titleSlavonic=item.title_slavonic,
        chapterId=item.chapter_id,
        text=item.text,
    )


def book_flatter(book):
    return dict(
        bookId=book.book_id,
        bookSlug=book.book_slug,
        bookTitle=book.title,
        titleSlavonic=book.title_slavonic,
    )


def kathismas_flatter(item):
    return dict(
        kathismaId=item.kathisma_id,
        kathismaTitle=item.title,
        kathismaTitleSlavonic=item.title_slavonic,
    )


def psalm_flatter(item):
    return dict(
        title=item.title,
        titleSlavonic=item.title_slavonic,
        kathismaId=item.kathisma_id,
        text=item.text,
    )
