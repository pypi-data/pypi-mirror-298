# System imports
from typing import List, Dict, Tuple, Union
from functools import lru_cache
from datetime import datetime
from enum import Enum
import asyncio
import json
import uuid
import math

# Third party imports
from chromadb.config import Settings
import networkx as nx
import chromadb

# LLMCore imports
from llmcore.prompt import PromptTemplate, Prompt
from llmcore.embeddings import Embeddings
from llmcore.core import LLM, LLMConfig

class Source:
    def __init__(self, url: str, credibility: float):
        self.url = url
        self.credibility = credibility

    def validate_credibility(self, credibility: float) -> float:
        """
        Validates and normalizes the credibility score.
        
        Args:
            credibility (float): The initial credibility score.
        
        Returns:
            float: A normalized credibility score between 0.0 and 1.0.
        """
        if not isinstance(credibility, (int, float)):
            raise ValueError("Credibility must be a numeric value.")
        return max(0.0, min(credibility, 1.0))
    
    def update_credibility(self, new_credibility: float):
        """
        Updates the credibility score with validation.
        
        Args:
            new_credibility (float): The new credibility score.
        """
        self.credibility = self.validate_credibility(new_credibility)

class ConceptCategory(Enum):
    # Broad, vague categories to be able to cover as much as possible
    # and then have the LLM refine them into more specific categories
    # as it gets more examples.
    ART = "Art"
    SCIENCE = "Science"
    HISTORY = "History"
    GEOGRAPHY = "Geography"
    POLITICS = "Politics"
    CULTURE = "Culture"
    TECHNOLOGY = "Technology"
    ENVIRONMENT = "Environment"
    HEALTH = "Health"
    EDUCATION = "Education"
    ECONOMICS = "Economics"
    LAW = "Law"
    RELIGION = "Religion"
    PHILOSOPHY = "Philosophy"
    MATH = "Math"
    LANGUAGE = "Language"
    MUSIC = "Music"
    SPORTS = "Sports"
    TRAVEL = "Travel"
    FOOD = "Food"
    FASHION = "Fashion"
    FILM = "Film"
    TV = "TV"
    BOOKS = "Books"
    OTHER = "Other"

class Concept:
    def __init__(
        self,
        name: str,
        description: str,
        category: ConceptCategory,
        sources: List[Dict[str, any]],
        tags: List[str] = None,
        significance: float = 1.0  # Default significance
    ):
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.description: str = description
        self.category: ConceptCategory = category
        self.sources: List[Source] = [Source(**s) if isinstance(s, dict) else s for s in sources]
        self.tags: List[str] = tags or []
        self.significance: float = self.validate_significance(significance)
        self.versions: List[Dict[str, any]] = [{
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "tags": self.tags,
            "significance": self.significance
        }]

    def validate_significance(self, significance: float) -> float:
        """
        Validates and normalizes the significance score.
        
        Args:
            significance (float): The initial significance score.
        
        Returns:
            float: A normalized significance score between 0.0 and 1.0.
        """
        if not isinstance(significance, (int, float)):
            raise ValueError("Significance must be a numeric value.")
        return max(0.0, min(significance, 1.0))

    def update(
        self,
        description: str,
        sources: List[Dict[str, any]],
        tags: List[str] = None,
        significance: float = None
    ):
        self.description = description
        self.sources = [Source(**s) if isinstance(s, dict) else s for s in sources]
        if tags is not None:
            self.tags = tags
        if significance is not None:
            self.significance = self.validate_significance(significance)
        self.versions.append({
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "tags": self.tags,
            "significance": self.significance
        })

    def to_dict(self) -> Dict[str, any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "tags": self.tags,
            "significance": self.significance,
            "sources": [{"url": s.url, "credibility": s.credibility} for s in self.sources],
            "versions": self.versions
        }

