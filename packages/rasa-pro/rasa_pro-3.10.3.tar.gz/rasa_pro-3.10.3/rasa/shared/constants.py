from __future__ import annotations

from typing import List, Text

from rasa.shared.engine.caching import get_local_cache_location

DOCS_BASE_URL = "https://rasa.com/docs/rasa-pro"
DOCS_URL_CONCEPTS = DOCS_BASE_URL + "/concepts"
DOCS_URL_NLU_BASED = DOCS_BASE_URL + "/nlu-based-assistants"

# Docs URLs for CALM assistants
DOCS_URL_SLOTS = DOCS_URL_CONCEPTS + "/domain#slots"
DOCS_URL_RESPONSES = DOCS_URL_CONCEPTS + "/responses"
DOCS_URL_POLICIES = DOCS_URL_CONCEPTS + "/policies/policy-overview"
DOCS_URL_ACTIONS = DOCS_URL_CONCEPTS + "/actions"
DOCS_URL_DEFAULT_ACTIONS = DOCS_URL_CONCEPTS + "/default-actions"
DOCS_URL_COMPONENTS = DOCS_URL_CONCEPTS + "/components/overview"
DOCS_URL_GRAPH_COMPONENTS = DOCS_URL_CONCEPTS + "/components/custom-graph-components"
DOCS_URL_GRAPH_RECIPE = DOCS_URL_CONCEPTS + "/components/graph-recipe"
DOCS_URL_CATEGORICAL_SLOTS = DOCS_URL_CONCEPTS + "/domain#categorical-slot"
DOCS_URL_DOMAIN = DOCS_URL_CONCEPTS + "/domain"

# Docs URLs for NLU-based assistants
DOCS_URL_TRAINING_DATA = DOCS_URL_NLU_BASED + "/training-data-format"
DOCS_URL_TRAINING_DATA_NLU = DOCS_URL_TRAINING_DATA + "#nlu-training-data"
DOCS_URL_DOMAINS = DOCS_URL_NLU_BASED + "/domain"
DOCS_URL_NLU_BASED_SLOTS = DOCS_URL_DOMAINS + "#slots"
DOCS_URL_INTENTS = DOCS_URL_DOMAINS + "#intents"
DOCS_URL_ENTITIES = DOCS_URL_DOMAINS + "#entities"
DOCS_URL_STORIES = DOCS_URL_NLU_BASED + "/stories"
DOCS_URL_RULES = DOCS_URL_NLU_BASED + "/rules"
DOCS_URL_FORMS = DOCS_URL_NLU_BASED + "/forms"
DOCS_URL_PIPELINE = DOCS_URL_NLU_BASED + "/model-configuration"
DOCS_URL_NLU_BASED_POLICIES = DOCS_URL_NLU_BASED + "/policies"

# Other docs URLs
DOCS_URL_MARKERS = DOCS_BASE_URL + "/operating/analytics/realtime-markers"
DOCS_URL_CONNECTORS = DOCS_BASE_URL + "/connectors/messaging-and-voice-channels"
DOCS_URL_CONNECTORS_SLACK = DOCS_BASE_URL + "/connectors/slack"
DOCS_URL_EVENT_BROKERS = DOCS_BASE_URL + "/production/event-brokers"
DOCS_URL_PIKA_EVENT_BROKER = DOCS_URL_EVENT_BROKERS + "#pika-event-broker"
DOCS_URL_TRACKER_STORES = DOCS_BASE_URL + "/production/tracker-stores"
DOCS_URL_MIGRATION_GUIDE = DOCS_BASE_URL + "/migration-guide"
DOCS_URL_TELEMETRY = DOCS_BASE_URL + "/telemetry/telemetry"

INTENT_MESSAGE_PREFIX = "/"

PACKAGE_NAME = "rasa"
NEXT_MAJOR_VERSION_FOR_DEPRECATIONS = "4.0.0"

