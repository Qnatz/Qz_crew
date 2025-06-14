# models.py
import time
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal

class AgentOutput(BaseModel):
    agent: str = Field(..., max_length=255, description="Name of the agent")
    role: str = Field(..., max_length=255, description="Role of the agent")
    response: str = Field(..., max_length=10000, description="Agent's response to the task")
    timestamp: float = Field(..., description="Timestamp of when the agent completed the task")
    model_used: str = Field(..., max_length=255, description="Model used by the agent")
    next_steps: Optional[str] = Field(None, max_length=1000, description="Next steps recommended by the agent")
    recommendation: Optional[str] = Field(None, max_length=1000, description="Recommendation by the agent")
    backend_code: Optional[str] = Field(None, max_length=50000, description="Backend code generated by the agent")
    ui_design: Optional[str] = Field(None, max_length=50000, description="UI design generated by the agent")
    mobile_design: Optional[str] = Field(None, max_length=50000, description="Mobile design generated by the agent")
    test_plan: Optional[str] = Field(None, max_length=10000, description="Test plan generated by the agent")
    fixed_code: Optional[str] = Field(None, max_length=50000, description="Fixed code generated by the agent")
    analysis: Optional[Dict[str, Any]] = Field(None, description="Analysis data generated by the agent")
    plan: Optional[str] = Field(None, max_length=10000, description="Plan generated by the agent")
    architecture: Optional[str] = Field(None, max_length=10000, description="Architecture generated by the agent")
    api_specs: Optional[str] = Field(None, max_length=10000, description="API specifications generated by the agent")
    start_time: Optional[float] = Field(None, description="Start time of the task")
    end_time: Optional[float] = None # Field(None, description="End time of the task")

class ProjectAnalysis(BaseModel):
    project_type: Literal["fullstack", "backend", "frontend", "mobile"] = Field(..., description="Type of the project")
    backend_needed: bool = Field(True, description="Whether a backend is needed.")
    frontend_needed: bool = Field(True, description="Whether a frontend is needed.")
    mobile_needed: bool = Field(False, description="Whether a mobile app is needed.")
    key_requirements: List[str] = Field(..., description="List of key requirements", min_items=1)


class PlatformRequirements(BaseModel):
    """Defines the required platforms for the project."""
    web: bool = Field(False, description="True if a web platform is required.")
    ios: bool = Field(False, description="True if an iOS mobile platform is required.")
    android: bool = Field(False, description="True if an Android mobile platform is required.")

class TechProposal(BaseModel):
    """Represents a single technology proposal made by an agent for a specific category."""
    proponent: str = Field(..., description="Name of the agent or role making the proposal.")
    technology: str = Field(..., description="The specific technology being proposed (e.g., 'FastAPI', 'React', 'PostgreSQL').")
    reason: str = Field(..., description="Justification for proposing this technology.")
    confidence: float = Field(..., description="The agent's confidence in this proposal (0.0 to 1.0).")
    compatibility_score: Optional[float] = Field(None, description="Optional score indicating compatibility with other stack components or requirements.")
    effort_estimate: Optional[str] = Field(None, description="Estimated effort to implement/integrate this technology (e.g., 'low', 'medium', 'high').")

class ApprovedTechStack(BaseModel):
    """Represents the final approved technology stack after negotiation and conflict resolution."""
    web_backend: Optional[str] = Field(None, description="Chosen web backend technology (e.g., 'FastAPI', 'Node.js with Express'). Could also store hybrid descriptions.")
    mobile_database: Optional[str] = Field(None, description="Chosen mobile database technology (e.g., 'SQLite', 'RoomDB + Firestore sync').")
    media_storage: Optional[str] = None
    core: Optional[List[str]] = None
    pdf_generation: Optional[str] = None
    background_work: Optional[str] = None

# Models for Planner Agent's structured JSON output
class PlannerTaskModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the task (e.g., '1.1', '1.2').")
    description: str = Field(..., description="Detailed description of the task.")
    assignee_type: str = Field(..., description="Suggested type of assignee (e.g., 'developer', 'architect', 'agent_or_human_suggestion').")

