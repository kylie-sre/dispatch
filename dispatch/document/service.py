from typing import List, Optional

from fastapi.encoders import jsonable_encoder

from dispatch.config import (
    INCIDENT_RESOURCE_CONVERSATION_REFERENCE_DOCUMENT,
    INCIDENT_RESOURCE_EXECUTIVE_REPORT_DOCUMENT_TEMPLATE,
    INCIDENT_RESOURCE_INCIDENT_REVIEW_DOCUMENT_TEMPLATE,
    INCIDENT_RESOURCE_INVESTIGATION_SHEET_TEMPLATE,
    INCIDENT_RESOURCE_INCIDENT_FAQ_DOCUMENT,
)
from dispatch.incident_priority import service as incident_priority_service
from dispatch.incident_type import service as incident_type_service
from dispatch.term import service as term_service

from .models import Document, DocumentCreate, DocumentUpdate


def get(*, db_session, document_id: int) -> Optional[Document]:
    """Returns a document based on the given document id."""
    return db_session.query(Document).get(document_id)


def get_by_incident_id_and_resource_type(
    *, db_session, incident_id: int, resource_type: str
) -> Optional[Document]:
    """Returns a document based on the given incident and id and document resource type."""
    return (
        db_session.query(Document)
        .filter(Document.incident_id == incident_id)
        .filter(Document.resource_type == resource_type)
        .one_or_none()
    )


def get_conversation_reference_document(*, db_session):
    """Fetches conversation reference document."""
    return (
        db_session.query(Document).filter(
            Document.resource_type == INCIDENT_RESOURCE_CONVERSATION_REFERENCE_DOCUMENT
        )
    ).one_or_none()


def get_executive_report_template(*, db_session):
    """Fetches executive report template document."""
    return (
        db_session.query(Document).filter(
            Document.resource_type == INCIDENT_RESOURCE_EXECUTIVE_REPORT_DOCUMENT_TEMPLATE
        )
    ).one_or_none()


def get_incident_review_template(*, db_session):
    """Fetches incident review template document."""
    return (
        db_session.query(Document).filter(
            Document.resource_type == INCIDENT_RESOURCE_INCIDENT_REVIEW_DOCUMENT_TEMPLATE
        )
    ).one_or_none()


def get_incident_faq_document(*, db_session):
    """Fetches incident faq docment."""
    return (
        db_session.query(Document).filter(
            Document.resource_type == INCIDENT_RESOURCE_INCIDENT_FAQ_DOCUMENT
        )
    ).one_or_none()


def get_incident_investigation_sheet_template(*, db_session):
    """Fetches incident investigation template sheet."""
    return (
        db_session.query(Document).filter(
            Document.resource_type == INCIDENT_RESOURCE_INVESTIGATION_SHEET_TEMPLATE
        )
    ).one_or_none()


def get_all(*, db_session) -> List[Optional[Document]]:
    """Returns all documents."""
    return db_session.query(Document)


def create(*, db_session, document_in: DocumentCreate) -> Document:
    """Creates a new document."""
    terms = [
        term_service.get_or_create(db_session=db_session, term_in=t) for t in document_in.terms
    ]
    incident_priorities = [
        incident_priority_service.get_by_name(db_session=db_session, name=n.name)
        for n in document_in.incident_priorities
    ]
    incident_types = [
        incident_type_service.get_by_name(db_session=db_session, name=n.name)
        for n in document_in.incident_types
    ]
    document = Document(
        **document_in.dict(exclude={"terms", "incident_priorities", "incident_types"}),
        incident_priorities=incident_priorities,
        incident_types=incident_types,
        terms=terms,
    )
    db_session.add(document)
    db_session.commit()
    return document


def update(*, db_session, document: Document, document_in: DocumentUpdate) -> Document:
    """Updates a document."""
    document_data = jsonable_encoder(document)
    update_data = document_in.dict(
        skip_defaults=True, exclude={"terms", "incident_priorities", "incident_types"}
    )

    terms = [
        term_service.get_or_create(db_session=db_session, term_in=t) for t in document_in.terms
    ]
    incident_priorities = [
        incident_priority_service.get_by_name(db_session=db_session, name=n.name)
        for n in document_in.incident_priorities
    ]
    incident_types = [
        incident_type_service.get_by_name(db_session=db_session, name=n.name)
        for n in document_in.incident_types
    ]

    for field in document_data:
        if field in update_data:
            setattr(document, field, update_data[field])

    document.terms = terms
    document.incident_priorities = incident_priorities
    document.incident_types = incident_types

    db_session.add(document)
    db_session.commit()
    return document


def delete(*, db_session, document_id: int):
    """Deletes a document."""
    db_session.query(Document).filter(Document.id == document_id).delete()
    db_session.commit()
