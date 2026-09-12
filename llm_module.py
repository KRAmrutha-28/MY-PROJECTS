import google.generativeai as genai
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMModule:
    def __init__(self, api_key=None, config=None, model_name=None, prompt=None, temperature=0.7, top_p=0.95, max_length=2048, n_ctx=1024, batch_size=32, device='cpu'):
        """
        Initialize the LLM module with Gemini API
        
        Args:
            api_key (str): Google Gemini API key (simple initialization)
            config: Alternative way to pass API key (for backward compatibility)
            model_name (str): Model name to use
            prompt (str): System prompt
            temperature (float): Temperature for generation
            top_p (float): Top p for generation
            max_length (int): Maximum length of generated text
            n_ctx (int): Context window size
            batch_size (int): Batch size for processing
            device (str): Device to use (cuda/cpu)
        """
        # Store all parameters
        self.model_name = model_name
        self.prompt = prompt if prompt else "You are an expert SQL query generator and data analyst."
        self.temperature = temperature
        self.top_p = top_p
        self.max_length = max_length
        self.n_ctx = n_ctx
        self.batch_size = batch_size
        self.device = device
        self.model = None
        
        try:
            # Determine the API key from various possible sources
            final_api_key = None
            
            # Check if api_key was provided directly
            if api_key:
                final_api_key = api_key
                logger.info("Using directly provided API key")
            elif config:
                if isinstance(config, str):
                    final_api_key = config
                    logger.info("Using config string as API key")
                elif hasattr(config, 'GEMINI_API_KEY'):
                    final_api_key = config.GEMINI_API_KEY
                    logger.info("Using config object with GEMINI_API_KEY attribute")
            else:
                final_api_key = os.getenv('GEMINI_API_KEY')
                if final_api_key:
                    logger.info("Using API key from environment variable")
            
            if not final_api_key:
                raise Exception("No API key found. Please provide GEMINI_API_KEY")
            
            # Configure the API
            logger.info("Configuring Gemini API...")
            genai.configure(api_key=final_api_key)
            
            # Test the API key by listing models
            logger.info("Testing API connection...")
            models = genai.list_models()
            
            # Print available models for debugging
            logger.info("Available models:")
            model_list = []
            for model in models:
                model_list.append(model.name)
                logger.info(f"  - {model.name}")
            
            # Try to initialize the model with different possible names
            self.model = None
            
            # Model names to try
            model_names_to_try = [
                'models/gemini-2.0-flash',
                'gemini-2.0-flash',
                'models/gemini-2.0-flash-001',
                'gemini-2.0-flash-001',
                'models/gemini-2.0-flash-lite-001',
                'gemini-2.0-flash-lite-001',
                'models/gemini-2.0-flash-lite',
                'gemini-2.0-flash-lite',
                'models/gemma-3-1b-it',
                'gemma-3-1b-it',
                'models/gemma-3-4b-it',
                'gemma-3-4b-it',
                'models/gemini-1.5-pro',
                'gemini-1.5-pro',
                'models/gemini-pro',
                'gemini-pro'
            ]
            
            # If a specific model name was provided, try it first
            if self.model_name and self.model_name not in model_names_to_try:
                model_names_to_try.insert(0, self.model_name)
            
            # Try each model name until one works
            for model_name_try in model_names_to_try:
                try:
                    logger.info(f"Attempting to initialize model: {model_name_try}")
                    self.model = genai.GenerativeModel(model_name_try)
                    
                    # Test the model with a simple prompt
                    test_response = self.model.generate_content(
                        "Hello", 
                        generation_config={"max_output_tokens": 5}
                    )
                    
                    if test_response and test_response.text:
                        logger.info(f"✓ Successfully initialized model: {model_name_try}")
                        logger.info(f"Test response: {test_response.text}")
                        self.model_name = model_name_try
                        break
                    else:
                        logger.warning(f"Model {model_name_try} initialized but test failed")
                        self.model = None
                        
                except Exception as e:
                    logger.warning(f"Failed to initialize {model_name_try}: {str(e)}")
                    self.model = None
                    continue
            
            # If no model was successfully initialized, raise an exception
            if self.model is None:
                clean_models = []
                for m in model_list:
                    if 'models/' in m and not any(c in m for c in ['#', '@', '$']):
                        clean_models.append(m)
                
                available_models = ", ".join(clean_models[:10]) if clean_models else "No clean models found"
                raise Exception(f"Could not initialize any Gemini model. Available models: {available_models}")
            
            logger.info("✓ LLM Module initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM Module: {str(e)}")
            raise Exception(f"LLM initialization failed: {str(e)}")
    
    def generate_sql_query(self, natural_language_query, table_info):
        """
        Convert natural language to SQL query
        
        Args:
            natural_language_query (str): User's natural language question
            table_info (str): Database table schema information
            
        Returns:
            str: Generated SQL query
        """
        try:
            # Create a prompt for SQL generation
            prompt = f"""
            You are an expert SQL query generator. Given the following database schema and a natural language question,
            generate a valid SQL query that answers the question.
            
            Database Schema:
            {table_info}
            
            Question: {natural_language_query}
            
            Generate only the SQL query without any explanations or additional text.
            Make sure the SQL query is compatible with standard SQL syntax.
            If the question cannot be answered with the given schema, respond with: "Cannot generate SQL for this question"
            """
            
            # Generate SQL query with the configured parameters
            generation_config = {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_output_tokens": self.max_length
            }
            
            response = self.model.generate_content(prompt, generation_config=generation_config)
            
            if response and response.text:
                # Clean up the response (remove markdown formatting if present)
                sql_query = response.text.strip()
                if sql_query.startswith("```sql"):
                    sql_query = sql_query[6:]
                if sql_query.startswith("```"):
                    sql_query = sql_query[3:]
                if sql_query.endswith("```"):
                    sql_query = sql_query[:-3]
                
                return sql_query.strip()
            else:
                return "Error: No response from model"
                
        except Exception as e:
            logger.error(f"Error generating SQL: {str(e)}")
            return f"Error generating SQL: {str(e)}"
    
    def validate_and_improve_query(self, sql_query, table_info):
        """
        Validate and improve the generated SQL query
        
        Args:
            sql_query (str): The generated SQL query
            table_info (str): Database table schema information
            
        Returns:
            str: Validated/improved SQL query
        """
        try:
            # Create a prompt for SQL validation and improvement
            prompt = f"""
            You are an expert SQL validator and optimizer. Review this SQL query and improve it if necessary.
            
            Database Schema:
            {table_info}
            
            Original SQL Query:
            {sql_query}
            
            Please check for and fix:
            1. Syntax errors
            2. Table/column name correctness (ensure they exist in the schema)
            3. Query optimization opportunities
            4. SQL best practices
            5. Security issues (SQL injection risks)
            
            Return only the corrected/improved SQL query without any explanations, comments, or markdown formatting.
            If the query is already correct and optimal, return it exactly as is.
            If the query cannot be fixed, return: "ERROR: Cannot validate this query"
            """
            
            # Use lower temperature for more precise validation
            generation_config = {
                "temperature": 0.2,
                "top_p": 0.9,
                "max_output_tokens": self.max_length
            }
            
            response = self.model.generate_content(prompt, generation_config=generation_config)
            
            if response and response.text:
                improved_query = response.text.strip()
                
                # Clean up markdown formatting if present
                if improved_query.startswith("```sql"):
                    improved_query = improved_query[6:]
                elif improved_query.startswith("```"):
                    improved_query = improved_query[3:]
                if improved_query.endswith("```"):
                    improved_query = improved_query[:-3]
                
                # Check if error message was returned
                if improved_query.startswith("ERROR:"):
                    logger.warning(f"Query validation failed: {improved_query}")
                    return sql_query  # Return original on validation failure
                
                return improved_query.strip()
            else:
                logger.warning("No response from validation model, using original query")
                return sql_query
                
        except Exception as e:
            logger.error(f"Error validating/improving query: {str(e)}")
            return sql_query  # Return original on error
    
    def generate_response(self, natural_language_query, sql_query, query_result):
        """
        Generate a natural language response based on the query result
        
        Args:
            natural_language_query (str): Original user question
            sql_query (str): Executed SQL query
            query_result: Result from database query
            
        Returns:
            str: Natural language response
        """
        try:
            # Format the query result for better readability
            result_str = str(query_result)
            if len(result_str) > 1000:
                result_str = result_str[:1000] + "... (truncated)"
            
            # Create a prompt for response generation
            prompt = f"""
            You are a helpful assistant that explains database query results in natural language.
            
            Original Question: {natural_language_query}
            
            SQL Query Used: {sql_query}
            
            Query Result: {result_str}
            
            Provide a clear and concise natural language response that answers the original question based on the query result.
            If the result is empty or no data was found, explain that appropriately.
            If there are multiple rows, summarize the key findings.
            Be friendly and helpful in your response.
            """
            
            # Generate response with the configured parameters
            generation_config = {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_output_tokens": self.max_length
            }
            
            response = self.model.generate_content(prompt, generation_config=generation_config)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def generate_chart_data(self, query_result, chart_type="auto"):
        """
        Generate chart configuration based on query result
        
        Args:
            query_result: Result from database query
            chart_type (str): Type of chart (auto, bar, line, pie, etc.)
            
        Returns:
            dict: Chart configuration
        """
        try:
            # This is a simplified version - you can enhance it based on your needs
            if not query_result:
                return {"type": "none", "data": [], "message": "No data to visualize"}
            
            # Try to determine best chart type based on data structure
            if chart_type == "auto":
                # Check if query_result is a list of dictionaries/rows
                if isinstance(query_result, list) and len(query_result) > 0:
                    # Get the first row to analyze structure
                    first_row = query_result[0]
                    
                    # Count numeric vs non-numeric columns
                    numeric_count = 0
                    if isinstance(first_row, dict):
                        for key, value in first_row.items():
                            if isinstance(value, (int, float)):
                                numeric_count += 1
                    
                    # Decide chart type based on data
                    if numeric_count >= 2:
                        chart_type = "bar"
                    elif numeric_count == 1:
                        chart_type = "pie"
                    else:
                        chart_type = "table"
                else:
                    chart_type = "table"
            
            # Prepare data for chart
            chart_config = {
                "type": chart_type,
                "data": query_result,
                "title": "Query Results Visualization",
                "timestamp": str(os.times().elapsed)  # Simple unique identifier
            }
            
            return chart_config
            
        except Exception as e:
            logger.error(f"Error generating chart data: {str(e)}")
            return {"type": "none", "data": [], "error": str(e)}
    
    def test_connection(self):
        """
        Test the API connection with a simple query
        
        Returns:
            bool: True if connection is working, False otherwise
        """
        try:
            test_prompt = "Say 'Connection successful' in one line"
            response = self.model.generate_content(
                test_prompt, 
                generation_config={"max_output_tokens": 10}
            )
            
            if response and response.text:
                logger.info(f"Connection test successful: {response.text}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def get_model_info(self):
        """
        Get information about the current model
        
        Returns:
            dict: Model information
        """
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_length": self.max_length,
            "device": self.device
        }

