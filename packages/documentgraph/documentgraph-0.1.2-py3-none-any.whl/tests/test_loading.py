import pytest
from unittest.mock import Mock, patch
from documentgraph.loading import KnowledgeGraphLoader
from documentgraph.models import Entity, Relationship, TextChunk, Document
from documentgraph.config import ETLConfig


@pytest.fixture
def mock_config():
    return Mock(spec=ETLConfig)


@pytest.fixture
def loader(mock_config):
    return KnowledgeGraphLoader(mock_config)


@pytest.fixture
def sample_data():
    entities = [Entity(id="1", name="Test Entity")]
    relationships = [Relationship(source_id="1", target_id="2", type="test")]
    chunks = TextChunk(
        id="1",
        text="Test chunk",
        embedding=[0.1, 0.2, 0.3],
        entities=[Entity(id="1", name="Test Entity")],
    )
    document = Document(id="1", title="Test Document")
    return entities, relationships, chunks, document


@pytest.mark.parametrize(
    "entities,relationships,chunks,document",
    [
        (
            [],
            [],
            TextChunk(id="1", content="Empty", document_id="1", embedding=[1, 2, 3]),
            Document(id="1", filename="my_file.txt", content="Empty"),
        ),
        (sample_data()[0], sample_data()[1], sample_data()[2], sample_data()[3]),
    ],
)
def test_load_incremental(loader, entities, relationships, chunks, document):
    with patch.object(loader, "load_document") as mock_load_document, patch.object(
        loader, "load_entities"
    ) as mock_load_entities, patch.object(
        loader, "load_relationships"
    ) as mock_load_relationships, patch.object(
        loader, "load_chunks"
    ) as mock_load_chunks:

        loader.load_incremental(entities, relationships, chunks, document)

        mock_load_document.assert_called_once_with(document)
        mock_load_entities.assert_called_once_with(entities)
        mock_load_relationships.assert_called_once_with(relationships)
        mock_load_chunks.assert_called_once_with(chunks, document)


def test_load_incremental_order(loader, sample_data):
    entities, relationships, chunks, document = sample_data

    with patch.object(loader, "load_document") as mock_load_document, patch.object(
        loader, "load_entities"
    ) as mock_load_entities, patch.object(
        loader, "load_relationships"
    ) as mock_load_relationships, patch.object(
        loader, "load_chunks"
    ) as mock_load_chunks:

        loader.load_incremental(entities, relationships, chunks, document)

        call_order = [
            call.args[0]
            for call in mock_load_document.mock_calls
            + mock_load_entities.mock_calls
            + mock_load_relationships.mock_calls
            + mock_load_chunks.mock_calls
        ]

        assert call_order == [document, entities, relationships, chunks]


def test_close(loader):
    with patch.object(loader.driver, "close") as mock_close:
        loader.close()
        mock_close.assert_called_once()