class PlannerMilestoneModel(BaseModel):
    name: str = Field(..., description="Name of the milestone (e.g., 'Milestone 1: Setup and Core Data Model').")
    description: str = Field(..., description="Brief description of this milestone's overall goal.")
    tasks: List[PlannerTaskModel] = Field(..., description="List of tasks for this milestone. Detailed for M1, can be empty or high-level for others.")

class PlannerRiskModel(BaseModel):
    risk: str = Field(..., description="Description of a potential risk to the project.")
    mitigation: str = Field(..., description="Proposed strategy to mitigate this risk.")

class PlannerOutputModel(BaseModel):
    milestones: List[PlannerMilestoneModel] = Field(..., description="List of all project milestones.")
    key_risks: List[PlannerRiskModel] = Field(..., description="List of key risks identified for the project and their mitigation strategies.")

# Models for APIDesigner Agent's OpenAPI JSON output validation
class OpenAPIInfoModel(BaseModel):
    title: str = Field(..., description="The title of the API.")
    version: str = Field(..., description="The version of the OpenAPI document (e.g., '1.0.0').")
    description: Optional[str] = Field(None, description="A short description of the API. CommonMark syntax MAY be used for rich text representation.")

class OpenAPIPathItemObjectModel(BaseModel):
    summary: Optional[str] = Field(None, description="An optional, string summary, intended to apply to all operations in this path.")
    description: Optional[str] = Field(None, description="An optional, string description, intended to apply to all operations in this path. CommonMark syntax MAY be used for rich text representation.")
    parameters: Optional[List[Dict[str, Any]]] = Field(None, description="A list of parameters that are applicable for all the operations described under this path. These parameters can be overridden at the Nperation level, but cannot be removed there.")
    responses: Dict[str, Any] = Field(..., description="A declaration of the responses to be expected for requests to this path.")
    # Common HTTP methods; can be expanded. Using Dict[str, Any] for flexibility in defining operations.
    get: Optional[Dict[str, Any]] = None
    put: Optional[Dict[str, Any]] = None
    post: Optional[Dict[str, Any]] = None
    delete: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None
    head: Optional[Dict[str, Any]] = None
    patch: Optional[Dict[str, Any]] = None
    trace: Optional[Dict[str, Any]] = None


class OpenAPISchemaModel(BaseModel):
    type: Optional[str] = Field(None, description="Data type of the schema.") # Optional because of 'oneOf', 'anyOf', etc.
    properties: Optional[Dict[str, Any]] = Field(None, description="Object properties. Ignored if type is not 'object'.")
    example: Optional[Any] = Field(None, description="A free-form example of an instance of this schema.")
    items: Optional[Dict[str, Any]] = Field(None, description="Describes the type of items in the array. Required if type is 'array'.") # Should ideally be OpenAPISchemaModel but causes recursion. Dict for now.
    format: Optional[str] = Field(None, description="The format of the data (e.g., 'int32', 'date-time').")
    description: Optional[str] = Field(None, description="A description of the schema. CommonMark syntax MAY be used.")
    default: Optional[Any] = Field(None, description="Default value for the schema.")
    required: Optional[List[str]] = Field(None, description="List of required property names. Only applicable for 'object' type.")
    # Support for references
    ref: Optional[str] = Field(None, alias="$ref", description="A JSON Reference to another schema component.")


class OpenAPIFlowModel(BaseModel):
    tokenUrl: Optional[str] = Field(None, description="The token URL to be used for this flow. This MUST be in the form of a URL.")
    scopes: Optional[Dict[str, str]] = Field(None, description="The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it.")
    refreshUrl: Optional[str] = Field(None, description="The URL to be used for obtaining refresh tokens. This MUST be in the form of a URL.")

class OpenAPISecuritySchemeFlowsModel(BaseModel):
    clientCredentials: Optional[OpenAPIFlowModel] = Field(None, description="Configuration for the Client Credentials flow.")
    authorizationCode: Optional[OpenAPIFlowModel] = Field(None, description="Configuration for the Authorization Code flow.")
    implicit: Optional[OpenAPIFlowModel] = Field(None, description="Configuration for the Implicit flow.")
    password: Optional[OpenAPIFlowModel] = Field(None, description="Configuration for the Resource Owner Password flow.")