# For testing the module directly
if __name__ == "__main__":
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        print("Make sure you have a .env file with: GEMINI_API_KEY=your_key_here")
    else:
        # Test the LLM module
        try:
            print("=" * 50)
            print("Testing LLM Module...")
            print("=" * 50)
            
            print(f"API Key length: {len(api_key)}")
            print(f"API Key starts with: {api_key[:10]}...")
            
            # Initialize the module
            print("\n1. Initializing LLM Module...")
            llm = LLMModule(api_key=api_key)
            
            # Test connection
            print("\n2. Testing Connection...")
            if llm.test_connection():
                print("✓ Connection test passed")
                print(f"✓ Using model: {llm.model_name}")
            else:
                print("✗ Connection test failed")
            
            # Get model info
            print("\n3. Model Information:")
            model_info = llm.get_model_info()
            for key, value in model_info.items():
                print(f"   - {key}: {value}")
            
            # Test SQL generation with a simple example
            print("\n4. Testing SQL Generation...")
            test_schema = "Table: users (id INT, name VARCHAR, age INT, email VARCHAR)"
            test_question = "Show me all users older than 25"
            
            sql = llm.generate_sql_query(test_question, test_schema)
            print(f"   Question: {test_question}")
            print(f"   Generated SQL: {sql}")
            
            # Test validation
            print("\n5. Testing Query Validation...")
            validated = llm.validate_and_improve_query(sql, test_schema)
            print(f"   Validated SQL: {validated}")
            
            print("\n" + "=" * 50)
            print("✓ All tests completed!")
            print("=" * 50)
                
        except Exception as e:
            print(f"\n✗ Error: {e}")