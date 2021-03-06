def test_get_document(session, document):
    from dispatch import get

    t_document = get(db_session=session, document_id=document.id)
    assert t_document.id == document.id


def test_get_all(session, document):
    from dispatch import get_all

    t_documents = get_all(db_session=session).all()
    assert len(t_documents) > 1


def test_create(session):
    from dispatch import create
    from dispatch.document import DocumentCreate

    name = "XXX"
    resource_id = "XXX"
    resource_type = "XXX"
    weblink = "https://example.com/"

    document_in = DocumentCreate(
        name=name, resource_id=resource_id, resource_type=resource_type, weblink=weblink
    )
    document = create(db_session=session, document_in=document_in)
    assert document


def test_delete(session, document):
    from dispatch import delete, get

    delete(db_session=session, document_id=document.id)
    assert not get(db_session=session, document_id=document.id)