class OpenAPISecuritySchemeModel(BaseModel):
    type: str = Field(..., description="The type of the security scheme (e.g., 'apiKey', 'http', 'oauth2', 'openIdConnect').")
    flows: Optional[OpenAPISecuritySchemeFlowsModel] = Field(None, description="An object containing configuration information for the flow types supported.")
    description: Optional[str] = Field(None, description="A short description for security scheme. CommonMark syntax MAY be used.")
    name: Optional[str] = Field(None, description="The name of the header, query or cookie parameter to be used. Required for 'apiKey' type.")
    in_val: Optional[str] = Field(None, alias="in", description="The location of the API key. Required for 'apiKey' type. Valid values are 'query', 'header' or 'cookie'.")
    scheme: Optional[str] = Field(None, description="The name of the HTTP Authorization scheme to be used in the Authorization header defined in RFC7235. Required for 'http' type.")
    bearerFormat: Optional[str] = Field(None, description="A hint to the client to identify how the bearer token is formatted. Bearer tokens are defined in RFC6750. Relevant for 'http' type with 'bearer' scheme.")


class OpenAPIComponentsModel(BaseModel):
    schemas: Optional[Dict[str, OpenAPISchemaModel]] = Field(None, description="An object to hold reusable Schema Objects.")
    securitySchemes: Optional[Dict[str, OpenAPISecuritySchemeModel]] = Field(None, description="An object to hold reusable Security Scheme Objects.")
    parameters: Optional[Dict[str, Any]] = Field(None, description="An object to hold reusable Parameter Objects.") # Values are Parameter Objects
    responses: Optional[Dict[str, Any]] = Field(None, description="An object to hold reusable Response Objects.") # Values are Response Objects

class APIDesignerOutputModel(BaseModel):
    openapi: str = Field(default="3.0.0", description="OpenAPI version string (e.g., '3.0.0', '3.0.1').")
    info: OpenAPIInfoModel = Field(..., description="Provides metadata about the API.")
    paths: Dict[str, Any] = Field(..., description="The available paths and operations for the API. Values are Path Item Objects.") # PathItemObjectModel would be more specific but Any for now
    components: Optional[OpenAPIComponentsModel] = Field(None, description="An element to hold various schemas for the OpenAPI document.")
    security: Optional[List[Dict[str, List[str]]]] = Field(None, description="A declaration of which security mechanisms can be used across the API. Each item references a security scheme declared in components.securitySchemes.")

# Models for Architect Agent's structured JSON output
class ArchDesignModel(BaseModel):
    diagram: str = Field(..., description="CONCISE Component Diagram or Directory Structure, textual if needed, using fixed stack technologies.")
    description: str = Field(..., description="CONCISE Description of components and interactions, using fixed stack technologies. Use bullet points for key features.")
    justification: str = Field(..., description="CONCISE Justification of architectural decisions within the given stack. Use bullet points.")

class ArchitectOutputModel(BaseModel):
    architecture_design: ArchDesignModel = Field(..., description="The core architecture design details.")
    tech_proposals: Optional[Dict[str, List[TechProposal]]] = Field(None, description="Technology proposals, categorized by area. TechProposal model is already defined and imported.")

# Models for MobileDeveloper Agent's structured JSON output
class MobileDetailsModel(BaseModel):
    component_structure: str = Field(..., description="CONCISE bullet-point list of key mobile components and hierarchy.")
    navigation: str = Field(..., description="CONCISE bullet-point description of navigation flow.")
    state_management: str = Field(..., description="CONCISE bullet-point description of state management approach.")
    api_integration: str = Field(..., description="CONCISE bullet-point list of API integration points.")
    framework_solutions: str = Field(..., description="CONCISE bullet-point list of specific framework solutions/libraries.")

class MobileOutputModel(BaseModel):
    mobile_details: MobileDetailsModel = Field(..., description="The core details of the mobile application design.")
    tech_proposals: Optional[Dict[str, List[TechProposal]]] = Field(None, description="Technology proposals, categorized by area. TechProposal model is already defined and imported.")