class Relationship:
    def __init__(self, source: str, target: str, rel_type: str, strength: float):
        self.id = str(uuid.uuid4())
        self.source = source
        self.target = target
        self.type = rel_type
        self.strength = strength
        self.versions = [{
            "timestamp": datetime.now().isoformat(),
            "type": rel_type,
            "strength": strength
        }]

    def update(self, rel_type: str, strength: float):
        self.type = rel_type
        self.strength = strength
        self.versions.append({
            "timestamp": datetime.now().isoformat(),
            "type": rel_type,
            "strength": strength
        })

    def to_dict(self) -> Dict[str, any]:
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "type": self.type,
            "strength": self.strength,
            "versions": self.versions
        }

class EmbeddingManager:
    def __init__(self, provider: str, model: str):
        self.embeddings = Embeddings(provider=provider, model=model)
    
    async def embed_text(self, text: str) -> List[float]:
        return await self.embeddings.embed_async(text)

class LLMHandler:
    def __init__(self, provider: str, model: str, temperature: float, max_tokens: int):
        self.llm = LLM(provider=provider, model=model, config=LLMConfig(temperature=temperature, max_tokens=max_tokens))
    
    async def send_prompt(self, prompt: Prompt, parse_json: bool = False) -> Union[str, Dict[str, any]]:
        response = await self.llm.send_input_async(prompt, parse_json=parse_json)
        return response

