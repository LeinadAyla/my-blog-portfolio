import google.generativeai as genai

# SUA CHAVE MESTRE INTEGRADA COM SUCESSO
CHAVE_API_GEMINI = "AIzaSyD4k4NHjnLHgEZQYqfS96QFk2s9R1yIrnc"

# Configuração da conexão com o QG do Gemini
genai.configure(api_key=CHAVE_API_GEMINI)

def pedir_ajuda_ia(texto_usuario):
    """
    Agente Mentor: Revisa gramática e sugere melhorias técnicas de Engenharia.
    """
    try:
        # Utilizamos o modelo 1.5 Flash para resposta instantânea
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Você é um mentor sênior de Engenharia de Software. 
        Analise o seguinte texto para um post de blog técnico:
        
        '{texto_usuario}'
        
        Por favor:
        1. Corrija erros gramaticais mantendo o tom profissional.
        2. Sugira 2 melhorias técnicas ou termos mais precisos de computação.
        3. Sugira 3 hashtags relevantes para LinkedIn.
        
        Responda de forma curta e direta, padrão militar. SELVA!
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # Retorno de erro estruturado para não derrubar o sistema
        return f"Erro na comunicação com o QG da IA: {str(e)}"