MODEL_CONFIG_SCHEMA_FILE = "shared/utils/schemas/model_config.yml"
CONFIG_SCHEMA_FILE = "shared/utils/schemas/config.yml"
RESPONSES_SCHEMA_FILE = "shared/nlu/training_data/schemas/responses.yml"
SCHEMA_EXTENSIONS_FILE = "shared/utils/pykwalify_extensions.py"
ASSERTIONS_SCHEMA_FILE = "e2e_test/assertions_schema.yml"
ASSERTIONS_SCHEMA_EXTENSIONS_FILE = "e2e_test/pykwalify_extensions.py"
LATEST_TRAINING_DATA_FORMAT_VERSION = "3.1"

DOMAIN_SCHEMA_FILE = "shared/utils/schemas/domain.yml"

DEFAULT_SESSION_EXPIRATION_TIME_IN_MINUTES = 60
DEFAULT_CARRY_OVER_SLOTS_TO_NEW_SESSION = True

DEFAULT_NLU_FALLBACK_INTENT_NAME = "nlu_fallback"

DEFAULT_E2E_TESTS_PATH = "."
TEST_STORIES_FILE_PREFIX = "test_"

LOG_LEVEL_NAME_TO_LEVEL = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}

DEFAULT_LOG_LEVEL = "INFO"
ENV_LOG_LEVEL = "LOG_LEVEL"
DEFAULT_LOG_LEVEL_LLM = "DEBUG"
ENV_LOG_LEVEL_LLM = "LOG_LEVEL_LLM"
ENV_LOG_LEVEL_LLM_MODULE_NAMES = {
    "LLMCommandGenerator": "LOG_LEVEL_LLM_COMMAND_GENERATOR",
    "SingleStepLLMCommandGenerator": "LOG_LEVEL_LLM_COMMAND_GENERATOR",
    "MultiStepLLMCommandGenerator": "LOG_LEVEL_LLM_COMMAND_GENERATOR",
    "EnterpriseSearchPolicy": "LOG_LEVEL_LLM_ENTERPRISE_SEARCH",
    "IntentlessPolicy": "LOG_LEVEL_LLM_INTENTLESS_POLICY",
    "ContextualResponseRephraser": "LOG_LEVEL_LLM_REPHRASER",
    "NLUCommandAdapter": "LOG_LEVEL_NLU_COMMAND_ADAPTER",
    "LLMBasedRouter": "LOG_LEVEL_LLM_BASED_ROUTER",
}
TCP_PROTOCOL = "TCP"

DEFAULT_SENDER_ID = "default"
UTTER_PREFIX = "utter_"
UTTER_ASK_PREFIX = "utter_ask_"
ACTION_ASK_PREFIX = "action_ask_"
FLOW_PREFIX = "flow_"

ASSISTANT_ID_KEY = "assistant_id"
ASSISTANT_ID_DEFAULT_VALUE = "placeholder_default"

CONFIG_MANDATORY_COMMON_KEYS = [ASSISTANT_ID_KEY]
CONFIG_AUTOCONFIGURABLE_KEYS_CORE = ["policies"]
CONFIG_AUTOCONFIGURABLE_KEYS_NLU = ["pipeline"]
CONFIG_AUTOCONFIGURABLE_KEYS = (
    CONFIG_AUTOCONFIGURABLE_KEYS_CORE + CONFIG_AUTOCONFIGURABLE_KEYS_NLU
)
CONFIG_KEYS_CORE = ["policies"] + CONFIG_MANDATORY_COMMON_KEYS
CONFIG_KEYS_NLU = ["language", "pipeline"] + CONFIG_MANDATORY_COMMON_KEYS
CONFIG_KEYS = CONFIG_KEYS_CORE + CONFIG_KEYS_NLU
CONFIG_MANDATORY_KEYS_CORE: List[Text] = [] + CONFIG_MANDATORY_COMMON_KEYS
CONFIG_MANDATORY_KEYS_NLU = ["language"] + CONFIG_MANDATORY_COMMON_KEYS
CONFIG_MANDATORY_KEYS = CONFIG_MANDATORY_KEYS_CORE + CONFIG_MANDATORY_KEYS_NLU