class KnowledgeGraph:
    def __init__(self):
        # The graph is a multidigraph, which allows for multiple edges between two nodes
        # with different relationship types and strengths. This allows for more complex
        # relationships to be represented and leveraged by the LLM.
        self.graph = nx.MultiDiGraph()
        
        # The embedding manager is used to create vector embeddings for the knowledge graph,
        # queries and other inputs. This allows for efficient similarity searches and 
        # other operations to be performed on the graph.
        self.embedding_manager = EmbeddingManager(provider="openai", model="text-embedding-3-small")

        # The LLM handler is used to send prompts to the LLM and handle the responses specifically
        # for operations related to the knowledge graph.
        try:
            self.llm_handler = LLMHandler(
                provider="google",
                model="gemini-1.5-flash",
                temperature=0.7,
                max_tokens=1500
            )
        except Exception as e1:
            try:
                self.llm_handler = LLMHandler(
                    provider="openai",
                    model="gpt-4o-mini",
                    temperature=0.7,
                    max_tokens=1500
                )
            except Exception as e2:
                try:
                    self.llm_handler = LLMHandler(
                        provider="anthropic",
                        model="claude-3-haiku",
                        temperature=0.7,
                        max_tokens=1500
                    )
                except Exception as e3:
                    raise RuntimeError(f"Failed to initialize any LLM for a knowledge graph: {str(e1)}, {str(e2)}, {str(e3)}")
        
        # The ChromaDB client is used to interact with the ChromaDB database, which is used to
        # store the knowledge graph as a vector database. This allows for efficient retrieval and
        # similarity searches based on the concept's embedding vector.
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./knowledge_graph"
        ))
        
        # The collection is used to store the concepts and relationships in the graph.
        collection_name = "knowledge_graph"
        try:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_manager.embeddings.embed
            )
        except ValueError as e:
            if "already exists" in str(e):
                self.collection = self.client.get_collection(
                    name=collection_name,
                    embedding_function=self.embedding_manager.embeddings.embed
                )
            else:
                raise
        
        # Decay cache is a concept that allows us to decay the confidence of a concept over time
        # if it is not used or updated. This is useful for concepts that are not used or updated
        # as often as others and allows us to decay them over time. This is useful for keeping
        # the knowledge graph up to date and relevant. (Potential Improvement: Figure out what is
        # the difference between knowledge that can decay over time versus knowledge that cannot.
        # For example, gravity will always be 9.81 m/s^2, but a concept like COVID-19 may decay
        # over time as our knowledge of the virus and its mutation evolves.
        self.decay_cache = {}

    async def add_concept(
        self,
        name: str,
        description: str,
        category: Union[ConceptCategory, str],
        sources: List[Dict[str, any]],
        tags: List[str] = None,
        significance: float = 1.0,
        initial_relationships: List[Dict[str, any]] = None
    ) -> str:
        """
        Add a new concept to the knowledge graph.

        Args:
            name (str): Name of the concept.
            description (str): Description of the concept.
            category (Category): Category of the concept.
            sources (List[Dict[str, any]]): Sources supporting the concept.
            tags (List[str], optional): Tags for better categorization.
            significance (float, optional): Importance of the concept.
            initial_relationships (List[Dict[str, any]], optional): 
                Relationships to establish upon creation.

        Returns:
            str: The ID of the added concept.
        """
        try:
            # Create a new Concept instance and generate an embedding vector
            # based on the provided description.
            concept = Concept(
                name=name,
                description=description,
                category=ConceptCategory(category),
                sources=sources,
                tags=tags,
                significance=significance
            )
        except ValueError as e:
            if "not a valid ConceptCategory" in str(e):
                # Use the LLM to refine the category
                refine_category_prompt = PromptTemplate(
                    "Given the following category that is not valid: '{{category}}'\n\n"
                    "Determine the most appropriate category from the following options: {{categories}}\n\n"
                    "Return the category name as the matching string.",
                    required_params={"category": str, "categories": str},
                    output_json_structure={"refined_category": str}
                ).create_prompt(
                    category=category,
                    categories=','.join([c.value for c in ConceptCategory])
                )
                refined_category = await self.llm_handler.send_prompt(refine_category_prompt, parse_json=True)

                category = ConceptCategory(refined_category["refined_category"])

                concept = Concept(
                    name=name,
                    description=description,
                    category=category,
                    sources=sources,
                    tags=tags,
                    significance=significance
                )
            else:
                raise e
        except Exception as e:
            raise e

        vector = await self.embedding_manager.embed_text(description)

        # Add the concept to the collection, which serves as a storage for concept embeddings, 
        # associated documents, and metadata. This allows for efficient retrieval and 
        # similarity searches based on the concept's embedding vector.
        self.collection.add(
            embeddings=[vector],
            documents=[json.dumps(concept.to_dict())],
            metadatas=[{
                "id": concept.id,
                "name": name,
                "category": category.value,
                "tags": ",".join(tags) if tags else "",
                "significance": significance
            }],
            ids=[concept.id]
        )

        # Add the concept to the graph with its ID as the node identifier
        # and process any initial relationships for the concept.
        self.graph.add_node(concept.id, concept=concept)
        if initial_relationships:
            # Prepare the relationships for adding to the graph. This needs to 
            # be done to ensure the correct concept is associated with each relationship.s
            relationships = [
                {
                    'source_id': concept.id,
                    'target_id': rel['target_id'],
                    'rel_type': rel['rel_type'],
                    'strength': rel['strength']
                }
                for rel in initial_relationships
            ]
            await self.add_multiple_relationships(relationships)
        
        return concept.id

    async def update_concept(
        self,
        concept_id: str,
        new_description: str,
        new_sources: List[Dict[str, any]],
        new_tags: List[str] = None,
        new_significance: float = None
    ):
        concept = self.graph.nodes[concept_id]['concept']
        concept.update(new_description, new_sources, new_tags, new_significance)
        vector = await self.embedding_manager.embed_text(new_description)
        self.collection.update(
            embeddings=[vector],
            documents=[json.dumps(concept.to_dict())],
            metadatas=[{
                "id": concept.id,
                "name": concept.name,
                "category": concept.category.value,
                "tags": ",".join(new_tags) if new_tags is not None else ",".join(concept.tags),
                "significance": new_significance if new_significance is not None else concept.significance
            }],
            ids=[concept.id]
        )

    async def add_relationship(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        strength: float
    ) -> str:
        relationship = Relationship(source_id, target_id, rel_type, strength)
        self.graph.add_edge(source_id, target_id, key=relationship.id, relationship=relationship)
        return relationship.id

    async def add_multiple_relationships(
        self,
        relationships: List[Dict[str, any]]
    ) -> List[str]:
        """
        Add multiple relationships to the knowledge graph.

        Args:
            relationships (List[Dict[str, any]]): A list of relationships with keys:
                - source_id (str)
                - target_id (str)
                - rel_type (str)
                - strength (float)

        Returns:
            List[str]: A list of added relationship IDs.
        """
        rel_ids = []
        for rel in relationships:
            rel_id = await self.add_relationship(
                source_id=rel['source_id'],
                target_id=rel['target_id'],
                rel_type=rel['rel_type'],
                strength=rel['strength']
            )
            rel_ids.append(rel_id)
        return rel_ids

    async def update_relationship(
        self,
        rel_id: str,
        new_type: str,
        new_strength: float
    ):
        for _, _, data in self.graph.edges(data=True):
            if data.get('key') == rel_id:
                relationship = data['relationship']
                relationship.update(new_type, new_strength)
                break

    def get_all_concepts(self) -> List[Concept]:
        return [data['concept'] for _, data in self.graph.nodes(data=True)]

    def get_all_relationships(self) -> List[Dict[str, any]]:
        """
        Retrieve all relationships in the knowledge graph.

        Returns:
            List[Dict[str, any]]: A list of relationships with details.
        """
        relationships = []
        for source_id, target_id, data in self.graph.edges(data=True):
            relationship: Relationship = data['relationship']
            relationships.append({
                "source": self.graph.nodes[source_id]['concept'].name,
                "target": self.graph.nodes[target_id]['concept'].name,
                "type": relationship.type,
                "strength": relationship.strength
            })
        return relationships

    async def get_concept_history(self, concept_id: str) -> List[dict]:
        concept = self.graph.nodes[concept_id]['concept']
        return concept.versions

    async def get_related_concepts(self, concept_id: str) -> List[Concept]:
        """
        Retrieve all concepts related to a given concept.

        Args:
            concept_id (str): The ID of the concept.

        Returns:
            List[Concept]: A list of related concepts.
        """
        related_concepts = []
        for _, target_id, data in self.graph.edges(concept_id, data=True):
            related_concepts.append(self.graph.nodes[target_id]['concept'])
        return related_concepts

    async def query_graph(self, query: str) -> List[Concept]:
        """
        Perform a semantic search on the knowledge graph based on the query. Practically, this
        means that users can ask questions and the graph will return a list of concepts that
        are most relevant to the query.

        Args:
            query (str): The search query.

        Returns:
            List[Concept]: A list of concepts relevant to the query.
        """
        # Embed the query and perform a similarity search on the collection.
        vector = await self.embedding_manager.embed_text(query)

        # Perform a similarity search on the collection to find the most relevant concepts.
        results = self.collection.query(
            query_embeddings=[vector],
            n_results=5
        )
        concept_ids = results['ids'][0]
        concepts = []
        for c_id in concept_ids:
            if c_id in self.graph:
                concept = self.graph.nodes[c_id]['concept']
                # Convert tags back to a list if they were stored as a string
                if isinstance(concept.tags, str):
                    concept.tags = concept.tags.split(',') if concept.tags else []
                concepts.append(concept)
        return concepts

    async def contextual_query(self, query: str) -> Dict[str, any]:
        initial_results = await self.query_graph(query)
        
        prompt = PromptTemplate(
            "Given the query: '{{query}}'\n\n"
            "And the following initial results from our knowledge graph:\n{{initial_results}}\n\n"
            "1. Identify the most relevant concepts and explain why they are relevant.\n"
            "2. Perform multi-hop reasoning to connect these concepts and provide insights.\n"
            "3. Synthesize a comprehensive answer to the query based on the available information.\n"
            "4. Suggest any missing information or areas where the knowledge graph could be expanded.\n"
            "Format your response as a JSON object.",
            required_params={"query": str, "initial_results": str},
            output_json_structure={
                "relevant_concepts": List[Dict[str, str]],
                "reasoning_path": List[str],
                "synthesized_answer": str,
                "knowledge_gaps": List[str]
            }
        ).create_prompt(
            query=query,
            initial_results=json.dumps(initial_results, indent=2)
        )
        
        contextual_response = await self.llm_handler.send_prompt(prompt)
        
        # Use the identified knowledge gaps to suggest new concepts or relationships
        for gap in contextual_response.get('knowledge_gaps', []):
            await self.suggest_new_concepts(gap)
        
        return contextual_response

    async def suggest_new_concepts(self, num_suggestions: int = 5) -> List[Dict[str, any]]:
        all_concepts = [data['concept'].name for _, data in self.graph.nodes(data=True)]
        prompt = PromptTemplate(
            "Based on the following concepts in our knowledge graph:\n{{concepts}}\n\n"
            "Suggest {{num_suggestions}} new related concepts that are not in the list above. "
            "For each concept, provide a name, brief description, category, estimated confidence level (0-1), "
            "and abstraction level (beginner, intermediate, expert).\n"
            "Format your response as a JSON list of objects.",
            required_params={"concepts": str, "num_suggestions": int},
            output_json_structure=[{
                "name": str,
                "description": str,
                "category": str,
                "confidence": float,
                "abstraction_level": str
            }]
        ).create_prompt(
            concepts=", ".join(all_concepts),
            num_suggestions=num_suggestions
        )
        new_concepts = await self.llm_handler.send_prompt(prompt)
        for concept in new_concepts:
            await self.add_concept(
                name=concept["name"],
                description=concept["description"],
                category=concept["category"],
                confidence=concept["confidence"],
                sources=[{"url": "AI-generated", "credibility": 0.8}],
                abstraction_level=concept["abstraction_level"]
            )
        return new_concepts

    async def generate_evolution_summary(self, concept_id: str) -> str:
        concept = self.graph.nodes[concept_id]['concept']
        prompt = f"""
        Analyze the evolution of the concept "{concept.name}" based on its version history:
        {json.dumps(concept.versions, indent=2)}
        
        Provide a concise summary of how this concept has evolved over time, 
        noting any significant changes in description, confidence, or abstraction level.
        Also, mention any changes in the credibility of sources used.
        """
        summary = await self.llm_handler.send_prompt(prompt)
        return summary

    @lru_cache(maxsize=1000)
    async def should_concept_decay(self, concept_name: str, category: str) -> bool:
        prompt = PromptTemplate(
            "Determine if the concept '{{concept}}' in category '{{category}}' should undergo confidence decay. Respond with 'Yes' or 'No'.",
            required_params={"concept": str, "category": str},
            output_json_structure={"decision": str}
        ).create_prompt(concept=concept_name, category=category)
        response = await self.llm_handler.send_prompt(prompt)
        return response.get("decision", "").lower() == "yes"

    async def apply_confidence_decay(
        self,
        decay_rate: float = 0.1,
        batch_size: int = 50
    ):
        current_time = datetime.now()
        concepts = list(self.graph.nodes(data='concept'))
        
        for i in range(0, len(concepts), batch_size):
            batch = concepts[i:i+batch_size]
            decay_checks = await asyncio.gather(*[
                self.should_concept_decay(c.name, c.category) for _, c in batch
            ])
            
            for (node_id, concept), should_decay in zip(batch, decay_checks):
                last_update = datetime.fromisoformat(concept.versions[-1]['timestamp'])
                time_diff = (current_time - last_update).days

                if should_decay:
                    decay_factor = math.exp(-decay_rate * time_diff)
                    concept.confidence *= decay_factor
                    if concept.confidence < 0.5:
                        print(f"Warning: Confidence for concept '{concept.name}' has dropped below 0.5. Consider updating.")
                else:
                    print(f"Concept '{concept.name}' does not decay over time. Confidence remains at {concept.confidence:.2f}")