# Keys related to Forms (in the Domain)
REQUIRED_SLOTS_KEY = "required_slots"
IGNORED_INTENTS = "ignored_intents"

# Constants for default Rasa Pro project layout
DEFAULT_ENDPOINTS_PATH = "endpoints.yml"
DEFAULT_CREDENTIALS_PATH = "credentials.yml"
DEFAULT_CONFIG_PATH = "config.yml"
DEFAULT_DOMAIN_PATHS = ["domain.yml", "domain"]
DEFAULT_DOMAIN_PATH = DEFAULT_DOMAIN_PATHS[0]
DEFAULT_ACTIONS_PATH = "actions"
DEFAULT_MODELS_PATH = "models"
DEFAULT_CONVERTED_DATA_PATH = "converted_data"
DEFAULT_DATA_PATH = "data"
DEFAULT_RESULTS_PATH = "results"
DEFAULT_NLU_RESULTS_PATH = "nlu_comparison_results"
DEFAULT_CORE_SUBDIRECTORY_NAME = "core"
DEFAULT_NLU_SUBDIRECTORY_NAME = "nlu"
DEFAULT_CONVERSATION_TEST_PATH = "tests"
DEFAULT_MARKERS_PATH = "markers"
DEFAULT_MARKERS_CONFIG_PATH = "markers/config"
DEFAULT_MARKERS_OUTPUT_PATH = "markers/output"
DEFAULT_MARKERS_STATS_PATH = "markers/stats"

DIAGNOSTIC_DATA = "diagnostic_data"

RESPONSE_CONDITION = "condition"
CHANNEL = "channel"

API_KEY = "api_key"

AZURE_API_KEY_ENV_VAR = "AZURE_API_KEY"
AZURE_AD_TOKEN_ENV_VAR = "AZURE_AD_TOKEN"
AZURE_API_BASE_ENV_VAR = "AZURE_API_BASE"
AZURE_API_VERSION_ENV_VAR = "AZURE_API_VERSION"
AZURE_API_TYPE_ENV_VAR = "AZURE_API_TYPE"

OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"
OPENAI_API_TYPE_ENV_VAR = "OPENAI_API_TYPE"
OPENAI_API_VERSION_ENV_VAR = "OPENAI_API_VERSION"
OPENAI_API_BASE_ENV_VAR = "OPENAI_API_BASE"

OPENAI_API_BASE_CONFIG_KEY = "openai_api_base"
OPENAI_API_TYPE_CONFIG_KEY = "openai_api_type"
OPENAI_API_VERSION_CONFIG_KEY = "openai_api_version"

API_BASE_CONFIG_KEY = "api_base"
API_TYPE_CONFIG_KEY = "api_type"
API_VERSION_CONFIG_KEY = "api_version"
LANGCHAIN_TYPE_CONFIG_KEY = "_type"
RASA_TYPE_CONFIG_KEY = "type"
PROVIDER_CONFIG_KEY = "provider"

REQUEST_TIMEOUT_CONFIG_KEY = "request_timeout"  # deprecated
TIMEOUT_CONFIG_KEY = "timeout"

DEPLOYMENT_NAME_CONFIG_KEY = "deployment_name"
DEPLOYMENT_CONFIG_KEY = "deployment"
EMBEDDINGS_CONFIG_KEY = "embeddings"
ENGINE_CONFIG_KEY = "engine"
LLM_CONFIG_KEY = "llm"
MODEL_CONFIG_KEY = "model"
MODEL_NAME_CONFIG_KEY = "model_name"
PROMPT_CONFIG_KEY = "prompt"
PROMPT_TEMPLATE_CONFIG_KEY = "prompt_template"

STREAM_CONFIG_KEY = "stream"
N_REPHRASES_CONFIG_KEY = "n"

AZURE_API_KEY_ENV_VAR = "AZURE_API_KEY"
AZURE_AD_TOKEN_ENV_VAR = "AZURE_AD_TOKEN"
AZURE_API_BASE_ENV_VAR = "AZURE_API_BASE"
AZURE_API_VERSION_ENV_VAR = "AZURE_API_VERSION"
AZURE_API_TYPE_ENV_VAR = "AZURE_API_TYPE"

HUGGINGFACE_MULTIPROCESS_CONFIG_KEY = "multi_process"
HUGGINGFACE_CACHE_FOLDER_CONFIG_KEY = "cache_folder"
HUGGINGFACE_SHOW_PROGRESS_CONFIG_KEY = "show_progress"
HUGGINGFACE_MODEL_KWARGS_CONFIG_KEY = "model_kwargs"
HUGGINGFACE_ENCODE_KWARGS_CONFIG_KEY = "encode_kwargs"
HUGGINGFACE_LOCAL_EMBEDDING_CACHING_FOLDER = (
    get_local_cache_location() / "huggingface_local_embeddings"
)

REQUESTS_CA_BUNDLE_ENV_VAR = "REQUESTS_CA_BUNDLE"
REQUESTS_SSL_CONTEXT_PURPOSE_ENV_VAR = "REQUESTS_SSL_CONTEXT_PURPOSE"
RASA_CA_BUNDLE_ENV_VAR = "RASA_CA_BUNDLE"  # used in verify
RASA_SSL_CERTIFICATE_ENV_VAR = "RASA_SSL_CERTIFICATE"  # used in cert (client side)
LITELLM_SSL_VERIFY_ENV_VAR = "SSL_VERIFY"
LITELLM_SSL_CERTIFICATE_ENV_VAR = "SSL_CERTIFICATE"

OPENAI_PROVIDER = "openai"
AZURE_OPENAI_PROVIDER = "azure"
SELF_HOSTED_PROVIDER = "self-hosted"
HUGGINGFACE_LOCAL_EMBEDDING_PROVIDER = "huggingface_local"

AZURE_API_TYPE = "azure"
OPENAI_API_TYPE = "openai"

RASA_DEFAULT_FLOW_PATTERN_PREFIX = "pattern_"
CONTEXT = "context"

RASA_PATTERN_INTERNAL_ERROR = "pattern_internal_error"
RASA_PATTERN_HUMAN_HANDOFF = "pattern_human_handoff"

RASA_INTERNAL_ERROR_PREFIX = "rasa_internal_error_"
RASA_PATTERN_INTERNAL_ERROR_DEFAULT = RASA_INTERNAL_ERROR_PREFIX + "default"
RASA_PATTERN_INTERNAL_ERROR_USER_INPUT_TOO_LONG = (
    RASA_INTERNAL_ERROR_PREFIX + "user_input_too_long"
)
RASA_PATTERN_INTERNAL_ERROR_USER_INPUT_EMPTY = (
    RASA_INTERNAL_ERROR_PREFIX + "user_input_empty"
)

RASA_PATTERN_CANNOT_HANDLE_PREFIX = "cannot_handle_"
RASA_PATTERN_CANNOT_HANDLE_DEFAULT = RASA_PATTERN_CANNOT_HANDLE_PREFIX + "default"
RASA_PATTERN_CANNOT_HANDLE_CHITCHAT = RASA_PATTERN_CANNOT_HANDLE_PREFIX + "chitchat"
RASA_PATTERN_CANNOT_HANDLE_NOT_SUPPORTED = (
    RASA_PATTERN_CANNOT_HANDLE_PREFIX + "not_supported"
)
RASA_PATTERN_CANNOT_HANDLE_INVALID_INTENT = (
    RASA_PATTERN_CANNOT_HANDLE_PREFIX + "invalid_intent"
)

ROUTE_TO_CALM_SLOT = "route_session_to_calm"
